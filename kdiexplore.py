#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kdiexplore — read-only обозреватель и экстрактор образов дисков KDI
(Корвет ПК8020, CP/M 2.2).

URL:      https://github.com/reclaimed/kdiexplore
Лицензия: Zero-Clause BSD (0BSD)
Версия:   1.0
Python:   3.6+ (без внешних зависимостей)
Платформы: Windows / Linux / macOS


НАЗНАЧЕНИЕ
----------
Разбор и извлечение данных из образов дисков KDI, снятых с советского
компьютера Корвет ПК8020 (формат CP/M 2.2, 800 КБ, DS/DD).

kdiexplore ничего не пишет в образ: операции изменения отсутствуют
как класс. Имена файлов в образах — КОИ8-Р. Код возврата:
0 — успех, 1 — предупреждения, 2 — ошибки.


ОСОБЕННОСТИ
-----------
  * Python 3.6+ без внешних зависимостей.
  * Работает на Windows / Linux / macOS.
  * Только чтение: образ никогда не модифицируется.
  * Разбор DSKINFO, геометрии, каталога, экстентов и блоков CP/M.
  * Карта всех 128-байтных записей образа с классификацией
    (SYS / DIR / FILE / SLACK / DEL / CROSS / FREE / ...) и хешами.
  * Диагностика: контрольная сумма, геометрия, перекрёстные ссылки,
    осиротевшие блоки, повреждённые файлы.
  * Машинный вывод JSON (по объекту на строку или с отступом).
  * Перекодировка содержимого и имён: КОИ8-Р (по умолчанию), CP866,
    либо без перекодировки (--raw).
  * Экранирование опасных и нестандартных байтов имён как %XX
    (обратная операция — команда name).
  * Режим --recover: продолжение работы при ошибках контрольной суммы,
    каталога и отсутствующих данных (с предупреждениями).
  * Отчёт о неизвестных и неподтверждённых токенах MBASIC в BAS-файлах.


ИСПОЛЬЗОВАНИЕ
-------------
    kdiexplore.py [ОПЦИИ] КОМАНДА [АРГУМЕНТЫ]


КОМАНДЫ
-------
    scan                Одна строка на образ: статус, хеши, геометрия,
                        загрузчик, файлы, свободное место.
    ls (list)           Листинг файлов: USER/NAME BYTES RECORDS SHA256.
    dskinfo             DSKINFO с описанием полей, производными
                        значениями и проверками.
    map                 Карта всех 128-байтных записей: что где лежит,
                        с хешами.
    check               Диагностика: контрольная сумма, геометрия,
                        перекрёстные ссылки, сироты, повреждённые файлы.
    info                Детали файла: экстенты, блоки, дорожки, записи,
                        секторы.
    cat (type)          Показать содержимое файла.
    rec (records)       Показать 128-байтные записи.
    raw                 Показать или сохранить байты по смещению в образе.
    x (extract)         Извлечь файлы (байт-в-байт, если не запрошена
                        перекодировка).
    xsys                Извлечь системные дорожки.
    xrec                Извлечь 128-байтные записи в файл.
    xall (unpack)       Извлечь всё в папку (по умолчанию — с именем
                        образа).
    bastokens           Отчёт о неизвестных и неподтверждённых токенах
                        MBASIC в BAS-файлах.
    name                Декодировать %XX-имена обратно в байты имён CP/M.


ОПЦИИ
-----
    -j, --json
        Машинный вывод: один JSON-объект на образ на строку.

    --pretty
        Отступы в JSON.

    -r, --recover
        Продолжать работу при ошибках контрольной суммы, каталога и
        отсутствующих данных (с предупреждениями).

    --set FIELD=VALUE
        Переопределить поле DSKINFO (можно повторять),
        например: --set DSM=394.

    -q, --quiet
        Только ошибки, без комментариев.

    -v, --verbose
        Дополнительно выводить информационные диагностики.

    -e, --encoding ENC
        Кодировка содержимого: koi8r (по умолчанию), cp866, raw
        (без перекодировки).

    --names {pretty,ascii}
        Имена на хосте: pretty сохраняет заглавную кириллицу,
        ascii экранирует каждый байт выше 0x7F.

    --fill HEX
        Байт для отсутствующих записей в режиме --recover
        (по умолчанию E5).


СЕЛЕКТОР ФАЙЛА
--------------
    [UU/|*/]NAME[.EXT][@SLOT]

    UU    — область пользователя, две hex-цифры (00..0F;
            E5 = удалённые файлы);
    без UU — 00;
    */    — любой пользователь, включая E5;
    * и ? — подстановочные знаки CP/M;
    @SLOT — выбор одного из нескольких файлов с одинаковым именем
            (номер слота показан в ls и в JSON).


АДРЕС ЗАПИСИ
------------
    T:R   — логическая дорожка от 0 и запись на дорожке от 0
            (чётные дорожки = сторона 0, нечётные = сторона 1);
    N     — абсолютный номер записи от начала образа (T*SPT+R);
    bN    — блок данных N.

    Одна запись — 128 байт, физический сектор — 1024 байта
    (8 записей), блок — 16 записей.


ИМЕНА НА ХОСТЕ
--------------
Байты имени CP/M, не входящие в A-Z 0-9 _-$!#&(){}'^+ и заглавную
кириллицу, записываются как %XX (включая строчные латинские буквы,
чтобы имена никогда не различались только регистром). Селекторы
регистронезависимы. '~N' перед точкой помечает переименование при
конфликте. Обратная операция — 'kdiexplore.py name NAME'.


КЛАССЫ КАРТЫ
------------
    INFO SYS DIR FILE SLACK DEL CROSS FREE OUTSIDE EXTRA TAIL
    Звёздочка в конце (*) = не весь диапазон заполнен 0xE5.


ПРИМЕРЫ
-------
    # Разведка по каталогу с образами
    kdiexplore.py scan -R /disks

    # Отфильтровать файлы по маске
    kdiexplore.py ls game.kdi -f '*/*.BAS'

    # Показать текстовый файл
    kdiexplore.py cat game.kdi README.TXT

    # Извлечь один файл в каталог
    kdiexplore.py x game.kdi 05/GAME.COM -o out/

    # Распаковать весь образ в ./game
    kdiexplore.py xall game.kdi

    # Показать 8 записей, начиная с дорожки 2, запись 0
    kdiexplore.py rec game.kdi 2:0 -n 8

    # Машинный листинг «плохого» образа с восстановлением
    kdiexplore.py ls -j --recover bad.kdi


ЗАМЕЧАНИЯ
---------
  * kdiexplore.py — инструмент только для чтения. Запись в образ
    невозможна по замыслу: это исключает порчу исходных данных при
    разборе повреждённых или нестандартных образов.
  * Имена файлов в образах — КОИ8-Р; при выводе на хост они
    преобразуются в Unicode (по умолчанию) или печатаются как %XX.
  * Файлы считаются в 128-байтных записях CP/M; размер в байтах —
    это records*128, а не «логическая» длина, известная DOS/CP-M-утилитам.
  * Ключ --recover не «лечит» образ, а лишь позволяет продолжать
    разбор, подставляя --fill вместо отсутствующих записей и
    печатая предупреждения.
  * Команда bastokens помечает токены MBASIC как unknown (нет записи
    в таблице) и unverified (есть, но сопоставление не подтверждено
    эталонной таблицей диалекта). Это диагностика, а не ошибка.


ФОРМАТ ОБРАЗА (KDI)
-------------------
Образ — плоский поток 128-байтных записей; дорожки логические,
начиная с 0, чередование сторон: чётные дорожки — сторона 0,
нечётные — сторона 1. Геометрия и параметры CP/M описаны в записи
DSKINFO и доступны через 'dskinfo'; их можно переопределить через
--set FIELD=VALUE, если образ размечен нестандартно. Физический
сектор — 1024 байта (8 записей), блок данных CP/M — 16 записей.


ЛИЦЕНЗИЯ
--------
Zero-Clause BSD (0BSD) — эквивалент общественного достояния
в рамках разрешительных лицензий. Разрешается любое использование,
копирование, изменение и распространение программы, в том числе
в составе проприетарных продуктов, без каких-либо условий
и без необходимости сохранять уведомление об авторстве.

Полный текст:

    Permission to use, copy, modify, and/or distribute this software
    for any purpose with or without fee is hereby granted.

    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
    WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
    AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR
    CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
    CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Полный текст лицензии также доступен по адресу:
https://opensource.org/licenses/0BSD
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys

VERSION = "1.0.0"
SCHEMA = 1

# ----------------------------------------------------------------------------
# DSKINFO
# ----------------------------------------------------------------------------
FIELDS = (
    ("LoadAddr", 0, 2, "Boot load address"),
    ("RunAddr", 2, 2, "Boot run address"),
    ("Count", 4, 2, "Physical sectors loaded at boot"),
    ("SizeDisk", 6, 1, "1 = 8 inch, 0 = 5.25 inch"),
    ("Density", 7, 1, "0 = FM, 1 = MFM"),
    ("TpI", 8, 1, "Tracks per inch: 0 = 48, 1 = 96, 2 = 135"),
    ("Skew", 9, 1, "1 = no translation table, else table size (info sector bytes 33-128)"),
    ("SecSize", 10, 1, "Physical sector: 0 = 128, 1 = 256, 2 = 512, 3 = 1024 bytes"),
    ("InSide", 11, 1, "0 = single side, 1 = double side"),
    ("SecPerTrack", 12, 2, "Physical sectors per track"),
    ("TrkPerDisk", 14, 2, "Tracks per side"),
    ("SPT", 16, 2, "128-byte records per track"),
    ("BSH", 18, 1, "Block shift = log2(records per block)"),
    ("BLM", 19, 1, "Block mask = records per block - 1"),
    ("EXM", 20, 1, "Extent mask = (BLM+1)*128/1024 - 1 - DSM/256"),
    ("DSM", 21, 2, "Data blocks - 1"),
    ("DRM", 23, 2, "Directory entries - 1"),
    ("AL0", 25, 1, "Directory block map, bit 7 = block 0"),
    ("AL1", 26, 1, "Directory block map, continued"),
    ("CKS", 27, 2, "Directory check vector size = (DRM+1)/4, 0 if fixed disk"),
    ("OFS", 29, 2, "Reserved (system) tracks before the directory"),
    ("CRC", 31, 1, "8-bit checksum: (0x66 + sum of bytes 0..30) & 0xFF"),
)
FIELD_INDEX = dict((n, (o, s)) for n, o, s, _ in FIELDS)

DELETED = 0xE5
EOF_MARK = 0x1A


def meaning(name, v):
    t = {
        "SizeDisk": {0: '5.25"', 1: '8"'},
        "Density": {0: "FM", 1: "MFM"},
        "TpI": {0: "48 TpI", 1: "96 TpI", 2: "135 TpI"},
        "InSide": {0: "single-sided", 1: "double-sided"},
    }
    if name in t:
        return t[name].get(v, "unknown")
    if name in ("LoadAddr", "RunAddr"):
        return "0x%04X" % v
    if name == "SecSize":
        return "%d bytes" % (128 << v) if v <= 3 else "invalid"
    if name == "Skew":
        return "no table" if v == 1 else "table of %d bytes" % v
    if name == "CRC":
        return "checksum"
    return ""


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------
def sha256(b):
    return hashlib.sha256(b).hexdigest()


def hexb(b):
    return "".join("%02X" % c for c in b)


