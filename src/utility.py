def read_contents(file):
    try:
        with open(file, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("The file was not found!")
    except PermissionError:
        print("Permission denied while trying to read the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

class PointedContents:
    def __init__(self, source_file):
        print(source_file)
        self.contents = read_contents(source_file)
        self.ptr = 0
        self.line_count = 1;

    def getCur(self):
        return self.contents[self.ptr]

    def getAfterCur(self):
        cur_ptr = self.ptr + 1
        while cur_ptr < len(self.contents) and self.contents[cur_ptr].isspace():
            cur_ptr += 1
        return 0 if cur_ptr == len(self.contents) else self.contents[cur_ptr]

    def movePtr(self):
        self.ptr += 1
        while self.ptr < len(self.contents) and self.contents[self.ptr].isspace():
            if self.contents[self.ptr] == "\n":
                self.line_count += 1
            self.ptr += 1

    def getLine(self):
        return self.line_count

class Grammar:
    def __init__(self, rules_dict):
        self.rules_dict = rules_dict

    def makeIteration(self) -> bool:
        for lhs, rhs in self.rules_dict.items():
            if lhs in self.input_string:
                self.input_string = self.input_string.replace(lhs, rhs, 1)
                return True
        return False

    def run(self, args : list):
        self.input_string = "\\S" + ",".join(args) + "\\!"
        while self.makeIteration():
            pass
        self.input_string = self.input_string.replace("\\E", "")
        print(self.input_string)

