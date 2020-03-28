import requests
import bs4 as bs4
from WordClass import *

def LookForWordDictionary(word) :
    r = requests.get('https://www.dictionary.com/browse/{}#'.format(word))
    soup = bs4.BeautifulSoup(r.text, features="html.parser")
    return soup

def ParWordDic_com(word) :
    soup = LookForWordDictionary(word)
    Limit = len(soup.find_all(id='luna-section'))+1
    WrodSections = soup.find_all(class_='css-1urpfgu e16867sm0',limit=Limit)
    WordList = []
    for SectionTag in WrodSections:
        PoSList = SectionTag.find_all(class_='css-pnw38j e1hk9ate0')
        DefList = []
        for PosTag in PoSList:
            InflectedList = PosTag.find_all(class_='luna-inflected-form')
            PoS = PosTag.find(class_='luna-pos')
            if PoS:
                PoS = PoS.string.rstrip(',')
            else:
                PoS = ''
            if InflectedList :
                inflect = [i.string.rstrip(',').rstrip('.') for i in InflectedList]
            else :
                inflect = ''
            Defs = PosTag.find_all(class_='e1q3nk1v3')
            for DefTag in Defs:
                special = DefTag.find_all(class_='luna-label')
                phrase = DefTag.find(class_='bold')
                if special:
                    special = [i.string for i in special]
                else:
                    special = ''
                if phrase : 
                    phrase = phrase.string 
                else :
                    phrase = ''
                if phrase or special :
                    ContentTags = DefTag.find_all(class_='e1q3nk1v4')[1:]
                else :
                    ContentTags = DefTag.find_all(class_='e1q3nk1v4')
                for content in ContentTags:
                    DefContent = list(content.strings)[0]
                    example = content.find(class_='luna-example')
                    if example:
                        example = example.string
                    else:
                        example = ''
                    Def = Definition(content=DefContent, PoS=PoS,inflect= inflect,phrase=phrase,
                                    special=special, example=example)
                    DefList.append(Def)
        WordList.append(DefList) 
    return WordList


