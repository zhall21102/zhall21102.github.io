import os
import inventory
dirname = os.path.dirname(__file__)[:-6]
def sortFile(fileName):
    '''sort a single file'''
    file = open(dirname+'\\Pages\\'+fileName)
    f = file.read()
    file.close()
    
    startIndex = f.find('<p')
    endIndex = f.find('<div')

    body = f[startIndex:endIndex]

    body = body.split('<p')
    body = body[1:]
    for e in range(len(body)):
        body[e] = '<p' + body[e]
    body = sorted(body)
    f = f.replace(f[startIndex:endIndex], ''.join(body))
    w = open(dirname+'\\Pages\\'+fileName,'w')
    w.write(f)
    w.close()

def sortKingdoms():
    '''sort the three kingdoms'''
    files = ['Animalia.html', 'Plantae.html', 'Fungi.html']
    for i in files:
        file = open(dirname+'\\Pages\\'+i)
        f = file.read()
        file.close()
        startIndex = f.find('<p')
        endIndex = f.find('<div')

        body = f[startIndex:endIndex]
        body = body.split('<p')
        body = body[1:]
        for e in range(len(body)):
            body[e] = '<p' + body[e]
        body = sorted(body)
        f = f.replace(f[startIndex:endIndex], ''.join(body))
        w = open(dirname+'\\Pages\\'+i,'w')
        w.write(f)
        w.close()
        #print(f)


def sortAll():
    '''sort every file in Pages'''
    sortKingdoms()
    inventory.sortInv()
    for file in os.listdir(dirname+'\\Pages'):
        if file[-1] == 'l':
            sortFile(file)
    print("Sorted!")
    




sortAll()
