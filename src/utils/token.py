from enum import Enum

class TType(Enum):
    """
    Token types
    """
    VAR         = 1
    INT         = 2
    FLOAT       = 3
    STRING      = 4
    BOOL        = 5
    DOUBLE      = 6
    PLUS        = 7
    MINUS       = 8
    SLASH       = 9
    COMMENT     = 10
    STARTBLOCK  = 11
    ENDBLOCK    = 12
    TINT        = 13
    TFLOAT      = 14
    TSTRING     = 15
    TBOOL       = 16
    TDOUBLE     = 17
    DECIMAL     = 18
    UNARY_INC   = 19
    UNARY_DEC   = 20
    FLOOR       = 21
    POWER       = 22
    TIMES       = 23
    LBRACE      = 24
    RBRACE      = 25
    EQ          = 26
    EQE         = 27
    NEQ         = 28
    IS          = 29
    IS_NOT      = 30
    IF          = 31
    FOR         = 32
    END         = 33
    WHILE       = 34
    FOREACH     = 35


class Token:
    """
    Token class

    name -> string
    type -> enum (int32) 
    """
    def __init__(self, t: TType):
        self.type = t
        self.name = self.type.name

    def __str__(self) -> str:
        """
        Human string representation of the token.
        """
        return f"{self.name}" 
    
    def __repr__(self) -> str:
        return f"Token({self.name}, {self.type})"

    def to_string(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.type is other.type

    def __ne__(self, other) -> bool:
        return self.type is not other.type
