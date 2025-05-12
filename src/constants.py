"""Global constants of the project."""

REGULAR_ALPHABET = [
    chr(c) for c in range(33, 127)
    if chr(c) not in [";", ",", ".", "{", "}", ">", "\\", "_", "'"]
]

DELIMETER = "#"
STARTING_SYMBOL = "\\S"
EMPTY_STRING = "\\E"
FINAL_SYMBOL = "\\!"
