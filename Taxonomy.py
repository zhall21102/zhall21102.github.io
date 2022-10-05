import requests
from bs4 import BeautifulSoup
import random
import time
import wikipedia
import os

dirname = os.path.dirname(__file__)

def call(HREF, titles=[],links=[]):
    response = requests.get(url=HREF,)
    soup = BeautifulSoup(response.content, 'html.parser')
    if 'Kingdom' in str(soup.find_all('table')[0]):
        step1=soup.find_all('table')[0].find_all('tr')
    else:
        step1=soup.find_all('table')[1].find_all('tr')
    step2=[]
    class1=[]
    wanted = ["Kingdom", "Subkingdom", "Phylum", "Division", "Superphylum", \
              "Class", "Order", "Suborder","Infraorder", "Superfamily", \
              "Family", "Subfamily", "Tribe", "Genus", "Species", "Subspecies"]
    for thread in step1:
        for key in wanted:
            if key in str(thread):
                step2.append(thread)
                class1.append(thread.find('td'))
    step3=[]
    class2=[]
    for thread in class1:
        tmp=str(thread)
        end=tmp.find(':')+1
        if tmp[4:tmp.find(':')] in wanted:
            class2.append(tmp[4:tmp.find(':')])
    
    for thread in step2:
        tmp1=str(thread).replace('<i>','').replace('<b>','').replace('\xa0',' ')
        start=tmp1.find('">')
        tmp2=tmp1[start+2:]
        if '">' in tmp2 and '<a' not in tmp2[2:] or '†' in tmp2 or tmp2[0] == '<':
            tmp2=tmp2[tmp2.find('">')+2:]
        end=tmp2.find('<')
        step3.append(tmp2[:end])
        
    dictionary = {}
    for e in range(len(step3)):
        try:
            dictionary[class2[e]]=step3[e]
        except:
            pass
    try:
        del dictionary['']
    except:
        pass
    if dictionary != {}:
        return dictionary
    else:
        return 'Something went wrong!'

    
def compareHelper(a,b):
    levels = ['Subspecies', 'Species', 'Genus', 'Tribe', 'Subfamily',\
              'Family', 'Superfamily', 'Infraorder', 'Suborder', 'Order',\
              'Class', 'Superphylum', 'Phylum', 'Subkingdom', 'Kingdom']
    for level in levels:
        try:
            if a[level] == b[level]:
                return level + ', ' + a[level]
        except:
            pass
    return 'Living Thing'
        
def compare():
    """Find the closest link between two animals"""
    while True:
        title = input('Lifeform A?\n')
        if title == 'quit' or title == 'lookup':
            break
        topic = wikipedia.search(title)[0]
        link='http://en.wikipedia.org/wiki/'+topic
        a = call(link)
        title = input('Lifeform B?\n')
        topic = wikipedia.search(title)[0]
        link='http://en.wikipedia.org/wiki/'+topic
        b = call(link)
        print('Closest link:\n' + compareHelper(a,b) + '\n')
    if title == 'lookup':
            lookup()
        
def lookup():
    """Get the taxonomy of a given animal"""
    while True:
        title = input('What Lifeform?\n')
        if title == 'quit' or title == 'compare':
            break
        topic = wikipedia.search(title)[0]
        link='http://en.wikipedia.org/wiki/'+topic
        PRETTY = True
        end = call(link)
        if PRETTY:
            for entry in end:
                print(entry + ': ' + end[entry])
        print()
    if title == 'compare':
            compare()

def log():
    """Log the input as a webpage"""
    levels = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']
    title = input('What Lifeform?\n> ')
    topic = wikipedia.search(title)[0]
    link='http://en.wikipedia.org/wiki/'+topic
    subject = call(link)
    if subject['Kingdom'] == 'Fungi':
        levels = ['Kingdom', 'Division', 'Class', 'Order', 'Family', 'Genus', 'Species']
    elif subject['Kingdom'] == 'Plantae':
        levels = ['Kingdom', 'Order', 'Family', 'Genus', 'Species']
    for level in range(len(levels)):
        if level != 0:
            try:
                if subject[levels[level]]+'.html' not in os.listdir(dirname+'\Webpage\Pages'):
                    #Write new File
                    readFile = open(dirname+'\Webpage\Pages\Examples\Middle.html', 'r')
                    toWrite = readFile.read()
                    toWrite = toWrite.replace('{NAME}', subject[levels[level]])
                    toWrite = toWrite.replace('{RANK}',levels[level])
                    toWrite = toWrite.replace('{PARENT}', subject[levels[level-1]])
                    readFile.close()
                    f = open(dirname+'\Webpage\Pages\\'+subject[levels[level]]+'.html', 'w')
                    f.write(toWrite)
                    f.close()#End
                    
                    #Update Parent
                    f = open(dirname+'\Webpage\Pages\\'+subject[levels[level-1]]+'.html', 'r')
                    toAdd = '<p style="font-size:3vw;"><a href="{CHILD}.html">{CHILD}</a></p>'.replace('{CHILD}',subject[levels[level]])
                    end=''
                    tmp = f.read().split('<div')
                    end+=(tmp[0]+toAdd+'<div')
                    for thing in range(len(tmp)):
                        if thing !=0:
                            end += tmp[thing]+'<div'
                    f.close()
                    f = open(dirname+'\Webpage\Pages\\'+subject[levels[level-1]]+'.html', 'w')
                    f.write(end[:-4])
                    f.close()
                    print('Added: '+subject[levels[level]])
            except Exception as e:
                print('Something went wrong: '+str(e))
                break
    print()


while __name__ == '__main__':
    log()
