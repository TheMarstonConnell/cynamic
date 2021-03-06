
import sys
import os

replacements = {':':'in', 'function':'def', "!":"not", "&&":"and", "||":"or"}



symbols = [":", "{", "}", "(", ")",  "+=", "==", "=", "++", "+", "/", "--", "-", ";", "[", "]", ",", "<=", ">=", ">", "<", "'", ".", "!=", "!", "&&", "||", "%"]


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



def convert(fileName, tokens, location):
    code = ""


    blockDepth = 0


    for tok in tokens:

        i = tok
        if i in replacements:
            i = replacements[i]

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

    preface = ""
    p = open(location + "\\system.py")
    for i in p:
        preface = preface + i + "\n"

    code = preface + "\n" + code

    f = open(fileName + ".cy", "w")
    f.write(code)
    f.close()
    

    #os.system('python3 -OO -m py_compile ' + fileName + '.py')


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

def getCharLit(text):
    token = ""
    lit = False

    for i in text:


        if(i == "'"):
            lit = not lit
            token = token + "'"
        elif(not lit):
            return text[len(token):], token
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

def preprocess(file, line):
    ret = ""
    inc = '#include'
    define = '#define'

    if(line[:len(inc)] == inc):

        newLine = line[len(inc):].strip()

        if(newLine[0] == '<'):
            return "import " + newLine[1:-1] + ";\n"

        path = os.path.abspath(file)
        path = path[:path.rindex('/')]
        toImp = newLine
        
        while(toImp[0] == '.'):
            path = path[:path.rindex('/')]
            toImp = toImp[1:]

        if(toImp[0] != '/'):
            toImp = '/' + toImp

        newFile = path + toImp + '.pyc'

        f = open(newFile)
        for i in f:
            ret = ret + i + "\n"
    elif(line[:len(define)] == define):
        newLine = line[len(inc):].strip()
        token = newLine[:newLine.find(' ')]
        definer = newLine[newLine.find(' ') + 1:].strip()
        replacements[token] = definer
    return ret

def translate(file, location):



    code = "" 

    f = open(file)
    for i in f:
        if(i.isspace()):
            continue

        if(i.strip()[0]=='#'):  
            code = code + preprocess(file, i) + "\n"

        else:
            code = code + i

    tokens = []

    

    while(len(code) > 0):
        before = code

        attempt = getID(code)
        code = attempt[0]
        tokens.append(attempt[1])

        attempt = getNum(code)
        code = attempt[0]
        tokens.append(attempt[1])
        
        attempt = getStringLit(code)
        code = attempt[0]
        tokens.append(attempt[1])

        attempt = getCharLit(code)
        code = attempt[0]
        tokens.append(attempt[1])

        attempt = getWhiteSpace(code)
        code = attempt[0]
        tokens.append(attempt[1])

        attempt = getSymbol(code)
        code = attempt[0]
        if(attempt[1] != ""):
            tokens.append(attempt[1])

        if(before == code):
            print(tokens)
            error = "Failed compile at: "
            print(error + code[:20].replace('\n', ' '))
            print("~"*len(error) + '^')
            return
    while('' in tokens):
        tokens.remove('')



    convert(file[:file.rindex('.')], tokens, location)


    

def main():

    location = os.path.dirname(os.path.abspath(__file__))
    


    if(len(sys.argv) > 1):
    	translate(sys.argv[1], location);
    else:
        print("Cannot run without file specified.")



if(__name__ == "__main__"):
    main()