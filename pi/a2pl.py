"""a2pl-Kompression (LZ77-Variante) für die Bilddaten der Surplife-Matrix.

Übernommen aus https://github.com/lambdafu/surplife (src/surplife_core/a2pl.py),
MIT-Lizenz, Copyright (c) 2026 Marcus Brinkmann. Angepasst: Spaltenhöhe fest 16 Zeilen.

Am 23.11.2026 gegen den Mitschnitt der iPhone-App geprüft: Die drei Bilder des Test-GIFs
werden Byte für Byte so komprimiert wie von der App.

Format: Jeder Befehl [op][sum_lit?][Literale][Abstand LE16][sum_copy?]; oberes Halbbyte =
Anzahl Literale (0xF = 15 + Summe), unteres = Kopierlänge - 4 (0xF = 19 + Summe).
Summenkodierung: 0xFF = +255 und weiter, sonst Wert und Ende.
"""

COL_BYTES = 16 * 2   # eine Spalte: 16 Pixel à 2 Bytes


def _sum_decode(data, offset):
    value = 0
    while offset < len(data) and data[offset] == 0xFF:
        value += 255
        offset += 1
    if offset < len(data):
        value += data[offset]
        offset += 1
    return value, offset


def _sum_encode(value):
    result = bytearray()
    while value >= 255:
        result.append(0xFF)
        value -= 255
    result.append(value)
    return bytes(result)


def decompress(data):
    fb = bytearray()
    i = 0
    while i < len(data):
        b = data[i]
        upper, lower = (b >> 4) & 0x0F, b & 0x0F
        i += 1
        if upper == 0x0F:
            ext, i = _sum_decode(data, i)
            n_lit = 15 + ext
        else:
            n_lit = upper
        fb.extend(data[i:i + n_lit])
        i += n_lit
        if i + 1 >= len(data):
            break
        dist = data[i] | (data[i + 1] << 8)
        i += 2
        if lower == 0x0F:
            length, i = _sum_decode(data, i)
            copy_len = length + 19
        else:
            copy_len = lower + 4
        start = len(fb) - dist
        if start < 0:
            for j in range(copy_len):
                fb.append(0 if start + j < 0 else fb[start + j])
        else:
            for j in range(copy_len):
                fb.append(fb[start + (j % dist) if dist > 0 else 0])
    return bytes(fb)


def _find_best_match(fb, pos, max_search=0):
    if pos < 1:
        return 0, 0
    remaining = len(fb) - pos
    if remaining < 4:
        return 0, 0
    best_dist = best_len = 0
    limit = min(pos, 0xFFFF)
    if max_search > 0:
        limit = min(limit, max_search)
    for dist in range(1, limit + 1):
        start = pos - dist
        if fb[start] != fb[pos]:
            continue
        length = 0
        while length < remaining and fb[pos + length] == fb[start + (length % dist)]:
            length += 1
        if length > best_len:
            best_len, best_dist = length, dist
            if best_len >= remaining:
                break
    return best_dist, best_len


def _emit_command(out, fb, pos, n_lit, match_dist, match_len):
    upper = min(n_lit, 15)
    lower = min(match_len - 4, 15) if match_len >= 4 else 0
    out.append((upper << 4) | lower)
    if n_lit >= 15:
        out.extend(_sum_encode(n_lit - 15))
    out.extend(fb[pos:pos + n_lit])
    out.extend(match_dist.to_bytes(2, "little"))
    if match_len > 18:
        out.extend(_sum_encode(match_len - 19))


def compress(fb, max_search=0):
    """Rohbild (spaltenweise, Vielfaches von 32 Bytes) → a2pl."""
    if len(fb) == 0 or len(fb) % COL_BYTES != 0:
        raise ValueError(f"Bild muss ein Vielfaches von {COL_BYTES} Bytes sein, nicht {len(fb)}")
    out = bytearray()
    pos = 0
    while pos < len(fb):
        remaining = len(fb) - pos
        if remaining <= 15:
            out.append((remaining << 4) | 0x0)
            out.extend(fb[pos:pos + remaining])
            break
        match_at, match_dist, match_len = None, 0, 0
        for lit_count in range(min(remaining - 3, len(fb) - pos)):
            dist, length = _find_best_match(fb, pos + lit_count, max_search)
            if length >= 4:
                match_at, match_dist = lit_count, dist
                match_len = min(length, remaining - lit_count)
                break
        if match_at is None:
            if remaining <= 15:
                out.append((remaining << 4) | 0x0)
            else:
                out.append(0xF0)
                out.extend(_sum_encode(remaining - 15))
            out.extend(fb[pos:pos + remaining])
            break
        # Firmware-Fehler: der Strom darf nicht genau auf einer Rückreferenz enden
        tail = remaining - match_at - match_len
        if tail == 0 and match_len > 4:
            match_len -= min(5, match_len - 4)
        _emit_command(out, fb, pos, match_at, match_dist, match_len)
        pos += match_at + match_len
    return bytes(out)
