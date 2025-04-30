import sys
import re
from utility import PointedContents
from analizer import Analyzer

def interpret(source_file : str, args : list):
    try:
        print(source_file)
        analyzer = Analyzer(PointedContents(source_file))
        grammar = analyzer.analyze()
        print(grammar.rules_dict)
        grammar.run(args)
    except Exception as e:
        print(f"An error occured: {e}")

def main():
    source_file, args = sys.argv[1], sys.argv[2:]
    interpret(source_file, args)

if __name__ == "__main__":
    main()

