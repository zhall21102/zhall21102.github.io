import os
import inventory
dirname = os.path.dirname(__file__)[:-6]
def removeLink(parent, toRemove):
    '''Remove the link to a page from another page'''
    if parent != 'inventory':
        try:
            file = open(dirname+'\\Pages\\'+parent)
        except:
            return
    else:
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
    for e in body:
        if toRemove in e:
            body.remove(e)
    f = f.replace(f[startIndex:endIndex], ''.join(body))
    if parent != 'inventory':
        w = open(dirname+'\\Pages\\'+parent, 'w')
    else:
        w = open(dirname+'\\Inventory.html', 'w')
    
    w.write(f)
    w.close()

def removeFile(toRemove):
    '''Remove a file and remove the link from the parent and inventory'''
    f = open(dirname+'\\Pages\\'+toRemove)
    curText = f.read()
    f.close()
    parent = curText[curText.find('within')+7:]
    parent = parent[:parent.find('<')]+'.html'
    removeLink(parent,toRemove)
    removeLink('inventory',toRemove)
    os.remove(dirname+'\\Pages\\'+toRemove)
    
