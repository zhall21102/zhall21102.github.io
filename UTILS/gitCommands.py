import git
import os, calendar
cal = {month: index for index, month in enumerate(calendar.month_abbr) if month}
pathName = os.path.dirname(__file__)[:-6]
g = git.Git(pathName) 
def singleMap(file):
    log = g.log('-n 1 --pretty=format:%cd', file).split('\n')[2].split()
    webPath = 'https://zhall21102.github.io/'+file
    log[2] = str(cal[log[2]])
    if len(log[2]) == 1:
        log[2] = '0'+log[2]
    prettyLog = '{}-{}-{}'.format(log[5],log[2],log[3])
    toAdd = f'<url><loc>{webPath}</loc><lastmod>{prettyLog}</lastmod></url>'
    return toAdd

def mapAll():
    clearMap()
    toWrite = ''
    toWrite += singleMap('index.html')
    toWrite += singleMap('Inventory.html')
    
    for file in os.listdir(pathName+'/Pages'):
        if file[-1] == 'l':
            toWrite += singleMap('Pages/'+file)
    f = open(pathName+'/sitemap.xml')
    txt = f.read()
    newTxt = txt.replace('</urlset>', toWrite + '\n</urlset>')
    f.close()
    f = open(pathName + '/sitemap.xml', 'w')
    f.write(newTxt)
    f.close()
    print('Mapping complete')
        
def clearMap():
    f = open(pathName+'/sitemap.xml', 'w')
    f.write('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

</urlset>''')
    f.close()
    

mapAll()

