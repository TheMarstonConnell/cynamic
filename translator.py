
import sys

symbols = ["->", "{", "}", "(", ")",  "+=", "==", "=", "++", "+", "/", "--", "-", ";", "[", "]", ",", ">", "<"]


def removeKeys(code):


    keys = ['for', 'while']

    for j in keys:

        key = j + ' ('

        dex = code.find('for (')
        if(dex < 0):
            continue
        end = code.find(')', dex)
        code = code[:end] + code[end + 1:]
        code = code[:dex] + key.replace('(', '') + code[dex + len(key):]


    return code



def convert(fileName, tokens):
    code = ""

    blockDepth = 0


    for i in tokens:

        if(i == '{'):
            blockDepth += 1
            code = code[0:-1] + ':\n' + ('    '*blockDepth)
        elif(i == '}'):
            blockDepth -= 1
            code = code + "\n" + ('    '*blockDepth)
        elif(i == ';'):
            code = code + '\n' + ('    '*blockDepth)
        elif(i == '++'):
            code = code + "+= 1"
        elif(i == '--'):
            code = code + "-= 1"
        
        else:
            code = code + i + " " 


    code = code + '\nif(__name__ == "__main__"):\n    main()'

    code = removeKeys(code)

    f = open(fileName + ".py", "w")
    f.write(code)
    f.close()
    print(code)


def getSymbol(text):
    for i in symbols:
        if(text[:len(i)] == i):
            return text[len(i):], i
    
    return text, ""

def getWhiteSpace(text):
    token = ""
    for i in text:
        if(i.isspace()):
            token = token + i
        else:
            return text[len(token):], token.strip()

    return "", ""

def getStringLit(text):
    token = ""
    lit = False
    skip = False

    for i in text:


        if(i == '"'):
            if not skip:
                lit = not lit
            else:
                skip = False
            token = token + '"'
        elif(not lit):
            return text[len(token):], token
        elif(i == '\\'):
            skip = True
            token = token + i
        else:
            token = token + i
        
        

    return text, ""

def getNum(text):
    token = ""
    for i in text:
        if(i.isnumeric()):
            token = token + i
        else:
            return text[len(token):], token
    return "", text

def getID(text):
    token = ""
    for i in text:
        if(i.isalpha()):
            token = token + i
        else:
            return text[len(token):], token
    return "", text

def preprocess(line):
    ret = ""
    inc = '#include'
    if(line[:len(inc)] == inc):
        f = open(line[len(inc):].strip())
        for i in f:
            ret = ret + i + "\n"
    
    return ret

def translate(file):



    code = ""

    f = open(file)
    for i in f:
        if(i.isspace()):
            continue

        if(i.strip()[0]=='#'):  
            code = code + preprocess(i)

        else:
            code = code + i

    tokens = []



    while(len(code) > 0):

        attempt = getID(code)
        code = attempt[0]
        tokens.append(attempt[1])

        attempt = getNum(code)
        code = attempt[0]
        tokens.append(attempt[1])
        
        attempt = getStringLit(code)
        code = attempt[0]
        tokens.append(attempt[1])

        attempt = getWhiteSpace(code)
        code = attempt[0]
        tokens.append(attempt[1])

        attempt = getSymbol(code)
        code = attempt[0]
        if(attempt[1] != ""):
            tokens.append(attempt[1])

        print(code)

    while('' in tokens):
        tokens.remove('')


    print(tokens)

    convert(file[:file.rindex('.')], tokens)


    

def main():

    translate(sys.argv[1]);



if(__name__ == "__main__"):
    main()