import os

if os.name == 'posix':
    from subprocess import check_output
elif os.name == 'nt':
    from ctypes import windll
    user32 = windll.user32


def get_locale():
    if os.name == 'nt':
        w = user32.GetForegroundWindow()
        tid = user32.GetWindowThreadProcessId(w, 0)
        return hex(user32.GetKeyboardLayout(tid))
    elif os.name == 'posix':
        return check_output(["./xkblayout-state", "print", "%s"])


# --------------------------- РУССКИЕ СИМВОЛЫ --------------------------------------------------------------------------
abc = {
    'q': 'й', 'Q': 'Й',
    'w': 'ц', 'W': 'Ц',
    'e': 'у', 'E': 'У',
    'r': 'к', 'R': 'К',
    't': 'е', 'T': 'Е',
    'y': 'н', 'Y': 'Н',
    'u': 'г', 'U': 'Г',
    'i': 'ш', 'I': 'Ш',
    'o': 'щ', 'O': 'Щ',
    'p': 'з', 'P': 'З',
    '[': 'х', '{': 'Х',
    ']': 'ъ', '}': 'Ъ',
    'a': 'ф', 'A': 'Ф',
    's': 'ы', 'S': 'Ы',
    'd': 'в', 'D': 'В',
    'f': 'а', 'F': 'А',
    'g': 'п', 'G': 'П',
    'h': 'р', 'H': 'Р',
    'j': 'о', 'J': 'О',
    'k': 'л', 'K': 'Л',
    'l': 'д', 'L': 'Д',
    ';': 'ж', ':': 'Ж',
    "'": 'э', '"': 'Э',
    'z': 'я', 'Z': 'Я',
    'x': 'ч', 'X': 'Ч',
    'c': 'с', 'C': 'С',
    'v': 'м', 'V': 'М',
    'b': 'и', 'B': 'И',
    'n': 'т', 'N': 'Т',
    'm': 'ь', 'M': 'Ь',
    ',': 'б', '<': 'Б',
    '.': 'ю', '>': 'Ю',
    '/': '.', '?': ','
}


def get_symbol(s):
    if str(get_locale())[2:-1] == 'ru' and abc.get(s) is not None:
        return abc.get(s)
    else:
        return s
