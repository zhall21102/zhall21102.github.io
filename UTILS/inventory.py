import os
dirname = os.path.dirname(__file__)[:-6]
def inventory():
    '''Recompile the inventory'''
    clearInv()
    f = open(dirname+'\\Inventory.html')
    inv = f.read()
    f.close()
    toWrite = ''
    for file in (os.listdir(dirname+'\\Pages')):
        if file[-1] == 'l':
            toWrite+='<p><a href="Pages/{CHILD}.html">{CHILD}</a></p>'.replace('{CHILD}',file[:file.find('.h')])
    start = inv[:inv.find('<div ')]
    end = inv[inv.find('<div '):]
    start += toWrite
    endText = start+(end)
    
    f = open(dirname+'\\Inventory.html','w')
    f.write(endText)
    f.close()




#inventory()

def sortInv():
    '''Sort the inventory'''
    file = open(dirname+'\\Inventory.html')
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
    w = open(dirname+'\\Inventory.html','w')
    w.write(f)
    w.close()
    
def clearInv():
    '''Clear the inventory to a clear template'''
    file = open(dirname+'\\Inventory.html')
    f = file.read()
    file.close()
    
    startIndex = f.find('<p')
    endIndex = f.find('<div')

    body = []
    f = f.replace(f[startIndex:endIndex], ''.join(body))
    w = open(dirname+'\\Inventory.html','w')
    w.write(f)
    w.close()

def checkInv():
    file = open(dirname+'\\Inventory.html')
    f = file.read()
    file.close()
    print(f.count('<a')-1)
    

