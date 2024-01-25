from src.utils.token import Token, TType
from .errors import ClassySyntaxError, ClassyIndentationError

class Lexer:
    """
    Lexer class consisting of input string.
    The input string can either be a text file or an actual string.

    Main task:
        walk through the file and save new tokens and lexemes
    """
    def __init__(self, inp: str):
        self.input:     int             = inp
        self.start:     int             = 0
        self.curr:      int             = self.start
        self.input_len: int             = len(inp)
        self.end:       int             = self.input_len
        self.tokens:    list[Token]     = []
        self.lexemes:   list[str]       = []
        self.line:      int             = 0
        self.indents:   list[int]       = [0]
        
    @property
    def last_indent(self) -> int:
        return self.indents[-1]

    def close_blocks(self, curr_indent: int):
        for ind in reversed(self.indents):
            if curr_indent < ind:
                self.add_token(TType.ENDBLOCK)
                self.indents.pop()

    def open_block(self, curr_indent: int):
        """
        Add a STARTBLOCK token and register the current indentation level.
        """
        last_indent = self.last_indent
        self.add_token(TType.STARTBLOCK)
        self.indents.append(curr_indent)

    def handle_indentation(self):
        spaces: int = 0
        while True:
            next_char = self.get_char(1)
            if next_char == " ":
                spaces += 1
                self.curr += 1
            elif next_char == "\t":
                spaces += 4
                self.curr += 1

            elif next_char == "\n":
                # this is just an empty line
                self.curr += 1
                return

            else:
                break

        indentation_level = spaces // 4
        last_indent: int = self.last_indent
        if (spaces % 4) != 0:
            raise ClassyIndentationError(f"""
                Indentation error:: 
                    last_indent: {last_indent}, 
                    indent: {indentation_level}, 
                    line: {self.line},
                    curr: {self.curr}

            """)

        if indentation_level == last_indent:
            return

        elif indentation_level < last_indent:
            return self.close_blocks(indentation_level)

        elif indentation_level > last_indent:
            return self.open_block(indentation_level)

    def close_all_blocks(self) -> None:
        """
        After the scanning has been finished some blocks might still be open.
        Close them all.
        """
        for indent in self.indents:
            self.add_token(TType.ENDBLOCK)
            self.indents.pop()


    def scan(self) -> tuple[list[Token], list[str]]:
        """
        Scan the input string and return the list of tokens
        generated and the list of lexemes.
        """
        while self.at_end is False:
            curr_char = self.get_char()
            if curr_char.isalpha() or curr_char == "_":
                self.get_keyword()

            elif curr_char.isdigit():
                self.get_number()

            elif curr_char == "\n":
                self.line += 1
                self.handle_indentation()

            elif curr_char == " ":
                pass

            elif curr_char == "\t":
                pass

            elif curr_char == "=":
                self.add_token(TType.EQ)

            elif curr_char == "{":
                self.add_token(TType.LBRACE)

            elif curr_char == "}":
                self.add_token(TType.RBRACE)

            elif curr_char == "+":
                next_char = self.get_char(1)
                if next_char == "+":
                    # handle unary inc
                    self.add_token(TType.UNARY_INC)
                    self.curr += 1
                else:
                    self.add_token(TType.PLUS)

            elif curr_char == "-":
                next_char = self.get_char(1)
                if next_char == "-":
                    # handle unary inc
                    self.add_token(TType.UNARY_DEC)
                    self.curr += 1
                else:
                    self.add_token(TType.MINUS)

            elif curr_char == "*":
                next_char = self.get_char(1)
                if next_char == "*":
                    # handle unary inc
                    self.add_token(TType.POWER)
                    self.curr += 1
                else:
                    self.add_token(TType.TIMES)

            elif curr_char == "/":
                next_char = self.get_char(1)
                if next_char == "/":
                    # handle unary inc
                    self.add_token(TType.FLOOR)
                    self.curr += 1
                else:
                    self.add_token(TType.SLASH)

            else: 
                raise ClassySyntaxError(f"Error line: {self.line}")

            self.curr += 1
        
        return self.close_all_blocks()

    def add_token(self, t: TType):
        self.tokens.append(Token(t))
    
    def get_char(self, offset: int = 0) -> str:
        """
        Get the character at the specific offset. This can return potentially nothing
        signifying that it is out of the boundaries of the string.
        """
        final = self.curr + offset
        if final < self.end:
            return self.input[self.curr + offset]
        return ""

    @property
    def curr_char(self) -> str:
        """
        Return the current character
        """
        return self.input[self.curr]

    @property
    def at_end(self) -> bool:
        """
        Check if we have hit the end.
        """
        return self.curr >= self.end

    def get_string(self) -> Token:
        """
        Consume the keyword and return the string token.
        """

    def get_number(self):
        """
        Consume the number and return either a float or an integer.
        """
        final_number = self.curr_char
        while True:
            next_char = self.get_char(1)
            if next_char == ".":
                self.curr += 1
                final_number += next_char
                return self.get_decimal(final_number)
            if next_char.isdigit():
                final_number += next_char
                self.curr += 1
                continue
            break
        
        self.lexemes.append(final_number)
        t = TType.INT
        token = Token(t)
        self.tokens.append(token)

    def get_decimal(self, number: str):
        """
        Return the decimal number.
        """
        while True:
            next_char = self.get_char(1)
            if next_char == ".":
                raise ClassySyntaxError("double floating pointe")
            if next_char.isdigit():
                number += next_char
                self.curr += 1
                continue
            break

        self.lexemes.append(number)
        t = TType.DECIMAL
        token = Token(t)
        self.tokens.append(token)


    def get_keyword(self) -> None:
        """
        Consume the keyword and return the corresponding token
        or an error.
        """
        final_keyword = self.get_char(0)
        while True:
            next_char = self.get_char(1)
            if next_char.isalpha() or next_char == "_":
                final_keyword += next_char
                self.curr += 1
                continue
            break
        try:
            copy_keyword = final_keyword.upper()
            t = TType[copy_keyword]
            token = Token(t)
            self.tokens.append(token)
        except KeyError:
            self.lexemes.append(final_keyword)
            t = TType.VAR
            token = Token(t)
            self.tokens.append(token)
