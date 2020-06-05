import requests
import bs4
import re
from functions.WordClass import *


# 来源与用于request的网址
SearcherDict = {'dictionary.com': 'https://www.dictionary.com/browse/{}#',
                'Merriam-Webster': 'https://www.merriam-webster.com/dictionary/{}'
                }

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
            return [i.string.rstrip(',') for i in tag]
        else:
            return tag.string.rstrip(',')
    else:
        return ''


PoSDict = {
            'noun':'n.',
            'verb':'v.',
            'verb (used with object)': 'v.t.',
            'verb (used without object)': 'v.i.',
            'verb (used with or without object)':'v.',
            'adjective':'adj.',
            'adverb':'adv.',
            'pronoun':'pron.',
            'abbreviation':'abbr.',
            'interjection': 'interj.',
            'conjunction':'conj.',
            'prepostion':'prep.',
            'article':'art.',
            '':''
            }

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
            PoS = PoSDict[GetTagString(PosTag.find(class_='luna-pos'))] 
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
    ExampleTagList = soup.find(class_='css-7w6khc e1md2px10').find(class_='expandable content-hidden css-14189ta-StatelessExpandableWrapper e1fc5zsj0').find_all(class_='one-click-content css-a8m74p e15kc6du6')
    ExampleList = [''.join(i.strings) for i in ExampleTagList ]
    return [WordList,ExampleList]


def ParserMer_Web(soup) :
    WordList = []
    WordList = []
    DefinitionList = []
    PosParent = soup.find(class_='left-content col-lg-7 col-xl-8')
    PoSList = []
    for PosTag in PosParent.children :
        try :
            if PosTag['class'] == ['row', 'entry-header'] :
                PoSList.append(PosTag)
        except :
            pass
    PoSList = [i.string for i in [j.find(class_='important-blue-link') for j in PoSList]] 
    PoSList = [''.join([j for j in string if j.isalpha()]) for string in PoSList]
    PoSList = [PoSDict[i] for i in PoSList]
    DefAreaList = soup.find_all(id=re.compile(r'dictionary-entry-[0-9]+'))
    inflect = [i for i in soup.find(class_='row headword-row').strings if i.strip() != ';']
    count = 0
    for DefAreaTag in DefAreaList:
        if PoSList[count] != 'verb' :
            inflect = ''
        DefTagList = DefAreaTag.find_all(class_=re.compile(r'sb-[0-9]+'))
        for DefTag in DefTagList:
            DefTextList = DefTag.find_all(class_='dtText')
            special = DefTag.find_all(class_='sd')
            for i in DefTag.find_all(class_='sl') :
                special.append(i)
            special = GetTagString(special)
            for Def in DefTextList:
                ExampleList = Def.find_all(class_='ex-sent')
                example = []
                for i in ExampleList :
                    for j in i.strings:
                        example.append(j)
                DefContent = ''.join([i for i in Def.descendants if isinstance(i,bs4.NavigableString) and not i in example and i.strip() != ':'])
                example = ', '.join([''.join([j for j in i.strings]) for i in ExampleList])
                Def = Definition(content=DefContent, PoS=PoSList[count], inflect=inflect, phrase='',
                                    special=special, example=example)
                DefinitionList.append(Def)
        count += 1
    PhraseList = soup.find_all(class_='dro')             
    for PhraseTag in PhraseList :
        phrase = [i for i in PhraseTag.strings][0]
        PhraseDef = ''.join([i for i in PhraseTag.strings][1:])
        Def = Definition(content=PhraseDef, PoS='phrase', inflect='', phrase=phrase)
        DefinitionList.append(Def)
    spelling = soup.find(class_='hword').string
    phonetic = "\\"+ soup.find(class_='pr').string.strip() + "\\"
    WordList.append(Word(spelling = spelling,phonetic=phonetic, definitions=DefinitionList))
    ExampleTag = soup.find(id='examples-anchor')
    ExampleTagList = ExampleTag.find_all(class_='ex-sent')
    ExampleList = []
    for tag in ExampleTagList:
        ExampleList.append(' '.join([i.strip() for i in tag.strings]))
    return [WordList,ExampleList]
    

ParserDict = {'dictionary.com': ParserDic_com,
            'Merriam-Webster': ParserMer_Web
            }


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
word = 'search'
NewWordSearcher = WordSearcher('Merriam-Webster')
SearchResult = NewWordSearcher.search(word)
NewParser = HTMLParser('Merriam-Webster')
try :
    result = NewParser.parse(SearchResult)
    for i in result[0]:
        i.show()
    for j in result[1] :
        print(j)
except NoSuchWord:
    print('No Such Word: {}'.format(word))
'''

