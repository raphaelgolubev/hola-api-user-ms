import re

class ANSI(str):
    ESC = '\033'
    END = ESC + '[0m'

    BLACK = '30m'
    RED = '31m'
    GREEN = '32m'
    YELLOW = '33m'
    BLUE = '34m'
    PURPLE = '35m'
    CYAN = '36m'
    WHITE = '37m'

    BOLD = '1m'
    FAINT = '2m'
    ITALIC = '3m'
    UNDERLINE = '4m'
    INVERSE = '7m'
    CROSSED = '9m'

    black        = property(lambda self: ANSI(f"{self.ESC}[{self.BLACK}{self}"))
    red          = property(lambda self: ANSI(f"{self.ESC}[{self.RED}{self}"))
    green        = property(lambda self: ANSI(f"{self.ESC}[{self.GREEN}{self}"))
    yellow       = property(lambda self: ANSI(f"{self.ESC}[{self.YELLOW}{self}"))
    blue         = property(lambda self: ANSI(f"{self.ESC}[{self.BLUE}{self}"))
    purple       = property(lambda self: ANSI(f"{self.ESC}[{self.PURPLE}{self}"))
    cyan         = property(lambda self: ANSI(f"{self.ESC}[{self.CYAN}{self}"))
    white        = property(lambda self: ANSI(f"{self.ESC}[{self.WHITE}{self}"))

    bold         = property(lambda self: ANSI(f"{self.ESC}[{self.BOLD}{self}"))
    faint        = property(lambda self: ANSI(f"{self.ESC}[{self.FAINT}{self}"))
    italic       = property(lambda self: ANSI(f"{self.ESC}[{self.ITALIC}{self}"))
    underline    = property(lambda self: ANSI(f"{self.ESC}[{self.UNDERLINE}{self}"))
    inverse      = property(lambda self: ANSI(f"{self.ESC}[{self.INVERSE}{self}"))
    crossed      = property(lambda self: ANSI(f"{self.ESC}[{self.CROSSED}{self}"))

    end          = property(lambda self: ANSI(f"{self}{self.END}"))

    @property
    def bg(self):
        # Заменяем '[3<цифра>m' на '[4<цифра>m'
        code = self.extract_ansi_codes()[0]
        to_replace = code.replace('3', '4')
        updated_text = self.replace(code, to_replace)
        # updated_text = re.sub(r'\[3(\d)m', r'[4\1m', self)
        return ANSI(updated_text)

    @property
    def fg(self):
        # Заменяем '[4<цифра>m' на '[3<цифра>m'
        code = self.extract_ansi_codes()[0]
        to_replace = code.replace('4', '3')
        updated_text = self.replace(code, to_replace)
        # updated_text = re.sub(r'\[4(\d)m', r'[3\1m', self)
        return ANSI(updated_text)

    def extract_ansi_codes(self):
        # Используем регулярное выражение для поиска ANSI кодов
        pattern = r'(\x1b\[[0-?9;]*[mK])'
        ansi_codes = re.findall(pattern, self)
        return ansi_codes

    def remove_ansi_codes(text):
        # Удаляем ANSI коды с помощью регулярного выражения
        cleaned_text = re.sub(r'\x1B\[[0-?9;]*[mK]', '', text)
        return cleaned_text  # Возвращаем новую строку без ANSI кодов

    @staticmethod
    def remove_ansi(func):
        def wrapper(*args, **kwargs):
            arguments = list(args)
            keyword_args = kwargs

            for i, arg in enumerate(arguments):
                if isinstance(arg, str):
                    arguments[i] = ANSI(arg).remove_ansi_codes()

            for key, value in keyword_args.items():
                if isinstance(value, str):
                    keyword_args[key] = ANSI(value).remove_ansi_codes()

            return func(*tuple(arguments), **keyword_args)

        return wrapper


def _display_test_str(text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."):
    test_str = ANSI(text)

    print("Как выглядит каждый стиль\n")
    print("black:", test_str.black.end)
    print("red:", test_str.red.end)
    print("green:", test_str.green.end)
    print("yellow:", test_str.yellow.end)
    print("blue:", test_str.blue.end)
    print("purple:", test_str.purple.end)
    print("cyan:", test_str.cyan.end)
    print("white:", test_str.white.end)

    print("bold:", test_str.bold.end)
    print("faint:", test_str.faint.end)
    print("italic:", test_str.italic.end)
    print("underline:", test_str.underline.end)
    print("inverse:", test_str.inverse.end)
    print("crossed:", test_str.crossed.end)

# _display_test_str()
