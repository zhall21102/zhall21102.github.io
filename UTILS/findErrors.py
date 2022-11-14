import os
import removeFile
dirname = os.path.dirname(__file__)[:-6]
def findErrors():
    '''Find simple errors relatively quickly'''
    errors = []
    for file in (os.listdir(dirname+'\\Pages')):
        if not file[0].isupper():
            errors.append([file, ' Non-capital first'])
            continue
        for letter in file:
            if letter.isupper() and letter is not file[0]:
                errors.append([file, ' Capital outside of first'])
                break
            if(letter not in ' .-' and not letter.isalpha()):
                errors.append([file, 'Non-alpha outside of .-'])
                break
    return errors


def printErrors():
    '''print errors from findErrors'''
    errors = findErrors()
    if len(errors) > 0:
        for error in errors:
            print(error[0],error[1])
    else:
        print("All set!")
    


def unreachable():
    '''Find pages that can not be reached by any link'''
    errors = []
    for file in (os.listdir(dirname+'\\Pages')):
        if file[-1] == 'l':
            f = open(dirname+'\\Pages\\'+file)
            curText = f.read()
            f.close()
            parent = curText[curText.find('within')+7:]
            parent = parent[:parent.find('<')]
            try:
                f = open(dirname+'\\Pages\\'+parent+'.html')
                parText = f.read()
                f.close()

                if file not in parText:
                    if file != 'Animalia.html' and file != 'Fungi.html' and file != 'Plantae.html':
                        errors.append([file, ' Unreachable'])
            except:
                if file != 'Animalia.html' and file != 'Fungi.html' and file != 'Plantae.html':
                    errors.append([file, ' Can\'t open parent'])
    return errors
            

def printUnreachable():
    '''print errors from unreachable'''
    errors = unreachable()
    if len(errors) > 0:
        for error in errors:
            print(error[0],error[1])
    else:
        print("All set!")

def fixUnreachable():
    '''Naively fix unreachable by appending the file to its alleged parent'''
    errors = unreachable()
    if len(errors) > 0:
        for error in errors:
            error = error[0]
            f = open(dirname+'\\Pages\\'+error)
            curText = f.read()
            f.close()
            parent = curText[curText.find('within')+7:]
            parent = parent[:parent.find('<')]
            try:
                f = open(dirname+'\\Pages\\'+parent+'.html')
                parText = f.read()
                f.close()
                start = parText[:parText.find('<div ')]
                end = parText[parText.find('<div '):]
                start+='<p style="font-size:3vw;"><a href="{CHILD}.html">{CHILD}</a></p>'.replace('{CHILD}',error[:error.find('.h')])
                endText = start+(end)
                f = open(dirname+'\\Pages\\'+parent+'.html','w')
                f.write(endText)
                f.close()
                         
            except:
                pass
    else:
        print("All set!")
        

def deepSearch():
    '''Read each file and find more complex errors relatively slowly'''
    errors = []
    for file in (os.listdir(dirname+'\\Pages')):
        if file[-1] == 'l':
            f = open(dirname+'\\Pages\\'+file)
            text = f.read()
            f.close()
            startIndex = text.find('<p')
            endIndex = text.find('<div')

            body = text[startIndex+1:endIndex]
            secondIndex = body.find('<p')
            body = body[secondIndex:]
            if "Species" in text:
                if not (file[2] == ' ' and file[1] == '.' and file[0].isupper()):
                    errors.append([file, ' Mislabeled species'])
                if '<a' in body:
                    errors.append([file, ' Link in species'])
                if ' ' in file[3:-5] or '.' in file[3:-5]:
                    errors.append([file, ' Incorrect spacing and period'])
                parent = text[text.find('within')+7:]
                parent = parent[:parent.find('<')]
                if parent[0] != file[0]:
                    errors.append([file, ' Binomial != Genus'])
            else:
                if ' ' in file or '-' in file or '.' in file[:-5]:
                    errors.append([file, ' Non-alpha in non-species'])
    return errors

def deadLinks():
    '''Find links that do not lead to any pages'''
    errors = []
    for file in (os.listdir(dirname+'\\Pages')):
        if file[-1] == 'l':
            f = open(dirname+'\\Pages\\'+file)
            text = f.read()
            f.close()
        if ' ' in file:
            continue
        startIndex = text.find('<p')
        endIndex = text.find('<div')
        body = text[startIndex:endIndex]
        body = body.split('<p')
        body = body[1:]
        for e in range(len(body)):
            body[e] = '<p' + body[e]
        for e in range(len(body)):
            try:
                body[e] = body[e][body[e].index('f="')+3:]
                body[e] = body[e][:body[e].index('"')]
            except:
                pass
        for e in body:
            try:
                f = open(dirname+'\\Pages\\'+e)
                f.close()
            except:
                errors.append([file,e])
    return errors

def deadInventory():
    '''deadLinks for Inventory.html'''
    errors = []
    f = open(dirname+'\\Inventory.html')
    text = f.read()
    f.close()
    startIndex = text.find('<p')
    endIndex = text.find('<div')
    body = text[startIndex:endIndex]
    body = body.split('<p')
    body = body[1:]
    for e in range(len(body)):
        body[e] = '<p' + body[e]
    for e in range(len(body)):
        try:
            body[e] = body[e][body[e].index('s/')+2:]
            body[e] = body[e][:body[e].index('"')]
        except:
            pass
    for e in body:
        try:
            f = open(dirname+'\\Pages\\'+e)
            f.close()
        except:
            errors.append(['Inventory.html',e])
    return errors

    
def printDead():
    '''print errors from deadLinks'''
    errors = deadLinks()
    errors += deadInventory()
    if len(errors) > 0:
        for e in errors:
            print(e[0],e[1])
    else:
        print('No dead links')


def printDeep():
    '''print errors from deepSearch'''
    errors = deepSearch()
    if len(errors) > 0:
        for error in errors:
            print(error[0],error[1])
    else:
        print("All set!")

def printAll():
    '''print errors from all excluding deadLinks'''
    errors = []
    printList = []
    for error in findErrors():
        if error[0] not in errors:
            errors.append(error[0])
            printList.append(error)
    for error in deepSearch():
        if error[0] not in errors:
            errors.append(error[0])
            printList.append(error)
    for error in unreachable():
        if error[0] not in errors:
            errors.append(error[0])
            printList.append(error)
    if len(printList) > 0:
        for error in printList:
            print(error[0],error[1])
    else:
        print("No errors")

def removeErrors():
    '''Delete trace of any error found except deadLinks'''
    errors = []
    for error in findErrors():
        if error[0] not in errors:
            errors.append(error[0])
    for error in deepSearch():
        if error[0] not in errors:
            errors.append(error[0])
    for error in unreachable():
        if error[0] not in errors:
            errors.append(error[0])
    for error in errors:
        removeFile.removeFile(error)

printDead()
print()
printAll()
cont = input("Remove errors? Y/N\n")
while cont.lower() != 'n':
    removeErrors()
    printAll()
    cont = input("Remove errors? Y/N\n")

