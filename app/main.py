from src.lexer.lexer import Lexer

def main():
    input_string = """
    alex = 4
    if alex
        print { 4 }
    """
    print(input_string)
    lex = Lexer(input_string)
    lex.scan()
    for tok in lex.tokens:
        print(tok)

if __name__ == "__main__":
    main()
