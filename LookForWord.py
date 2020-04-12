import requests
import bs4
from WordClass import *


# 来源与用于request的网址
SearcherDict = {'dictionary.com': 'https://www.dictionary.com/browse/{}#'}

class WordSearcher():
    '''
    查找单词，返回相应网页的html代码
    用法：
    NewWordSearcher = WordSearcher('dictionary.com')   
    SearchResult = NewWordSearcher.search('test')
    '''
    
    def __init__(self, target):
        self.target = target

    def search(self, word):
        return requests.get(SearcherDict[self.target].format(word)).text


class NoSuchWord(Exception):
    '''
    未找到，抛出异常
    '''
    pass

def GetTagString(tag):
    '''
    从tag或一个list的tag中拿字符串，如果没有返回空字符串
    '''
    if tag:
        if isinstance(tag, list):
            return [i.string for i in tag]
        else:
            return tag.string
    else:
        return ''


def ParserDic_com(soup):
    NoResult = soup.find(class_='no-results-title css-1w0dr93 e6aw9qa0')
    if NoResult :
        raise NoSuchWord()
    WordList = []
    WordSectionList = []
    WordNumList = soup.find_all(id='luna-section')
    WordSectionList.append(soup.find(class_='css-1urpfgu e16867sm0'))
    for WordNumTag in WordNumList:
        WordSectionList.append(WordNumTag.next_sibling)
    for WordSectionTag in WordSectionList:
        spelling = WordSectionTag.find(class_='css-1jzk4d9 e1rg2mtf8').string
        phonetic = GetTagString(WordSectionTag.find(class_='pron-ipa-content css-z3mf2 evh0tcl2')) 
        PoSList = WordSectionTag.find_all(class_='css-pnw38j e1hk9ate0')
        DefinitionList = []
        for PosTag in PoSList:
            inflect = GetTagString(PosTag.find_all(
                class_='luna-inflected-form'))
            PoS = GetTagString(PosTag.find(class_='luna-pos'))
            DefTagList = PosTag.find_all(class_='e1q3nk1v3')
            for DefTag in DefTagList:
                special = GetTagString(DefTag.find_all(class_='luna-label'))
                phrase = GetTagString(DefTag.find(class_='bold'))
                if phrase or special:
                    ContentTagList = DefTag.find_all(class_='e1q3nk1v4')[1:]
                else:
                    ContentTagList = DefTag.find_all(class_='e1q3nk1v4')
                for ContentTag in ContentTagList:
                    content = list(ContentTag.strings)[0]
                    example = GetTagString(ContentTag.find(class_='luna-example'))
                    Def = Definition(content=content, PoS=PoS, inflect=inflect, phrase=phrase,
                                    special=special, example=example)
                    DefinitionList.append(Def)
        word = Word(spelling=spelling,phonetic=phonetic,definitions=DefinitionList)
        WordList.append(word)
    return WordList


ParserDict = {'dictionary.com': ParserDic_com}


class HTMLParser():
    '''
    HTML解析
    用法：
    NewParser = HTMLParser('dictionary.com')
    WordList = NewParser.parse(SearchResult)
    '''
    def __init__(self, source):
        self.source = source

    def parse(self, HTMLCode):
        soup = bs4.BeautifulSoup(HTMLCode, features="html.parser")
        return ParserDict[self.source](soup)

'''
word = 'tttt'
NewWordSearcher = WordSearcher('dictionary.com')
SearchResult = NewWordSearcher.search(word)
NewParser = HTMLParser('dictionary.com')
try :
    WordList = NewParser.parse(SearchResult)
    for i in WordList:
        i.show()
except NoSuchWord:
    print('No Such Word: {}'.format(word))
'''