def ceil_div(a, b):
    return -(-a // b)


ENC_ALIASES = {"koi8r": "koi8_r", "koi8-r": "koi8_r", "koi8_r": "koi8_r",
               "cp866": "cp866", "ibm866": "cp866", "866": "cp866",
               "raw": "raw", "orig": "raw", "original": "raw"}


def norm_enc(name):
    k = ENC_ALIASES.get(str(name).lower())
    if not k:
        raise argparse.ArgumentTypeError("encoding must be koi8r, cp866 or raw")
    return k


_dec_cache = {}


def dec_table(enc):
    if enc not in _dec_cache:
        _dec_cache[enc] = [bytes([i]).decode(enc, "replace") for i in range(256)]
    return _dec_cache[enc]


def decode_text(data, enc):
    if enc == "raw":
        return data.decode("ascii", "backslashreplace")
    return data.decode(enc, "replace")


_ctrl_re = re.compile("[\x00-\x08\x0b-\x1f\x7f]")


def screen_text(data, enc, stop_eof=True):
    """Text for a terminal: stop at first ^Z, CRLF->LF, controls as ^X."""
    hidden = 0
    if stop_eof:
        i = data.find(bytes([EOF_MARK]))
        if i >= 0:
            hidden = len(data) - i
            data = data[:i]
    s = decode_text(data, enc).replace("\r\n", "\n")
    s = _ctrl_re.sub(lambda m: "^" + chr(ord(m.group()) ^ 0x40), s)
    return s, hidden


def hexdump(data, enc, base=0):
    tbl = dec_table(enc) if enc != "raw" else None
    lines = []
    for i in range(0, len(data), 16):
        ch = data[i:i + 16]
        a = " ".join("%02X" % c for c in ch[:8])
        b = " ".join("%02X" % c for c in ch[8:])
        hx = (a + "  " + b).ljust(48)
        asc = []
        for c in ch:
            if tbl is None:
                asc.append(chr(c) if 0x20 <= c < 0x7F else ".")
            else:
                t = tbl[c]
                asc.append(t if (c >= 0x20 and c != 0x7F and t.isprintable()) else ".")
        lines.append("%08X  %s |%s|" % (base + i, hx, "".join(asc)))
    return lines


def looks_like_text(data):
    d = data
    i = d.find(bytes([EOF_MARK]))
    if i >= 0:
        d = d[:i]
    d = d[:4096]
    if not d:
        return True
    bad = sum(1 for c in d if c < 32 and c not in (9, 10, 12, 13, 27))
    return bad * 50 <= len(d)


# ----------------------------------------------------------------------------
# reversible host names:  %XX escaping of CP/M name bytes
# ----------------------------------------------------------------------------
NAMES_PRETTY = True
SAFE = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-$!#&(){}'^+")
RESERVED = frozenset(["CON", "PRN", "AUX", "NUL"] + ["COM%d" % i for i in range(1, 10)]
                     + ["LPT%d" % i for i in range(1, 10)])


def _up_cyr(b):
    c = bytes([b]).decode("koi8_r")
    return c.isalpha() and c.isupper()


CYR_UPPER = frozenset(b for b in range(128, 256) if _up_cyr(b))


def esc_field(bs):
    out = []
    for b in bs:
        if b in SAFE:
            out.append(chr(b))
        elif NAMES_PRETTY and b in CYR_UPPER:
            out.append(bytes([b]).decode("koi8_r"))
        else:
            out.append("%%%02X" % b)
    return "".join(out)


def esc_parts(name8, ext7):
    n = bytes(name8).rstrip(b" ")
    e = bytes(ext7).rstrip(b" ")
    if not n:
        ns = "%20"
    elif n.decode("latin-1") in RESERVED:
        ns = "%%%02X" % n[0] + esc_field(n[1:])
    else:
        ns = esc_field(n)
    return ns, esc_field(e)


def esc_name(name8, ext7):
    ns, es = esc_parts(name8, ext7)
    return ns + ("." + es if es else "")


def display_name(name8, ext7):
    def d(b):
        s = bytes(b).rstrip(b" ").decode("koi8_r", "replace")
        return "".join(c if c.isprintable() else "?" for c in s)
    n, e = d(name8), d(ext7)
    return n + ("." + e if e else "")


_tok_re = re.compile(r"%([0-9A-Fa-f]{2})|(.)", re.S)


def _char_byte(ch, strict):
    if ch == "%":
        raise ValueError("bad %-escape (use %XX)")
    if strict and ch.isalpha() and ch != ch.upper():
        raise ValueError("literal lowercase letter %r is not allowed, use %%XX" % ch)
    bs = ch.upper().encode("koi8_r", "ignore")
    if len(bs) != 1:
        raise ValueError("character %r is not in KOI8-R" % ch)
    return bs[0]


def _tokens(s, strict):
    out = []
    for m in _tok_re.finditer(s):
        if m.group(1):
            out.append(("b", int(m.group(1), 16)))
        else:
            ch = m.group(2)
            if ch in "*?.":
                out.append((ch, None))
            else:
                out.append(("b", _char_byte(ch, strict)))
    return out


def _field(toks, n, wild):
    items = []
    for k, v in toks:
        if k == "b":
            items.append(("lit", v))
        elif k == "?" and wild:
            items.append(("any", 0))
        elif k == "*" and wild:
            items.extend([("any", 0)] * (n - len(items)))
            break
        else:
            raise ValueError("unexpected %r in name" % k)
        if len(items) > n:
            raise ValueError("name field longer than %d" % n)
    if len(items) > n:
        raise ValueError("name field longer than %d" % n)
    while len(items) < n:
        items.append(("lit", 0x20))
    return items


def _split_dot(toks):
    for i, (k, _) in enumerate(toks):
        if k == ".":
            return toks[:i], toks[i + 1:], True
    return toks, [], False


def unescape_name(s):
    """Host name -> (name8, ext3, rename_suffix or None).  Inverse of esc_name."""
    base, dot, ext = s.partition(".")
    m = re.search(r"~(\d+)$", base)
    ren = None
    if m:
        ren = int(m.group(1))
        base = base[:m.start()]
    nt = _tokens(base, True)
    et = _tokens(ext, True)
    if any(k != "b" for k, _ in nt + et):
        raise ValueError("unescaped special character in name")
    nf = _field(nt, 8, False)
    ef = _field(et, 3, False)
    return bytes(v for _, v in nf), bytes(v for _, v in ef), ren


def _fold_table():
    t = []
    for b in range(256):
        u = bytes([b]).decode("koi8_r").upper()
        try:
            e = u.encode("koi8_r")
            t.append(e[0] if len(e) == 1 else b)
        except UnicodeEncodeError:
            t.append(b)
    return t


FOLD = _fold_table()


def field_match(pat, bs):
    """Selector fields match ignoring case (ASCII and Cyrillic); use @SLOT to pick between case variants."""
    for (k, v), b in zip(pat, bs):
        if k == "lit" and FOLD[v] != FOLD[b]:
            return False
    return True


class Selector(object):
    """[UU/|*/]NAME[.EXT][@slot]   UU = two hex digits, E5 = deleted files."""

    def __init__(self, text, default_user=0):
        m = re.match(r"^(?:([0-9A-Fa-f]{2}|\*)/)?(.*?)(?:@(\d+))?$", text, re.S)
        g1, body, g3 = m.group(1), m.group(2), m.group(3)
        if g1 is None:
            self.user = default_user
        elif g1 == "*":
            self.user = None
        else:
            self.user = int(g1, 16)
        self.slot = int(g3) if g3 is not None else None
        self.text = text
        if body in ("", "*"):
            body = "*.*"
        nt, et, _ = _split_dot(_tokens(body, False))
        self.name = _field(nt, 8, True)
        self.ext = _field(et, 3, True)

    def matches(self, f):
        if self.user is not None and f.user != self.user:
            return False
        if self.slot is not None and f.slot != self.slot:
            return False
        return field_match(self.name, f.name) and field_match(self.ext, f.ext)


# ----------------------------------------------------------------------------
# MBASIC detokenizer (token table from KdiFileManager.html; partly verified)
# status: V verified on a real file, I inferred by list order, W wiki list
# ----------------------------------------------------------------------------
TOK = {
    0x81: "END", 0x82: "FOR", 0x83: "NEXT", 0x84: "DATA", 0x85: "INPUT", 0x86: "DIM",
    0x87: "READ", 0x88: "LET", 0x89: "GOTO", 0x8A: "RUN", 0x8B: "IF", 0x8C: "RESTORE",
    0x8D: "GOSUB", 0x8E: "RETURN", 0x8F: "REM", 0x90: "STOP", 0x91: "PRINT",
    0x92: "CLEAR", 0x93: "LIST", 0x94: "NEW", 0x95: "ON",
    0x99: "POKE", 0xAE: "DEFINT", 0xB1: "LINE", 0xD1: "CIRCLE", 0xD3: "PSET", 0xD6: "LOCATE",
    0xDC: "TO", 0xDD: "THEN", 0xDE: "TAB(", 0xDF: "STEP", 0xE0: "USR", 0xE1: "FN",
    0xE2: "SPC(", 0xE3: "NOT", 0xE4: "ERL", 0xE5: "ERR", 0xE6: "STRING$", 0xE7: "USING",
    0xE8: "INSTR", 0xE9: "'", 0xEA: "VARPTR", 0xEB: "SCRN", 0xEC: "HSCRN", 0xED: "INKEY$",
    0xEF: ">", 0xF0: "=", 0xF1: "<", 0xF2: "+", 0xF3: "-", 0xF4: "*", 0xF5: "/",
    0xF6: "^", 0xF7: "AND", 0xF8: "OR", 0xF9: "XOR", 0xFA: "EQV", 0xFB: "IMP", 0xFC: "MOD",
}
TOK2 = {0x95: "ASC"}  # functions after the 0xFF prefix
TOK_VERIFIED = frozenset([0x99, 0xAE, 0xB1, 0xD1, 0xD3, 0xD6, 0xDD, 0xDF, 0xED])
TOK_INFERRED = frozenset([0xDC, 0xDE] + list(range(0xE0, 0xED)))


def _bfl(b, p, n):
    e = b[p + n - 1]
    if e == 0:
        return "0"
    f = 0.0
    for i in range(n - 2, -1, -1):
        byte = (b[p + i] & 0x7F | 0x80) if i == n - 2 else b[p + i]
        f += byte / (256.0 ** (n - 1 - i))
    v = f * (2.0 ** (e - 128))
    if b[p + n - 2] & 0x80:
        v = -v
    return ("%.7g" if n == 4 else "%.15g") % v


def is_tokenized(data):
    return len(data) > 0 and data[0] == 0xFF


def detok(data, enc):
    """Expand a tokenized BASIC file (first byte 0xFF).  Returns dict or None."""
    if not is_tokenized(data):
        return None
    tbl = dec_table(enc) if enc != "raw" else None

    def ch(c):
        if c < 32:
            return "\\x%02X" % c
        if tbl is None:
            return chr(c) if c < 128 else "\\x%02X" % c
        return tbl[c]

    unknown, inferred, first = {}, set(), {}
    out = []
    n, p = len(data), 1
    truncated = False
    while p + 4 <= n and not truncated:
        if (data[p] | data[p + 1] << 8) == 0:
            break
        ln = data[p + 2] | data[p + 3] << 8
        s = str(ln) + " "
        p += 4
        while p < n and data[p]:
            c = data[p]
            p += 1
            need = 0
            if c in (0x0E, 0x1C, 0x0B, 0x0C):
                need = 2
            elif c == 0x0F or c == 0xFF:
                need = 1
            elif c == 0x1D:
                need = 4
            elif c == 0x1F:
                need = 8
            if p + need > n:
                s += "[truncated]"
                truncated = True
                break
            if c == 0x22:
                s += '"'
                while p < n and data[p] and data[p] != 0x22:
                    s += ch(data[p])
                    p += 1
                if p < n and data[p] == 0x22:
                    s += '"'
                    p += 1
            elif c == 0x0E:
                s += str(data[p] | data[p + 1] << 8)
                p += 2
            elif c == 0x0F:
                s += str(data[p])
                p += 1
            elif 0x11 <= c <= 0x1A:
                s += str(c - 0x11)
            elif c == 0x1C:
                v = data[p] | data[p + 1] << 8
                s += str(v - 65536 if v > 32767 else v)
                p += 2
            elif c == 0x0B:
                s += "&O" + format(data[p] | data[p + 1] << 8, "o")
                p += 2
            elif c == 0x0C:
                s += "&H" + format(data[p] | data[p + 1] << 8, "X")
                p += 2
            elif c == 0x1D:
                s += _bfl(data, p, 4)
                p += 4
            elif c == 0x1F:
                s += _bfl(data, p, 8)
                p += 8
            elif c == 0xFF:
                c2 = data[p]
                p += 1
                if c2 in TOK2:
                    s += TOK2[c2]
                else:
                    k = "FF%02X" % c2
                    unknown[k] = unknown.get(k, 0) + 1
                    first.setdefault(k, ln)
                    s += "[" + k + "]"
            elif c >= 0x80:
                w = TOK.get(c)
                if w is None:
                    k = "%02X" % c
                    unknown[k] = unknown.get(k, 0) + 1
                    first.setdefault(k, ln)
                    s += "[" + k + "]"
                else:
                    if c not in TOK_VERIFIED:
                        inferred.add(c)
                    s += w
                    if w in ("REM", "'"):
                        while p < n and data[p]:
                            s += ch(data[p])
                            p += 1
                    elif w == "DATA":
                        while p < n and data[p] and data[p] != 0x3A:
                            s += ch(data[p])
                            p += 1
            else:
                s += chr(c) if c >= 32 else "<%02X>" % c
        p += 1
        out.append(s)
    text = "\n".join(out) + ("\n" if out else "")
    return {"text": text, "lines": len(out), "unknown": unknown, "first": first,
            "unverified": sorted("%02X" % c for c in inferred), "truncated": truncated,
            "protected": False}


# ----------------------------------------------------------------------------
# image model
# ----------------------------------------------------------------------------
class Entry(object):
    pass


class FileInst(object):
    pass


class Image(object):
    def __init__(self, path, data, recover=False, overrides=None, fill=0xE5):
        self.path = path
        self.data = data
        self.size = len(data)
        self.sha = sha256(data)
        self.recover = recover
        self.overrides = overrides or {}
        self.fill = fill
        self.diag = []
        self.fatal = None
        self.is_kdi = True
        self.f = None
        self.raw_f = None
        self.crc_ok = None
        self.crc_calc = None
        self.model_ok = False
        self.entries = []
        self.files = []
        self.empty_slots = 0
        self.claims = {}
        self.cross = {}
        self.diag_label = {}
        self.selected = set()
        self._analyze()

    # -- diagnostics ---------------------------------------------------------
    def add(self, level, code, msg):
        self.diag.append((level, code, msg))

    def add_file(self, level, code, label, msg):
        self.diag_label[len(self.diag)] = label
        self.diag.append((level, code, "%s: %s" % (label, msg)))

    def fail(self, code, msg):
        self.fatal = (code, msg)
        self.add("error", code, msg)

    # -- analysis ------------------------------------------------------------
    def _insane(self):
        f = self.f
        if f["SecSize"] > 3:
            return "SecSize %d is not 0..3" % f["SecSize"]
        for k in ("SecPerTrack", "TrkPerDisk", "SPT"):
            if f[k] == 0:
                return "%s is zero" % k
        return None

    def _analyze(self):
        if self.size < 32:
            self.is_kdi = False
            self.fail("NOT_KDI", "file is %d bytes, DSKINFO needs 32" % self.size)
            return
        raw = self.data[:32]
        self.raw = raw
        f = dict((n, int.from_bytes(raw[o:o + s], "little")) for n, o, s, _ in FIELDS)
        self.raw_f = dict(f)
        self.crc_calc = (0x66 + sum(raw[:31])) & 0xFF
        self.crc_ok = self.crc_calc == f["CRC"]
        f.update(self.overrides)
        self.f = f
        bad = self._insane()
        if not self.crc_ok:
            msg = "DSKINFO checksum mismatch: stored 0x%02X, computed 0x%02X" % (f["CRC"], self.crc_calc)
            if bad and not self.overrides:
                self.is_kdi = False
                self.fail("NOT_KDI", msg + " and fields are implausible: not a KDI image")
                return
            if self.recover or self.overrides:
                self.add("warning", "CHECKSUM", msg)
            else:
                self.fail("CHECKSUM", msg + " (use --recover to continue)")
                return
        if bad:
            self.fail("GEOMETRY", "DSKINFO is unusable: " + bad)
            return
        self._model()
        self._read_dir()
        if self.fatal:
            return
        self._build_files()
        self._analyze_files()

    def _model(self):
        f = self.f
        self.sec_bytes = 128 << f["SecSize"]
        self.rps = self.sec_bytes // 128
        self.spt = f["SPT"]
        self.sides = 2 if f["InSide"] else 1
        self.tracks = f["TrkPerDisk"] * self.sides
        self.block_recs = f["BLM"] + 1
        self.block_bytes = self.block_recs * 128
        self.sys_recs = f["OFS"] * self.spt
        self.sys_bytes = self.sys_recs * 128
        self.nblocks = f["DSM"] + 1
        self.ptr16 = f["DSM"] > 255
        self.ppe = 8 if self.ptr16 else 16
        self.exm = f["EXM"]
        self.dir_entries = f["DRM"] + 1
        al = f["AL0"] << 8 | f["AL1"]
        self.dir_blocks = [i for i in range(16) if (al >> (15 - i)) & 1]
        self.nominal_bytes = self.spt * self.tracks * 128
        self.data_end = self.sys_bytes + self.nblocks * self.block_bytes
        self.nrec = ceil_div(self.size, 128)
        self.tail = self.size % 128
        self.model_ok = True
        add = self.add
        if f["InSide"] > 1:
            add("warning", "INSIDE", "InSide=%d, treated as double-sided" % f["InSide"])
        if f["SPT"] != f["SecPerTrack"] * self.rps:
            add("warning", "SPT", "SPT=%d but SecPerTrack*SecSize/128=%d (SPT is used)"
                % (f["SPT"], f["SecPerTrack"] * self.rps))
        if f["BSH"] < 16 and f["BLM"] != (1 << f["BSH"]) - 1:
            add("warning", "BSH_BLM", "BLM=%d does not match BSH=%d (BLM is used)" % (f["BLM"], f["BSH"]))
        if self.block_bytes % 1024 == 0:
            e = self.block_bytes // 1024 - 1 - (f["DSM"] >> 8)
            if e != f["EXM"]:
                add("warning", "EXM", "EXM=%d but the formula gives %d" % (f["EXM"], e))
        if f["EXM"]:
            add("info", "EXM_USED", "EXM != 0: extents are handled by CP/M 2.2 rules, not verified on real Korvet data")
        if f["Skew"] != 1:
            add("warning", "SKEW", "Skew=%d: translation table is shown but not applied" % f["Skew"])
        if f["CKS"] and f["CKS"] != self.dir_entries // 4:
            add("info", "CKS", "CKS=%d, expected (DRM+1)/4=%d" % (f["CKS"], self.dir_entries // 4))
        need, have = self.dir_entries * 32, len(self.dir_blocks) * self.block_bytes
        if need > have:
            add("warning", "DIR_AL", "directory needs %d bytes but AL0/AL1 reserve %d" % (need, have))
        if self.dir_blocks and max(self.dir_blocks) >= self.nblocks:
            add("warning", "DIR_BEYOND_DSM", "directory blocks %s but there are only %d data blocks (DSM=%d)"
                % (",".join(map(str, self.dir_blocks)), self.nblocks, f["DSM"]))
        if self.size != self.nominal_bytes:
            add("info", "SIZE", "image is %d bytes, nominal geometry gives %d (%+d)"
                % (self.size, self.nominal_bytes, self.size - self.nominal_bytes))
        if self.data_end > self.size:
            full = max(0, (self.size - self.sys_bytes) // self.block_bytes)
            add("info", "DSM_BEYOND_FILE", "declared data area ends at byte %d, image ends at %d; blocks from %d are not fully present"
                % (self.data_end, self.size, full))
        elif self.size > self.data_end:
            add("info", "AFTER_DATA", "%d bytes (%d records) follow the declared data area"
                % (self.size - self.data_end, ceil_div(self.size - self.data_end, 128)))
        if self.tail:
            add("info", "TAIL", "last record has only %d bytes" % self.tail)

    def _read_dir(self):
        off = self.sys_bytes
        n = max(0, min(self.dir_entries, (self.size - off) // 32))
        if n < self.dir_entries:
            msg = "directory truncated: %d of %d entries present" % (n, self.dir_entries)
            if self.recover:
                self.add("warning", "DIR_TRUNC", msg)
            else:
                self.fail("DIR_TRUNC", msg + " (use --recover to continue)")
                return
        users = {}
        for i in range(n):
            b = self.data[off + 32 * i: off + 32 * i + 32]
            if b[0] == DELETED and all(x == 0xE5 for x in b[1:12]):
                self.empty_slots += 1
                continue
            e = Entry()
            e.slot, e.user = i, b[0]
            e.name = bytes(b[1:9])
            e.ext_raw = bytes(b[9:12])
            e.ext = bytes(x & 0x7F for x in e.ext_raw)
            e.attrs = [nm for nm, x in zip(("RO", "SYS", "T3"), e.ext_raw) if x & 0x80]
            e.ex, e.s1, e.s2, e.rc = b[12], b[13], b[14], b[15]
            if self.ptr16:
                e.ptrs = [b[16 + 2 * k] | b[17 + 2 * k] << 8 for k in range(8)]
            else:
                e.ptrs = list(b[16:32])
            e.xn = 32 * e.s2 + e.ex
            e.rc_total = (e.ex & self.exm) * 128 + e.rc
            e.deleted = e.user == DELETED
            self.entries.append(e)
            if not e.deleted and e.user > 0x0F:
                users[e.user] = users.get(e.user, 0) + 1
            if not e.deleted:
                if e.ex > 0x1F:
                    self.add("warning", "ENTRY", "slot %d: EX=0x%02X is above 0x1F" % (i, e.ex))
                if e.rc > 0x80:
                    self.add("warning", "ENTRY", "slot %d: RC=0x%02X is above 0x80" % (i, e.rc))
        for u, c in sorted(users.items()):
            self.add("warning", "USER", "%d entries with unusual user byte 0x%02X" % (c, u))

    def _make_file(self, key, ents, inst):
        f = FileInst()
        f.user, f.name, f.ext = key
        f.ext_raw, f.attrs = ents[0].ext_raw, ents[0].attrs
        f.deleted = f.user == DELETED
        f.entries, f.slot, f.inst = ents, ents[0].slot, inst
        f.flags, f.stream, f.blocks = set(), [], []
        seen = set()
        for e in ents:
            nb = ceil_div(e.rc_total, self.block_recs)
            for r in range(e.rc_total):
                bi = r // self.block_recs
                if bi >= len(e.ptrs):
                    f.stream.append(-1)
                    f.flags.add("rc_overflow")
                    continue
                blk = e.ptrs[bi]
                if blk >= self.nblocks:
                    f.stream.append(-1)
                    f.flags.add("bad_pointer")
                    continue
                lrn = self.sys_recs + blk * self.block_recs + r % self.block_recs
                f.stream.append(lrn if (lrn + 1) * 128 <= self.size else -1)
            for bi in range(min(nb, len(e.ptrs))):
                blk = e.ptrs[bi]
                if blk < self.nblocks and blk not in seen:
                    seen.add(blk)
                    f.blocks.append(blk)
        f.records = len(f.stream)
        f.bytes = f.records * 128
        f.missing = sum(1 for x in f.stream if x < 0)
        if f.missing:
            f.flags.add("incomplete")
        xs = [e.xn for e in ents]
        if xs[0] != 0:
            f.flags.add("orphan")
        if any(b - a != self.exm + 1 for a, b in zip(xs, xs[1:])):
            f.flags.add("gap")
        if inst > 0:
            f.flags.add("duplicate")
        return f

    def _build_files(self):
        groups = {}
        for e in self.entries:
            groups.setdefault((e.user, e.name, e.ext), []).append(e)
        files = []
        for key in sorted(groups, key=lambda k: (k[0], k[1], k[2], groups[k][0].slot)):
            bynum = {}
            for e in sorted(groups[key], key=lambda e: (e.xn, e.slot)):
                bynum.setdefault(e.xn, []).append(e)
            for k in range(max(len(v) for v in bynum.values())):
                chosen = [v[k] for _, v in sorted(bynum.items()) if len(v) > k]
                files.append(self._make_file(key, chosen, k))
        cnt = {}
        for i, f in enumerate(files):
            f.id = i
            k = (f.user, f.name, f.ext)
            cnt[k] = cnt.get(k, 0) + 1
        for f in files:
            f.ambiguous = cnt[(f.user, f.name, f.ext)] > 1
        self.files = files

    def _analyze_files(self):
        dirset = set(self.dir_blocks)
        claims = {}
        for f in self.files:
            if not f.deleted:
                for b in f.blocks:
                    claims.setdefault(b, []).append(f.id)
        self.claims = claims
        for b, ids in claims.items():
            ids = sorted(set(ids))
            if len(ids) > 1 or b in dirset:
                self.cross[b] = ids
        crossed = set(i for ids in self.cross.values() for i in ids)
        for f in self.files:
            if f.id in crossed:
                f.flags.add("crosslink")
            if f.deleted and any(b in claims or b in dirset for b in f.blocks):
                f.flags.add("overlaps_live")
        text = {
            "orphan": ("ORPHAN", "first extent number is not 0 (extents of a lost file)"),
            "gap": ("EXTENT_GAP", "extent numbers are not consecutive; data is concatenated"),
            "duplicate": ("DUP_FILE", "same user/name exists more than once"),
            "bad_pointer": ("BAD_POINTER", "block pointer is beyond DSM"),
            "rc_overflow": ("RC_OVERFLOW", "record count exceeds the extent's block pointers"),
            "incomplete": ("INCOMPLETE", None),
            "crosslink": ("CROSSLINK", "shares blocks with another file or the directory"),
            "overlaps_live": ("DELETED_OVERLAP", "deleted; its blocks are reused, data is likely overwritten"),
        }
        for f in self.files:
            lv = "info" if f.deleted else "warning"
            for flag in sorted(f.flags):
                code, msg = text[flag]
                if flag == "incomplete":
                    msg = "%d of %d records are not present in the image" % (f.missing, f.records)
                if flag == "overlaps_live" and not f.deleted:
                    continue
                self.add_file(lv if flag != "overlaps_live" else "info", code, self.label(f), msg)

    # -- helpers -------------------------------------------------------------
    def label(self, f):
        s = "%02X/%s" % (f.user, esc_name(f.name, f.ext))
        if f.ambiguous:
            s += "@%d" % f.slot
        return s

    def tr(self, lrn):
        return divmod(lrn, self.spt)

    def side_cyl(self, t):
        return (t % 2, t // 2) if self.sides == 2 else (0, t)

    def content(self, f, fill=None):
        fb = bytes([self.fill if fill is None else fill]) * 128
        d = self.data
        return b"".join(d[x * 128:x * 128 + 128] if x >= 0 else fb for x in f.stream)

    def file_hash(self, f):
        if f.missing and not self.recover:
            return None
        return sha256(self.content(f))

    def stats(self):
        used = set(b for b in self.dir_blocks if b < self.nblocks)
        for b in self.claims:
            if b < self.nblocks:
                used.add(b)
        live = [f for f in self.files if not f.deleted]
        used_entries = sum(len(f.entries) for f in live)
        return {"files": len(live), "deleted_files": len(self.files) - len(live),
                "blocks_total": self.nblocks, "blocks_used": len(used),
                "blocks_free": max(0, self.nblocks - len(used)),
                "dir_entries": self.dir_entries, "dir_used": used_entries,
                "dir_free": self.dir_entries - used_entries}

    def build_map(self, full=False):
        data = self.data
        live_map, del_map = {}, {}
        for f in self.files:
            m = del_map if f.deleted else live_map
            for idx, x in enumerate(f.stream):
                if x >= 0 and x not in m:
                    m[x] = (f.id, idx)
        dirset = set(self.dir_blocks)
        runs, cur = [], None
        nom = self.nominal_bytes // 128
        for lrn in range(self.nrec):
            chunk = data[lrn * 128:lrn * 128 + 128]
            e5 = chunk.count(0xE5) == len(chunk)
            cls, label, fidx, blk = None, "-", None, None
            if lrn < self.sys_recs:
                cls = "INFO" if lrn == 0 else "SYS"
            else:
                blk = (lrn - self.sys_recs) // self.block_recs
                if blk < self.nblocks:
                    if blk in self.cross:
                        parts = (["DIR"] if blk in dirset else []) + \
                                [self.label(self.files[i]) for i in self.cross[blk][:3]]
                        cls, label = "CROSS", "+".join(parts)
                    elif blk in dirset:
                        cls = "DIR"
                    elif lrn in live_map:
                        fid, fidx = live_map[lrn]
                        cls, label = "FILE", self.label(self.files[fid])
                    elif blk in self.claims:
                        cls, label = "SLACK", self.label(self.files[self.claims[blk][0]])
                    elif lrn in del_map:
                        fid, fidx = del_map[lrn]
                        cls, label = "DEL", self.label(self.files[fid])
                    else:
                        cls = "FREE"
                elif lrn < nom:
                    cls = "OUTSIDE"
                else:
                    cls = "EXTRA"
            if len(chunk) < 128:
                cls, blk = "TAIL", None
            if not e5 and cls in ("FREE", "SLACK", "OUTSIDE", "EXTRA", "TAIL"):
                cls += "*"
            if (cur is not None and not full and cur["cls"] == cls and cur["label"] == label
                    and (fidx is None or (cur["f1"] is not None and fidx == cur["f1"] + 1))
                    and (blk is None) == (cur["blk1"] is None)):
                cur["lrn1"] = lrn
                cur["f1"] = fidx
                cur["blk1"] = blk
            else:
                cur = {"lrn0": lrn, "lrn1": lrn, "cls": cls, "label": label,
                       "f0": fidx, "f1": fidx, "blk0": blk, "blk1": blk}
                runs.append(cur)
        for r in runs:
            r["t0"], r["r0"] = self.tr(r["lrn0"])
            r["t1"], r["r1"] = self.tr(r["lrn1"])
            r["records"] = r["lrn1"] - r["lrn0"] + 1
            r["sha256"] = sha256(data[r["lrn0"] * 128:min((r["lrn1"] + 1) * 128, self.size)])
        return runs


# ----------------------------------------------------------------------------
# command infrastructure
# ----------------------------------------------------------------------------
class CmdError(Exception):
    def __init__(self, code, msg, logged=False):
        Exception.__init__(self, msg)
        self.code, self.msg, self.logged = code, msg, logged


class Ctx(object):
    def __init__(self, n):
        self.n = n
        self.used = set()
        self.used_dirs = set()


def require_model(img):
    if img.fatal:
        raise CmdError(img.fatal[0], img.fatal[1], True)


def img_status(img, diag=None):
    if not img.is_kdi:
        return "not_kdi"
    lv = set(d[0] for d in (img.diag if diag is None else diag))
    return "error" if "error" in lv else ("warn" if "warning" in lv else "ok")


def stem_of(path):
    return os.path.splitext(os.path.basename(path))[0] or "image"


def select_files(img, sels):
    out, seen = [], set()
    for sel in sels:
        hit = False
        for f in img.files:
            if sel.matches(f):
                hit = True
                if f.id not in seen:
                    seen.add(f.id)
                    out.append(f)
                    img.selected.add(img.label(f))
        if not hit:
            img.add("error", "NO_MATCH", "selector %r matched no file" % sel.text)
    return out


def file_obj(img, f, h):
    return {
        "label": img.label(f), "user": f.user, "user_hex": "%02X" % f.user, "slot": f.slot,
        "deleted": f.deleted, "ambiguous": f.ambiguous,
        "name": esc_name(f.name, f.ext), "name_display": display_name(f.name, f.ext),
        "name_raw_hex": hexb(f.name), "ext_raw_hex": hexb(f.ext_raw), "attrs": list(f.attrs),
        "records": f.records, "bytes": f.bytes, "blocks": len(f.blocks),
        "alloc_bytes": len(f.blocks) * img.block_bytes, "extents": len(f.entries),
        "sha256": h, "complete": f.missing == 0, "missing_records": f.missing,
        "flags": sorted(f.flags),
    }


def geom_str(f):
    return "%dx%dx%d/OFS%d/DSM%d/B%d" % (f["TrkPerDisk"], 2 if f["InSide"] else 1, f["SPT"],
                                        f["OFS"], f["DSM"], 128 * (f["BLM"] + 1))


def parse_addr(text, img):
    t = text.strip()
    dflt = None
    m = re.match(r"^(\d+):(\d+)$", t)
    if m:
        tt, rr = int(m.group(1)), int(m.group(2))
        if rr >= img.spt:
            raise CmdError("ADDRESS", "record %d is outside the track (SPT=%d)" % (rr, img.spt))
        lrn = tt * img.spt + rr
    else:
        m = re.match(r"^[bB](\d+)$", t)
        if m:
            b = int(m.group(1))
            if b >= img.nblocks:
                raise CmdError("ADDRESS", "block %d is beyond DSM (%d blocks)" % (b, img.nblocks))
            lrn, dflt = img.sys_recs + b * img.block_recs, img.block_recs
        elif re.match(r"^(0[xX][0-9A-Fa-f]+|\d+)$", t):
            lrn = int(t, 0)
        else:
            raise CmdError("ADDRESS", "bad address %r (use T:R, N or bN)" % text)
    if lrn >= img.nrec:
        raise CmdError("ADDRESS", "record %d is beyond the image end (%d records)" % (lrn, img.nrec))
    return lrn, dflt


def rec_obj(img, lrn, with_hex=False):
    t, r = img.tr(lrn)
    side, cyl = img.side_cyl(t)
    chunk = img.data[lrn * 128:lrn * 128 + 128]
    o = {"lrn": lrn, "track": t, "record": r, "side": side, "cylinder": cyl,
         "sector": r // img.rps + 1, "offset": lrn * 128, "bytes": len(chunk), "sha256": sha256(chunk)}
    if with_hex:
        o["hex"] = hexb(chunk)
    return o


def rec_head(o):
    return "-- T%d:%d  LRN %d  offset 0x%X  side %d cyl %d sector %d  (%d bytes) --" % (
        o["track"], o["record"], o["lrn"], o["offset"], o["side"], o["cylinder"], o["sector"], o["bytes"])


def out(s):
    sys.stdout.write(s)


def write_binary(data):
    sys.stdout.flush()
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


# -- host file writing --------------------------------------------------------
def key_of(p):
    return os.path.normcase(os.path.abspath(p)).lower()


def with_suffix(path, n):
    d, base = os.path.split(path)
    stem, dot, ext = base.partition(".")
    return os.path.join(d, "%s~%d%s%s" % (stem, n, dot, ext))


def resolve_target(path, policy, used):
    k = key_of(path)
    if k not in used and not os.path.lexists(path):
        used.add(k)
        return path, "new"
    if policy == "overwrite":
        used.add(k)
        return path, "overwrite"
    if policy == "skip":
        return None, "skip"
    if policy == "rename":
        n = 2
        while True:
            c = with_suffix(path, n)
            kc = key_of(c)
            if kc not in used and not os.path.lexists(c):
                used.add(kc)
                return c, "rename"
            n += 1
    raise CmdError("EXISTS", "target exists: %s (use -c skip|rename|overwrite)" % path)


def resolve_dir(path, policy, used):
    k = key_of(path)
    busy = k in used or (os.path.lexists(path) and not (os.path.isdir(path) and not os.listdir(path)))
    if not busy:
        used.add(k)
        return path, "new"
    if policy == "overwrite":
        used.add(k)
        return path, "overwrite"
    if policy == "skip":
        return None, "skip"
    if policy == "rename":
        n = 2
        while True:
            c = "%s~%d" % (path, n)
            kc = key_of(c)
            if kc not in used and not os.path.lexists(c):
                used.add(kc)
                return c, "rename"
            n += 1
    raise CmdError("EXISTS", "output folder exists: %s (use -c skip|rename|overwrite)" % path)


def write_atomic(path, data):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    tmp = path + ".kdix.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, path)


def host_name(f):
    ns, es = esc_parts(f.name, f.ext)
    return ns + ("." + es if es else "")


# ----------------------------------------------------------------------------
# DSKINFO
# ----------------------------------------------------------------------------
MODEL_CODES = frozenset(["CHECKSUM", "GEOMETRY", "INSIDE", "SPT", "BSH_BLM", "EXM", "EXM_USED", "SKEW",
                         "CKS", "DIR_AL", "DIR_BEYOND_DSM", "SIZE", "DSM_BEYOND_FILE", "AFTER_DATA", "TAIL",
                         "NOT_KDI"])


def derived_obj(img):
    f = img.f
    return {
        "record_bytes": 128, "sector_bytes": img.sec_bytes, "records_per_sector": img.rps,
        "records_per_track": img.spt, "sides": img.sides, "logical_tracks": img.tracks,
        "system_tracks": f["OFS"], "system_records": img.sys_recs, "system_bytes": img.sys_bytes,
        "block_records": img.block_recs, "block_bytes": img.block_bytes, "data_blocks": img.nblocks,
        "data_bytes": img.nblocks * img.block_bytes, "data_end_offset": img.data_end,
        "directory_entries": img.dir_entries, "directory_blocks": list(img.dir_blocks),
        "block_pointer_bits": 16 if img.ptr16 else 8, "pointers_per_extent": img.ppe,
        "nominal_image_bytes": img.nominal_bytes, "image_bytes": img.size,
        "image_delta": img.size - img.nominal_bytes, "image_records": img.nrec,
        "boot": {"load": f["LoadAddr"], "run": f["RunAddr"], "count": f["Count"]},
    }


def cmd_dskinfo(args, img, ctx):
    if img.f is None:
        raise CmdError(img.fatal[0], img.fatal[1], True)
    rows, lines = [], []
    for n, o, s, desc in FIELDS:
        v = img.f[n]
        ov = n in img.overrides
        rows.append({"name": n, "offset": o, "size": s, "value": v, "hex": "0x%0*X" % (s * 2, v),
                     "meaning": meaning(n, v), "description": desc, "overridden": ov,
                     "file_value": img.raw_f[n] if ov else None})
    lines.append("DSKINFO of %s (%d bytes); 32 bytes at offset 0" % (img.path, img.size))
    lines.append("%3s %2s  %-12s %7s  %-8s %s" % ("OFF", "SZ", "FIELD", "DEC", "HEX", "MEANING"))
    for r in rows:
        m = r["meaning"]
        extra = ("  [=%s]" % m) if m else ""
        if r["overridden"]:
            extra += "  [OVERRIDDEN, file has %d]" % r["file_value"]
        lines.append("%3d %2d  %-12s %7d  %-8s %s%s" % (r["offset"], r["size"], r["name"], r["value"],
                                                        r["hex"], r["description"], extra))
    obj = {"fields": rows, "checksum": {"stored": img.raw_f["CRC"], "computed": img.crc_calc,
                                         "ok": img.crc_ok}}
    lines.append("Checksum: stored 0x%02X, computed 0x%02X: %s" % (
        img.raw_f["CRC"], img.crc_calc, "OK" if img.crc_ok else "MISMATCH"))
    if img.model_ok:
        d = derived_obj(img)
        obj["derived"] = d
        lines.append("Derived:")
        for k in ("sector_bytes", "records_per_sector", "records_per_track", "sides", "logical_tracks",
                  "system_tracks", "system_records", "system_bytes", "block_records", "block_bytes",
                  "data_blocks", "data_bytes", "data_end_offset", "directory_entries",
                  "block_pointer_bits", "pointers_per_extent", "nominal_image_bytes", "image_bytes",
                  "image_delta", "image_records"):
            lines.append("  %-22s %d" % (k, d[k]))
        lines.append("  %-22s %s" % ("directory_blocks", ",".join(map(str, d["directory_blocks"])) or "-"))
        lines.append("  %-22s 0x%04X -> 0x%04X, %d physical sectors" % (
            "boot", d["boot"]["load"], d["boot"]["run"], d["boot"]["count"]))
    if img.f["Skew"] > 1:
        tbl = list(img.data[32:32 + img.f["Skew"]])
        obj["skew_table"] = tbl
        lines.append("Skew table (info sector bytes 33..): " + " ".join(map(str, tbl)))
    diag = [d for d in img.diag if d[1] in MODEL_CODES]
    if diag:
        lines.append("Checks:")
        for lv, code, msg in diag:
            lines.append("  %-7s %-16s %s" % (lv.upper(), code, msg))
    return obj, lines


# ----------------------------------------------------------------------------
# listing, info, map, check, scan
# ----------------------------------------------------------------------------
def default_user(args, filtering):
    if args.user:
        return None if args.user == "*" else int(args.user, 16)
    return 0 if filtering else None


def list_lines(img, files, hashes=True):
    lines, objs = [], []
    for f in files:
        h = img.file_hash(f) if hashes else None
        lines.append("%s %d %d %s" % (img.label(f), f.bytes, f.records, h or "-"))
        objs.append(file_obj(img, f, h))
    return lines, objs


def stats_line(img):
    st = img.stats()
    return ("# files=%d deleted=%d blocks_used=%d/%d blocks_free=%d dir_used=%d/%d" % (
        st["files"], st["deleted_files"], st["blocks_used"], st["blocks_total"], st["blocks_free"],
        st["dir_used"], st["dir_entries"]))


def cmd_ls(args, img, ctx):
    require_model(img)
    filt = args.filter or []
    du = default_user(args, bool(filt))
    sels = [Selector(s, du) for s in (filt or ["*.*"])]
    files = [f for f in img.files if any(s.matches(f) for s in sels)]
    if args.no_deleted:
        files = [f for f in files if not f.deleted]
    lines, objs = list_lines(img, files, not args.no_hash)
    lines.append(stats_line(img))
    return {"files": objs, "stats": img.stats()}, lines


def spans_of(img, e):
    out_ = []
    nb = ceil_div(e.rc_total, img.block_recs)
    for bi in range(min(nb, len(e.ptrs))):
        blk = e.ptrs[bi]
        n = min(img.block_recs, e.rc_total - bi * img.block_recs)
        sp = {"block": blk, "records": n, "valid": blk < img.nblocks}
        if blk < img.nblocks:
            l0 = img.sys_recs + blk * img.block_recs
            l1 = l0 + n - 1
            t0, r0 = img.tr(l0)
            t1, r1 = img.tr(l1)
            s0, c0 = img.side_cyl(t0)
            s1, c1 = img.side_cyl(t1)
            sp.update({"lrn0": l0, "lrn1": l1, "t0": t0, "r0": r0, "t1": t1, "r1": r1,
                       "side0": s0, "cyl0": c0, "side1": s1, "cyl1": c1,
                       "sector0": r0 // img.rps + 1, "sector1": r1 // img.rps + 1,
                       "present": (l1 + 1) * 128 <= img.size})
        out_.append(sp)
    return out_


def cmd_info(args, img, ctx):
    require_model(img)
    files = select_files(img, [Selector(s) for s in args.selectors])
    lines, objs = [], []
    for f in files:
        h = img.file_hash(f)
        o = file_obj(img, f, h)
        lines.append("%s  slot %d  %s" % (img.label(f), f.slot, "DELETED" if f.deleted else "live"))
        lines.append("  name %s ext %s  display %s  attrs %s" % (
            hexb(f.name), hexb(f.ext_raw), display_name(f.name, f.ext), ",".join(f.attrs) or "-"))
        lines.append("  size %d bytes = %d records; %d blocks (%d bytes allocated); %d extents" % (
            f.bytes, f.records, len(f.blocks), len(f.blocks) * img.block_bytes, len(f.entries)))
        lines.append("  sha256 %s" % (h or "-"))
        if f.flags:
            lines.append("  flags: " + ", ".join(sorted(f.flags)))
        exts = []
        for e in f.entries:
            sp = spans_of(img, e)
            exts.append({"slot": e.slot, "ex": e.ex, "s1": e.s1, "s2": e.s2, "rc": e.rc, "xn": e.xn,
                         "records": e.rc_total, "pointers": list(e.ptrs), "spans": sp})
            lines.append("  extent %d: slot %d  EX=%d S1=%d S2=%d RC=%d  records=%d" % (
                e.xn, e.slot, e.ex, e.s1, e.s2, e.rc, e.rc_total))
            for s in sp:
                if not s["valid"]:
                    lines.append("    block %d: invalid (beyond DSM)" % s["block"])
                    continue
                lines.append("    block %-5d LRN %d-%d  T%d:%d (side %d cyl %d sec %d) .. T%d:%d (side %d cyl %d sec %d)%s" % (
                    s["block"], s["lrn0"], s["lrn1"], s["t0"], s["r0"], s["side0"], s["cyl0"], s["sector0"],
                    s["t1"], s["r1"], s["side1"], s["cyl1"], s["sector1"],
                    "" if s["present"] else "  [NOT PRESENT IN IMAGE]"))
        o["extent_list"] = exts
        objs.append(o)
    return {"files": objs}, lines


def map_lines(runs, hashes=True):
    rows = [("T:R-T:R", "LRN", "RECS", "BLOCK", "CLASS", "LABEL", "SHA256")]
    for r in runs:
        b0, b1 = r["blk0"], r["blk1"]
        blk = "-" if b0 is None else (str(b0) if b0 == b1 else "%d-%d" % (b0, b1))
        lab = r["label"]
        if r["f0"] is not None:
            lab += "[%d]" % r["f0"] if r["f0"] == r["f1"] else "[%d-%d]" % (r["f0"], r["f1"])
        rows.append(("%d:%d-%d:%d" % (r["t0"], r["r0"], r["t1"], r["r1"]),
                     "%d-%d" % (r["lrn0"], r["lrn1"]), str(r["records"]), blk, r["cls"], lab,
                     r["sha256"] if hashes else "-"))
    w = [max(len(x[i]) for x in rows) for i in range(6)]
    res = []
    for k, x in enumerate(rows):
        s = "  ".join(x[i].ljust(w[i]) for i in range(6)) + "  " + x[6]
        res.append("# " + s if k == 0 else "  " + s)
    return res


def cmd_map(args, img, ctx):
    require_model(img)
    runs = img.build_map(args.full)
    lines = map_lines(runs, not args.no_hash)
    counts = {}
    for r in runs:
        counts[r["cls"]] = counts.get(r["cls"], 0) + r["records"]
    lines.append("# records=%d  " % img.nrec + " ".join("%s=%d" % kv for kv in sorted(counts.items())))
    lines.append("# * after a class = records are not all 0xE5")
    return {"records_total": img.nrec, "class_records": counts,
            "ranges": [dict(r, sha256=(None if args.no_hash else r["sha256"])) for r in runs]}, lines


def cmd_check(args, img, ctx):
    if img.fatal is None and img.model_ok:
        runs = img.build_map()
        cnt = {}
        for r in runs:
            cnt[r["cls"]] = cnt.get(r["cls"], 0) + r["records"]
        for cls, code, txt in (("FREE*", "FREE_DATA", "records in free blocks contain non-E5 data (possible deleted data)"),
                               ("OUTSIDE*", "OUTSIDE_DATA", "records beyond the declared data area contain non-E5 data"),
                               ("EXTRA*", "EXTRA_DATA", "records beyond the nominal geometry contain non-E5 data"),
                               ("TAIL*", "TAIL_DATA", "partial last record contains non-E5 data")):
            if cnt.get(cls):
                img.add("info", code, "%d %s" % (cnt[cls], txt))
    order = {"error": 0, "warning": 1, "info": 2}
    diag = sorted((d for d in img.diag if d[0] in order), key=lambda d: order[d[0]])
    lines = ["%-7s %-16s %s" % (lv.upper(), code, msg) for lv, code, msg in diag]
    c = dict((k, sum(1 for d in diag if d[0] == k)) for k in order)
    if not diag:
        lines.append("# no problems found")
    lines.append("# errors=%d warnings=%d info=%d" % (c["error"], c["warning"], c["info"]))
    return {"counts": c}, lines


def cmd_scan(args, img, ctx):
    obj = {"kdi": img.is_kdi, "geometry": None, "boot": None, "sys_sha256": None,
           "boot_code_sha256": None, "stats": None, "nominal_bytes": None, "delta": None,
           "beyond_nominal": None, "checksum": None}
    f = img.f
    if f is not None:
        obj["checksum"] = {"stored": img.raw_f["CRC"], "computed": img.crc_calc, "ok": img.crc_ok}
    if f is not None and not img._insane():
        nominal = f["SPT"] * f["TrkPerDisk"] * (2 if f["InSide"] else 1) * 128
        obj["geometry"] = geom_str(f)
        obj["boot"] = {"load": f["LoadAddr"], "run": f["RunAddr"], "count": f["Count"]}
        obj["nominal_bytes"], obj["delta"] = nominal, img.size - nominal
        extra = img.data[nominal:]
        obj["beyond_nominal"] = {"bytes": len(extra), "all_e5": extra.count(0xE5) == len(extra)}
        sb = f["OFS"] * f["SPT"] * 128
        if img.size >= sb:
            obj["sys_sha256"] = sha256(img.data[:sb])
            obj["boot_code_sha256"] = sha256(img.data[32:sb])
        if img.fatal is None:
            obj["stats"] = img.stats()
    st = "NOT_KDI" if not img.is_kdi else {"ok": "OK", "warn": "WARN", "error": "ERROR"}[img_status(img)]
    b = obj["boot"]
    sx = obj["stats"]
    line = " ".join([
        st, str(img.size), img.sha, obj["geometry"] or "-",
        ("%04X>%04X x%d" % (b["load"], b["run"], b["count"])) if b else "-",
        ("%d/%d" % (sx["files"], sx["deleted_files"])) if sx else "-",
        str(sx["blocks_free"]) if sx else "-",
        ("%+d" % obj["delta"]) if obj["delta"] is not None else "-",
        img.path])
    head = "# STATUS SIZE SHA256 GEOMETRY BOOT FILES/DELETED FREE_BLOCKS DELTA PATH"
    return obj, [head, line]


def cmd_bastokens(args, img, ctx):
    require_model(img)
    unknown, unver, n = {}, {}, 0
    for f in img.files:
        if f.ext.rstrip(b" ") != b"BAS" or (f.missing and not img.recover):
            continue
        d = detok(img.content(f), args.encoding)
        if d is None:
            continue
        n += 1
        for k, c in d["unknown"].items():
            u = unknown.setdefault(k, {"count": 0, "first": "%s:%d" % (img.label(f), d["first"][k])})
            u["count"] += c
        for k in d["unverified"]:
            unver[k] = unver.get(k, 0) + 1
    lines = ["# tokenized BAS files: %d" % n]
    for k in sorted(unknown):
        lines.append("unknown token %s: %d uses, first at %s" % (k, unknown[k]["count"], unknown[k]["first"]))
    for k in sorted(unver):
        lines.append("unverified token %s (%s) used in %d files" % (k, TOK[int(k, 16)], unver[k]))
    if len(lines) == 1:
        lines.append("# all tokens known and verified")
    return {"tokenized_files": n, "unknown": unknown, "unverified": unver}, lines


# ----------------------------------------------------------------------------
# viewing: cat / rec / raw
# ----------------------------------------------------------------------------
def view_data(img, data, mode, enc, past_eof, f=None):
    """Return (mode_used, lines, extra-json-fields)."""
    extra = {}
    if mode == "mbasic":
        if data[:1] == b"\xfe":
            img.add("warning", "PROTECTED", "protected BASIC file (0xFE): cannot be decoded, showing hex")
            mode = "hex"
        elif not is_tokenized(data):
            img.add("warning", "NOT_TOKENIZED", "no tokenized-BASIC flag (0xFF), showing as text")
            mode = "text"
    if mode == "mbasic":
        d = detok(data, enc)
        text = d["text"]
        if d["unknown"]:
            img.add("warning", "UNKNOWN_TOKENS", "%d unknown token kinds: %s" % (
                len(d["unknown"]), ", ".join(sorted(d["unknown"]))))
        extra.update({"text": text, "unknown_tokens": d["unknown"], "unverified_tokens": d["unverified"]})
        tl = text.split("\n")
        if tl and tl[-1] == "":
            tl.pop()
        return mode, tl, extra
    if mode == "text":
        text, hidden = screen_text(data, enc, not past_eof)
        extra.update({"text": text, "hidden_after_eof": hidden})
        if hidden and data[len(data) - hidden:].strip(bytes([EOF_MARK])):
            img.add("notice", "HIDDEN_AFTER_EOF", "%d bytes after ^Z are hidden (use --past-eof or -x)" % hidden)
        tl = text.split("\n")
        if tl and tl[-1] == "":
            tl.pop()
        return mode, tl, extra
    extra["hex"] = hexb(data)
    return "hex", hexdump(data, enc), extra


def pick_mode(mode, f, data):
    if mode != "auto":
        return mode
    if f.ext.rstrip(b" ") == b"BAS" and data[:1] == b"\xff":
        return "mbasic"
    if f.ext.rstrip(b" ") == b"BAS" and data[:1] == b"\xfe":
        return "hex"
    return "text" if looks_like_text(data) else "hex"


def cmd_cat(args, img, ctx):
    require_model(img)
    files = select_files(img, [Selector(s) for s in args.selectors])
    lines, objs = [], []
    for f in files:
        label = img.label(f)
        if f.missing and not img.recover:
            img.add("error", "INCOMPLETE", "%s: %d records are not present (use --recover)" % (label, f.missing))
            continue
        data = img.content(f)
        mode, tl, extra = view_data(img, data, pick_mode(args.mode, f, data), args.encoding, args.past_eof, f)
        if len(files) > 1:
            lines.append("==> %s <==" % label)
        lines.extend(tl)
        o = {"label": label, "mode": mode, "encoding": args.encoding, "bytes": len(data), "sha256": sha256(data)}
        o.update(extra)
        objs.append(o)
    return {"files": objs}, lines


def cmd_rec(args, img, ctx):
    require_model(img)
    lrn, dflt = parse_addr(args.addr, img)
    count = args.count or dflt or 1
    end = min(lrn + count, img.nrec)
    mode = "hex" if args.mode in ("auto", "hex") else args.mode
    objs, lines = [], []
    if mode == "hex":
        for x in range(lrn, end):
            o = rec_obj(img, x, True)
            objs.append(o)
            lines.append(rec_head(o))
            lines.extend(hexdump(img.data[x * 128:x * 128 + 128], args.encoding, x * 128))
    else:
        chunk = img.data[lrn * 128:end * 128]
        for x in range(lrn, end):
            objs.append(rec_obj(img, x))
        _, tl, extra = view_data(img, chunk, "text", args.encoding, args.past_eof)
        lines.extend(tl)
    return {"records": objs, "mode": mode}, lines


def cmd_raw(args, img, ctx):
    off = int(args.offset, 0)
    if off >= img.size:
        raise CmdError("ADDRESS", "offset %d is beyond the image end (%d bytes)" % (off, img.size))
    length = int(args.length, 0) if args.length else (img.size - off if args.output else 256)
    chunk = img.data[off:off + length]
    if args.output:
        return write_out(args, img, ctx, chunk, "raw_%X_%d.bin" % (off, len(chunk)),
                         {"offset": off})
    return ({"offset": off, "bytes": len(chunk), "sha256": sha256(chunk), "hex": hexb(chunk)},
            hexdump(chunk, args.encoding, off))


# ----------------------------------------------------------------------------
# extraction
# ----------------------------------------------------------------------------
def convert(args, img, raw, enc, label):
    steps, out_ = [], raw
    if getattr(args, "detok", False):
        d = detok(raw, enc) if is_tokenized(raw) else None
        if d is not None:
            if d["unknown"]:
                img.add("warning", "UNKNOWN_TOKENS", "%s: unknown tokens %s" % (label, ", ".join(sorted(d["unknown"]))))
            out_, steps = d["text"].encode("utf-8"), ["detok"]
        else:
            img.add("warning", "NOT_TOKENIZED", "%s: no 0xFF flag, MBASIC expansion skipped" % label)
    if not steps:
        if args.cut_eof or args.text:
            i = out_.find(bytes([EOF_MARK]))
            if i >= 0:
                out_ = out_[:i]
            steps.append("cut-eof")
        if args.recode or args.text:
            out_ = decode_text(out_, enc).encode("utf-8")
            steps.append("recode:" + enc)
    if args.eol != "keep":
        out_ = out_.replace(b"\r\n", b"\n")
        if args.eol == "crlf":
            out_ = out_.replace(b"\n", b"\r\n")
        steps.append("eol:" + args.eol)
    return out_, steps


def write_out(args, img, ctx, data, default_name, extra):
    o = args.output
    res = {"bytes": len(data), "sha256": sha256(data)}
    res.update(extra)
    if o == "-":
        if args.json:
            raise CmdError("USAGE", "-o - cannot be combined with --json")
        write_binary(data)
        return {"written": res}, []
    path = o
    if o is None or os.path.isdir(o) or o.endswith(("/", os.sep)):
        path = os.path.join(o or ".", default_name)
    dst, how = resolve_target(path, args.on_conflict, ctx.used)
    if dst is None:
        res.update({"path": path, "status": "skipped"})
        return {"written": res}, ["skipped (exists): %s" % path]
    write_atomic(dst, data)
    res.update({"path": dst, "status": "written" if how != "rename" else "renamed"})
    return {"written": res}, ["%s (%d bytes)" % (dst, len(data))]


def cmd_x(args, img, ctx):
    require_model(img)
    enc = args.encoding
    if (args.recode or args.text) and enc == "raw":
        raise CmdError("USAGE", "--recode/--text need -e koi8r or cp866")
    sels = [Selector(s) for s in args.selectors]
    files = select_files(img, sels)
    out_ = args.output
    to_stdout = out_ == "-"
    if to_stdout and (len(files) != 1 or args.json):
        raise CmdError("USAGE", "-o - needs exactly one file and no --json")
    user_dirs = any(s.user is None for s in sels)
    single = None
    if out_ and not to_stdout and len(files) == 1 and not os.path.isdir(out_) and not out_.endswith(("/", os.sep)):
        single = out_
    base = out_ if (out_ and not to_stdout and single is None) else "."
    if args.subdir and single is None and not to_stdout:
        base = os.path.join(base, stem_of(img.path))
    results, lines = [], []
    for f in files:
        label = img.label(f)
        try:
            if f.missing and not img.recover:
                raise CmdError("INCOMPLETE", "%s: %d records are not present (use --recover)" % (label, f.missing))
            raw = img.content(f)
            data, steps = convert(args, img, raw, enc, label)
            r = {"file": label, "records": f.records, "sha256": sha256(raw), "out_bytes": len(data),
                 "out_sha256": sha256(data), "convert": steps}
            if to_stdout:
                write_binary(data)
                results.append(r)
                continue
            if single:
                path = single
            elif user_dirs:
                path = os.path.join(base, "%02X" % f.user, host_name(f))
            else:
                path = os.path.join(base, host_name(f))
            dst, how = resolve_target(path, args.on_conflict, ctx.used)
            if dst is None:
                r.update({"path": path, "status": "skipped"})
                lines.append("%s skipped (exists): %s" % (label, path))
            else:
                write_atomic(dst, data)
                r.update({"path": dst, "status": "renamed" if how == "rename" else "extracted"})
                lines.append("%s -> %s (%d bytes)" % (label, dst, len(data)))
            results.append(r)
        except (CmdError, OSError) as e:
            code = e.code if isinstance(e, CmdError) else "IO"
            msg = e.msg if isinstance(e, CmdError) else "%s: %s" % (label, e)
            img.add("error", code, msg)
            results.append({"file": label, "status": "error", "message": msg})
    return {"extracted": results}, lines


def cmd_xsys(args, img, ctx):
    require_model(img)
    data = img.data[:img.sys_bytes]
    if len(data) < img.sys_bytes:
        img.add("warning", "SYS_TRUNC", "system area is cut: %d of %d bytes present" % (len(data), img.sys_bytes))
    return write_out(args, img, ctx, data, stem_of(img.path) + "_SYSTRACK.BIN",
                     {"system_tracks": img.f["OFS"]})


def cmd_xrec(args, img, ctx):
    require_model(img)
    lrn, dflt = parse_addr(args.addr, img)
    count = args.count or dflt or 1
    data = img.data[lrn * 128:(lrn + count) * 128]
    if len(data) < count * 128:
        img.add("warning", "RANGE_CUT", "range is cut at the image end: %d of %d bytes" % (len(data), count * 128))
    t, r = img.tr(lrn)
    return write_out(args, img, ctx, data, "%s_T%d_%d_N%d.bin" % (stem_of(img.path), t, r, count),
                     {"lrn": lrn, "track": t, "record": r, "records": count})


def cmd_xall(args, img, ctx):
    require_model(img)
    st = stem_of(img.path)
    if args.output:
        folder = args.output if ctx.n == 1 else os.path.join(args.output, st)
    else:
        folder = st
    folder, how = resolve_dir(folder, args.on_conflict, ctx.used_dirs)
    if folder is None:
        return {"folder": None, "status": "skipped"}, ["skipped (folder exists): %s" % st]
    used = set()
    results, saved, lines = [], {}, []
    files = [f for f in img.files if not (args.no_deleted and f.deleted)]
    for f in files:
        label = img.label(f)
        try:
            if f.missing and not img.recover:
                raise CmdError("INCOMPLETE", "%s: %d records are not present (use --recover)" % (label, f.missing))
            data = img.content(f)
            path = os.path.join(folder, "%02X" % f.user, host_name(f))
            dst, how2 = resolve_target(path, args.on_conflict, used)
            r = {"file": label, "bytes": len(data), "sha256": sha256(data)}
            if dst is None:
                r["status"] = "skipped"
                saved[f.id] = "NOT EXTRACTED (exists)"
            else:
                write_atomic(dst, data)
                r.update({"status": "renamed" if how2 == "rename" else "extracted",
                          "path": os.path.relpath(dst, folder).replace(os.sep, "/")})
                if how2 == "rename":
                    saved[f.id] = "saved as " + r["path"]
            results.append(r)
        except (CmdError, OSError) as e:
            code = e.code if isinstance(e, CmdError) else "IO"
            msg = e.msg if isinstance(e, CmdError) else "%s: %s" % (label, e)
            img.add("error", code, msg)
            results.append({"file": label, "status": "error", "message": msg})
            saved[f.id] = "NOT EXTRACTED: " + msg
    # listing with notes
    dl = ["# kdiexplore directory listing",
          "# image: %s  %d bytes  sha256 %s" % (os.path.basename(img.path), img.size, img.sha),
          "# columns: USER/NAME BYTES RECORDS SHA256"]
    for f in files:
        ll, _ = list_lines(img, [f])
        dl.extend(ll)
        if f.id in saved:
            dl.append("#   " + saved[f.id])
    dl.append(stats_line(img))
    di_obj, di_lines = cmd_dskinfo(args, img, ctx)
    runs = img.build_map()
    ml = ["# kdiexplore sector map (records of 128 bytes)",
          "# image: %s  %d bytes  sha256 %s" % (os.path.basename(img.path), img.size, img.sha)] + map_lines(runs)
    extras = [("_DSKINFO.TXT", "\n".join(di_lines) + "\n"), ("_DIRECTORY.TXT", "\n".join(dl) + "\n"),
              ("_MAP.TXT", "\n".join(ml) + "\n"), ("_SYSTRACK.BIN", img.data[:img.sys_bytes])]
    if args.manifest:
        man = {"schema": SCHEMA, "image": {"name": os.path.basename(img.path), "size": img.size, "sha256": img.sha},
               "dskinfo": di_obj, "files": [file_obj(img, f, img.file_hash(f)) for f in files],
               "map": runs, "extracted": results}
        extras.append(("_MANIFEST.json", json.dumps(man, ensure_ascii=False, indent=2) + "\n"))
    ex_res = []
    for name, content in extras:
        data = content.encode("utf-8") if isinstance(content, str) else content
        try:
            dst, _ = resolve_target(os.path.join(folder, name), args.on_conflict, used)
            if dst is None:
                ex_res.append({"name": name, "status": "skipped"})
                continue
            write_atomic(dst, data)
            ex_res.append({"name": name, "status": "written", "bytes": len(data), "sha256": sha256(data)})
        except (CmdError, OSError) as e:
            img.add("error", "IO", "%s: %s" % (name, getattr(e, "msg", e)))
            ex_res.append({"name": name, "status": "error"})
    n_ok = sum(1 for r in results if r["status"] in ("extracted", "renamed"))
    lines.append("%s: %d of %d files extracted into %s" % (os.path.basename(img.path), n_ok, len(files), folder))
    return {"folder": folder, "files": results, "extras": ex_res}, lines


# ----------------------------------------------------------------------------
# name utility (no image)
# ----------------------------------------------------------------------------
def cmd_name(args):
    rc, first = 0, True
    for s in args.names:
        o = {"schema": SCHEMA, "command": "name", "input": s}
        try:
            n8, e3, ren = unescape_name(s)
            o.update({"name_hex": hexb(n8), "ext_hex": hexb(e3), "display": display_name(n8, e3),
                      "rename_suffix": ren, "canonical": esc_name(n8, e3)})
            line = "%s  name=%s ext=%s  %s%s" % (s, o["name_hex"], o["ext_hex"], o["display"],
                                                  ("  (rename suffix ~%d)" % ren) if ren else "")
        except ValueError as e:
            o["error"] = str(e)
            line = "%s  ERROR: %s" % (s, e)
            rc = 2
        if args.json:
            out(json.dumps(o, ensure_ascii=False, indent=2 if args.pretty else None) + "\n")
        else:
            out(line + "\n")
    return rc


# ----------------------------------------------------------------------------
# CLI plumbing
# ----------------------------------------------------------------------------
class Command(object):
    def __init__(self, name, func, batch, diag_in_lines=False):
        self.name, self.func, self.batch, self.diag_in_lines = name, func, batch, diag_in_lines


COMMANDS = dict((c.name, c) for c in (
    Command("scan", cmd_scan, True),
    Command("ls", cmd_ls, True),
    Command("dskinfo", cmd_dskinfo, True, "model"),
    Command("map", cmd_map, True),
    Command("check", cmd_check, True, "all"),
    Command("info", cmd_info, False),
    Command("cat", cmd_cat, False),
    Command("rec", cmd_rec, False),
    Command("raw", cmd_raw, False),
    Command("x", cmd_x, False),
    Command("xsys", cmd_xsys, False),
    Command("xrec", cmd_xrec, False),
    Command("xall", cmd_xall, True),
    Command("bastokens", cmd_bastokens, True),
))
ALIASES = {"list": "ls", "extract": "x", "unpack": "xall", "type": "cat", "records": "rec"}

DESC = """Kdi Explorer: read-only explorer and extractor for KDI disk images (Korvet PK8020, CP/M 2.2).
Never writes to an image. File names are KOI8-R. Exit code: 0 ok, 1 warnings, 2 errors."""

EPILOG = """\
file selector   [UU/|*/]NAME[.EXT][@SLOT]   UU = user area, two hex digits (00..0F, E5 = deleted files)
                no UU = 00;  */ = any user including E5;  * and ? are CP/M wildcards;  @SLOT picks one of
                several files with the same name (slot is shown by ls and in JSON)
host names      CP/M name bytes outside A-Z 0-9 _-$!#&(){}'^+ and uppercase Cyrillic are written as %XX
                (lowercase letters too, so names never differ only by case); selectors ignore case;
                '~N' before the dot marks a
                rename on conflict.  'kdiexplore.py name NAME' reverses it.
record address  T:R = logical track from 0 and record on track from 0 (even tracks = side 0, odd = side 1);
                N = absolute record number from image start (T*SPT+R);  bN = data block N
                (a record is 128 bytes, a physical sector is 1024 bytes = 8 records, a block is 16 records)
files           ls shows size in bytes (= records*128), in 128-byte records and SHA-256 of those bytes
map classes     INFO SYS DIR FILE SLACK DEL CROSS FREE OUTSIDE EXTRA TAIL; a trailing * = not all 0xE5
examples        kdiexplore.py scan -R /disks
                kdiexplore.py ls game.kdi -f '*/*.BAS'
                kdiexplore.py cat game.kdi README.TXT
                kdiexplore.py x game.kdi 05/GAME.COM -o out/
                kdiexplore.py xall game.kdi            (into folder ./game)
                kdiexplore.py rec game.kdi 2:0 -n 8
                kdiexplore.py ls -j --recover bad.kdi
"""


def hexbyte(s):
    try:
        v = int(s, 16)
    except ValueError:
        raise argparse.ArgumentTypeError("fill must be a hex byte, e.g. E5")
    if not 0 <= v <= 255:
        raise argparse.ArgumentTypeError("fill must be 00..FF")
    return v


def add_common(p, sub):
    d = argparse.SUPPRESS if sub else None

    def dv(x):
        return argparse.SUPPRESS if sub else x
    p.add_argument("-j", "--json", action="store_true", default=dv(False),
                   help="machine output: one JSON object per image per line")
    p.add_argument("--pretty", action="store_true", default=dv(False), help="indent JSON")
    p.add_argument("-r", "--recover", action="store_true", default=dv(False),
                   help="continue despite checksum, directory and missing-data errors (with warnings)")
    p.add_argument("--set", action="append", default=d, metavar="FIELD=VALUE",
                   help="override a DSKINFO field (repeatable), e.g. --set DSM=394")
    p.add_argument("-q", "--quiet", action="store_true", default=dv(False), help="only errors, no comments")
    p.add_argument("-v", "--verbose", action="store_true", default=dv(False), help="also show info diagnostics")
    p.add_argument("-e", "--encoding", type=norm_enc, default=dv("koi8_r"), metavar="ENC",
                   help="content encoding: koi8r (default), cp866, raw (no recoding)")
    p.add_argument("--names", choices=("pretty", "ascii"), default=dv("pretty"),
                   help="host names: pretty keeps uppercase Cyrillic, ascii escapes every byte above 0x7F")
    p.add_argument("--fill", type=hexbyte, default=dv(0xE5), metavar="HEX",
                   help="byte used for missing records in --recover mode (default E5)")


def build_parser():
    fm = argparse.RawDescriptionHelpFormatter
    p = argparse.ArgumentParser(prog="kdiexplore.py", formatter_class=fm, description=DESC, epilog=EPILOG)
    p.add_argument("--version", action="version", version="Kdi Explorer " + VERSION)
    add_common(p, False)
    sub = p.add_subparsers(dest="cmd", metavar="COMMAND", title="commands")
    sub.required = True

    def mk(name, help_, aliases=()):
        sp = sub.add_parser(name, help=help_, description=help_, aliases=list(aliases), formatter_class=fm)
        add_common(sp, True)
        return sp

    def many(sp):
        sp.add_argument("images", nargs="+", metavar="IMAGE",
                        help="image files, directories, wildcards or @listfile (@- = stdin)")
        sp.add_argument("-R", "--recursive", action="store_true", help="scan directories recursively")

    def one(sp):
        sp.add_argument("image", metavar="IMAGE")

    def sels(sp):
        sp.add_argument("selectors", nargs="+", metavar="FILE", help="file selector, see below")

    def conflict(sp):
        sp.add_argument("-c", "--on-conflict", choices=("fail", "skip", "rename", "overwrite"), default="fail",
                        help="when the target exists (default fail)")

    sp = mk("scan", "one line per image: status, hashes, geometry, boot, files, free space")
    many(sp)
    sp = mk("ls", "list files: USER/NAME BYTES RECORDS SHA256", ["list"])
    many(sp)
    sp.add_argument("-f", "--filter", action="append", metavar="SEL", help="file selector (repeatable)")
    sp.add_argument("-u", "--user", metavar="UU", help="default user for selectors, hex, or *")
    sp.add_argument("--no-hash", action="store_true", help="skip SHA-256 (prints -)")
    sp.add_argument("--no-deleted", action="store_true", help="hide deleted (E5) files")
    sp = mk("dskinfo", "show DSKINFO with field descriptions, derived values and checks")
    many(sp)
    sp = mk("map", "map of all 128-byte records: what lies where, with hashes")
    many(sp)
    sp.add_argument("--full", action="store_true", help="one line per record")
    sp.add_argument("--no-hash", action="store_true", help="skip SHA-256")
    sp = mk("check", "diagnostics: checksum, geometry, crosslinks, orphans, damaged files")
    many(sp)
    sp = mk("info", "file details: extents, blocks, tracks, records, sectors")
    one(sp)
    sels(sp)
    sp = mk("cat", "show file content", ["type"])
    one(sp)
    sels(sp)
    sp.add_argument("--as", dest="mode", choices=("auto", "hex", "text", "mbasic"), default="auto",
                    help="view mode (default auto: tokenized BAS -> mbasic, text -> text, else hex)")
    sp.add_argument("-x", dest="mode", action="store_const", const="hex", help="hex + ascii, bytes as stored")
    sp.add_argument("-t", dest="mode", action="store_const", const="text", help="text, stops at first ^Z")
    sp.add_argument("-b", dest="mode", action="store_const", const="mbasic", help="expand MBASIC tokens")
    sp.add_argument("--past-eof", action="store_true", help="text mode: do not stop at ^Z")
    sp = mk("rec", "show 128-byte records", ["records"])
    one(sp)
    sp.add_argument("addr", metavar="ADDR", help="T:R, N or bN")
    sp.add_argument("-n", "--count", type=int, help="number of records (bN default: whole block)")
    sp.add_argument("--as", dest="mode", choices=("auto", "hex", "text"), default="auto")
    sp.add_argument("-x", dest="mode", action="store_const", const="hex")
    sp.add_argument("-t", dest="mode", action="store_const", const="text")
    sp.add_argument("--past-eof", action="store_true")
    sp = mk("raw", "show or save bytes at an image offset")
    one(sp)
    sp.add_argument("offset", metavar="OFFSET")
    sp.add_argument("length", nargs="?", metavar="LENGTH", help="default 256 (to the end with -o)")
    sp.add_argument("-o", "--output", metavar="PATH", help="save to PATH, a folder, or - for stdout")
    conflict(sp)
    sp = mk("x", "extract files from the image (byte-exact unless conversion is requested)", ["extract"])
    one(sp)
    sels(sp)
    sp.add_argument("-o", "--output", metavar="PATH", help="existing folder or PATH/ (several files), a file name (one file), or - for stdout")
    sp.add_argument("-D", "--subdir", action="store_true", help="put files into a folder named after the image")
    conflict(sp)
    sp.add_argument("--text", action="store_true", help="shortcut for --recode --cut-eof")
    sp.add_argument("--recode", action="store_true", help="recode to UTF-8 from the -e encoding")
    sp.add_argument("--cut-eof", action="store_true", help="stop at first ^Z")
    sp.add_argument("--detok", action="store_true", help="expand tokenized MBASIC files to text")
    sp.add_argument("--eol", choices=("keep", "lf", "crlf"), default="keep", help="line ends of the output")
    sp = mk("xsys", "extract the system tracks")
    one(sp)
    sp.add_argument("-o", "--output", metavar="PATH", help="file, folder, or - for stdout")
    conflict(sp)
    sp = mk("xrec", "extract 128-byte records to a file")
    one(sp)
    sp.add_argument("addr", metavar="ADDR", help="T:R, N or bN")
    sp.add_argument("-n", "--count", type=int, help="number of records")
    sp.add_argument("-o", "--output", metavar="PATH", help="file, folder, or - for stdout")
    conflict(sp)
    sp = mk("xall", "extract everything into a folder (default: named after the image)", ["unpack"])
    many(sp)
    sp.add_argument("-o", "--output", metavar="DIR", help="folder (one image) or root folder (several images)")
    conflict(sp)
    sp.add_argument("--no-deleted", action="store_true", help="do not extract deleted (E5) files")
    sp.add_argument("--manifest", action="store_true", help="also write _MANIFEST.json")
    sp = mk("bastokens", "report unknown and unverified MBASIC tokens in BAS files")
    many(sp)
    sp = sub.add_parser("name", help="decode %%XX host names back to CP/M name bytes", formatter_class=fm)
    add_common(sp, True)
    sp.add_argument("names", nargs="+", metavar="NAME")
    return p


def parse_overrides(items, parser):
    d = {}
    low = dict((k.lower(), k) for k in FIELD_INDEX)
    for it in items or []:
        k, eq, v = it.partition("=")
        if not eq or k.lower() not in low:
            parser.error("--set needs FIELD=VALUE, fields: " + ", ".join(n for n, _, _, _ in FIELDS))
        k = low[k.lower()]
        try:
            val = int(v, 0)
        except ValueError:
            parser.error("--set %s: bad number %r" % (k, v))
        if not 0 <= val < 256 ** FIELD_INDEX[k][1]:
            parser.error("--set %s: value out of range" % k)
        d[k] = val
    return d


def expand_inputs(items, recursive):
    out_, seen = [], set()

    def add(p):
        if p not in seen:
            seen.add(p)
            out_.append(p)

    def one(it):
        if os.path.isdir(it):
            if recursive:
                for root, dirs, files in os.walk(it):
                    dirs.sort()
                    for fn in sorted(files):
                        if fn.lower().endswith(".kdi"):
                            add(os.path.join(root, fn))
            else:
                for fn in sorted(os.listdir(it)):
                    pth = os.path.join(it, fn)
                    if fn.lower().endswith(".kdi") and os.path.isfile(pth):
                        add(pth)
        elif not os.path.exists(it) and any(c in it for c in "*?["):
            for g in sorted(glob.glob(it, recursive=True)):
                if os.path.isdir(g):
                    one(g)
                else:
                    add(g)
        else:
            add(it)

    for it in items:
        if it.startswith("@") and len(it) > 1:
            fh = sys.stdin if it == "@-" else open(it[1:], "r", encoding="utf-8")
            try:
                for ln in fh:
                    ln = ln.rstrip("\r\n")
                    if ln.strip():
                        one(ln)
            finally:
                if fh is not sys.stdin:
                    fh.close()
        else:
            one(it)
    return out_


def process(path, cmd, args, ctx):
    env = {"schema": SCHEMA, "command": cmd.name}
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as e:
        env.update({"image": {"path": path, "size": None, "sha256": None, "kdi": None}, "status": "error",
                    "diagnostics": [{"level": "error", "code": "OPEN", "message": str(e)}]})
        return env, [], "error", [("error", "OPEN", str(e))]
    img = Image(path, data, args.recover or bool(args.overrides), args.overrides, args.fill)
    obj, lines = {}, []
    try:
        obj, lines = cmd.func(args, img, ctx)
    except CmdError as e:
        if not e.logged:
            img.add("error", e.code, e.msg)
    except (BrokenPipeError, KeyboardInterrupt):
        raise
    except Exception as e:
        img.add("error", "INTERNAL", "%s: %s" % (type(e).__name__, e))
        if args.verbose:
            import traceback
            traceback.print_exc()
    diag = img.diag
    if not cmd.batch:
        diag = [d for i, d in enumerate(img.diag)
                if i not in img.diag_label or img.diag_label[i] in img.selected]
    status = img_status(img, diag)
    env["image"] = {"path": path, "size": img.size, "sha256": img.sha, "kdi": img.is_kdi}
    env["status"] = status
    env["diagnostics"] = [{"level": a, "code": b, "message": c} for a, b, c in diag]
    env.update(obj)
    return env, lines, status, diag


def emit(env, lines, status, diag, cmd, args, ctx):
    path = env["image"]["path"]
    if args.json:
        if args.pretty:
            out(json.dumps(env, ensure_ascii=False, indent=2) + "\n")
        else:
            out(json.dumps(env, ensure_ascii=False, separators=(",", ":")) + "\n")
        return
    if cmd.batch and ctx.n > 1 and not args.quiet:
        out("# == %s\n" % path)
    for ln in lines:
        if args.quiet and ln.startswith("# "):
            continue
        out(ln + "\n")
    sys.stdout.flush()
    for lv, code, msg in diag:
        if cmd.diag_in_lines == "all" or (cmd.diag_in_lines == "model" and code in MODEL_CODES):
            continue
        if lv == "info" and not args.verbose:
            continue
        if args.quiet and lv != "error":
            continue
        sys.stderr.write("kdiexplore: %s: %s [%s] %s\n" % (path, lv, code, msg))


def rank(status, cmd):
    if status == "ok":
        return 0
    if status == "warn":
        return 1
    if status == "not_kdi":
        return 1 if cmd.name == "scan" else 2
    return 2


def run(args):
    if args.cmd == "name":
        return cmd_name(args)
    cmd = COMMANDS[args.cmd]
    paths = expand_inputs(args.images, args.recursive) if cmd.batch else [args.image]
    if not paths:
        sys.stderr.write("kdiexplore: no image files found\n")
        return 2
    ctx = Ctx(len(paths))
    worst = 0
    if cmd.name == "scan" and not args.json and not args.quiet:
        pass
    first = True
    for p in paths:
        env, lines, status, diag = process(p, cmd, args, ctx)
        if cmd.name == "scan" and not args.json and not first:
            lines = [ln for ln in lines if not ln.startswith("# ")]
        first = False
        emit(env, lines, status, diag, cmd, args, ctx)
        worst = max(worst, rank(status, cmd))
    return worst


def setup_stdio():
    for name in ("stdout", "stderr"):
        st = getattr(sys, name)
        try:
            if st.isatty():
                st.reconfigure(errors="replace")
            else:
                st.reconfigure(encoding="utf-8", errors="replace", newline="\n")
        except (AttributeError, ValueError, OSError):
            pass


def main(argv=None):
    global NAMES_PRETTY
    setup_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)
    args.cmd = ALIASES.get(args.cmd, args.cmd)
    NAMES_PRETTY = args.names == "pretty"
    args.overrides = parse_overrides(getattr(args, "set", None), parser)
    try:
        return run(args)
    except KeyboardInterrupt:
        return 130
    except BrokenPipeError:
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        except Exception:
            pass
        return 0


if __name__ == "__main__":
    sys.exit(main())
