class Token:
    def __init__(self, token_class="", lexeme="", line=0, token_id=0, num_position=0):
        self.token_class = token_class
        self.lexeme = lexeme
        self.line = line
        self.token_id = token_id
        self.pos = num_position


def array_pointer(token):
    if token != "Id" or token != "Num":
        print("Error pointer array");
        return -1


def remove_template(str_, char):
    count_chars = 0
    str_output = ""
    len_str = len(str_)
    for i in range(len_str):
        if str_[i] == char:
            count_chars += 1
            if count_chars <= 1:
                str_output += char
        else:
            count_chars = 0
            str_output += str_[i]
    return str_output


def replace_(str_, old, new):
    str2 = ""
    a = 0
    for i in range(len(str_) - len(old) + 2):
        print(str(i))
        for j in range(len(old)):
            print("-- " + str(j))
            if old[j] == str_[i]:
                i += 1
                a += 1
                if a == len(old):
                    str2 += new
            else:
                a = 0
                str2 += str_[i]
                break
    return str2
