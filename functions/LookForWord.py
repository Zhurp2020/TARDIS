import requests
import bs4
import re
try:
    from functions.WordClass import *
except:
    from WordClass import *


PoSDict = {
    'noun': 'n.',
    'countable noun':'c.n.',
    'uncountable noun':'u.n.',
    'variable noun':'v.n.',
    'verb': 'v.',
    'verb (used with object)': 'v.t.',
    'vt.':'v.t.',
    'verb (used without object)': 'v.i.',
    'vi.':'v.i.',
    'verb (used with or without object)': 'v.',
    'Verb Phrases': 'phrase',
    'adjective': 'adj.',
    'adverb': 'adv.',
    'pronoun': 'pron.',
    'abbreviation': 'abbr.',
    'interjection': 'interj.',
    'conjunction': 'conj.',
    'prepostion': 'prep.',
    'article': 'art.',
    '': ''
}

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
def GetPoSAbbr(PoS):
    try :
        return PoSDict[PoS]
    except :
        return PoS

class NoSuchWord(Exception):
    '''
    未找到，抛出异常
    '''
    pass


class ParserDic_com():
    def __init__(self, target):
        self.target =  target
        self.WordList = []
        self.ExampleList = []
    def GetSoup(self):
        SearchResult = requests.get('https://www.dictionary.com/browse/{}#'.format(self.target)).text
        soup = bs4.BeautifulSoup(SearchResult, features="html.parser")
        self.soup = soup
    def CheckNoResult(self):
        NoResult = self.soup.find(class_='no-results-title css-1w0dr93 e6aw9qa0')
        if NoResult:
            raise NoSuchWord()
    def GetWordList(self):
        WordSectionList = []
        WordNumList = self.soup.find_all(id='luna-section')
        WordSectionList.append(self.soup.find(class_='css-1urpfgu e16867sm0'))
        for WordNumTag in WordNumList:
            WordSectionList.append(WordNumTag.next_sibling)
        return WordSectionList
    def GetSpelling(self, tag):
        spelling = tag.find(class_='css-1jzk4d9 e1rg2mtf8').string
        return spelling
    def GetPhonetic(self, tag):
        phonetic = GetTagString(
            tag.find(class_='pron-ipa-content css-z3mf2 evh0tcl2'))
        return phonetic
    def GetPoSTagList(self, tag):
        PoSList = tag.find_all(class_='css-pnw38j e1hk9ate0')
        return PoSList
    def GetInflect(self, tag):
        inflect = GetTagString(tag.find_all(class_='luna-inflected-form'))
        inflect = [i.replace('·', '').rstrip('.').rstrip(',') for i in inflect]
        return inflect
    def GetPos(self, tag):
        PoS = GetPoSAbbr(GetTagString(tag.find(class_='luna-pos')).rstrip(','))
        return PoS
    def GetDefList(self, tag):
        DefTagList = tag.find_all(class_='e1q3nk1v3')
        return DefTagList
    def GetSpecial(self, tag):
        special = GetTagString(tag.find_all(class_='luna-label'))
        return special
    def GetPhrase(self, tag):
        phrase = GetTagString(tag.find(class_='bold'))
        return phrase
    def GetDefContent(self, tag):
        ContentTag = tag.find_all(class_='e1q3nk1v4')[-1]
        return ContentTag
    def GetContentString(self, tag,example):
        content =''.join( [i for i in tag.strings if i not in example])
        return content
    def GetDefExample(self, tag):
        example = GetTagString(tag.find(class_='luna-example'))
        if example:
            example = [example]
            return example
        else:
            return []
    def GetWordExample(self):
        ExampleTagList = self.soup.find(class_='css-7w6khc e1md2px10').find(
        class_='expandable content-hidden css-14189ta-StatelessExpandableWrapper e1fc5zsj0').find_all(class_='one-click-content css-a8m74p e15kc6du6')
        ExampleList = [''.join(i.strings) for i in ExampleTagList]
        return ExampleList
    def parse(self):
        self.CheckNoResult()
        for WordTag in self.GetWordList():
            DefList = []
            spelling = self.GetSpelling(WordTag)
            phonetic = self.GetPhonetic(WordTag)
            PosList = self.GetPoSTagList(WordTag)
            for PosTag in PosList:
                inflect = self.GetInflect(PosTag)
                PoS = self.GetPos(PosTag)
                DefTagList = self.GetDefList(PosTag)
                for DefTag in DefTagList:
                    special = self.GetSpecial(DefTag)
                    phrase = self.GetPhrase(DefTag)
                    ContentTag = self.GetDefContent(DefTag)
                    example = self.GetDefExample(ContentTag)
                    content = self.GetContentString(ContentTag,example)
                    NewDef = Definition(content=content, PoS=PoS, inflect=inflect,
                                        phrase=phrase, special=special, example=example)
                    DefList.append(NewDef)
            NewWord = Word(spelling=spelling,phonetic=phonetic,definitions=DefList)
            self.WordList.append(NewWord)
        self.ExampleList = self.GetWordExample()
    def GetResult(self):
        self.GetSoup()
        self.parse()
        self.result = [self.WordList,self.ExampleList]
        return self.result



class ParserMer_Web(ParserDic_com):
    def __init__(self, target):
        super().__init__(target)
    def GetSoup(self):
        SearchResult = requests.get('https://www.merriam-webster.com/dictionary/{}'.format(self.target)).text
        self.soup = bs4.BeautifulSoup(SearchResult, features="html.parser")
    def CheckNoResult(self):
        NoResult = self.soup.find(class_='missing-query')
        NoResult2 = self.soup.find(class_='words_fail_us_cont search-results')
        if NoResult or NoResult2:
            raise NoSuchWord
    def GetAllTagList(self):
        AllTagParent = self.soup.find(class_='left-content col-lg-7 col-xl-8')
        AllTagList = [i for i in AllTagParent.children]
        return AllTagList
    def IsWordTag (self,tag):
        try:
            if tag['class'] == ['row','entry-header']:
                return True
        except:
            pass
    def IsPhoneticTag(self,tag):
        try:
            if tag['class'] == ['row','entry-attr']:
                return True
        except:
            pass
    def IsDefAreaTag(self,tag):
        try :
            if 'dictionary-entry' in tag['id']:
                return True
        except:
            pass 
    def IsInflectTag(self,tag):
        try:
            if tag['class'] == ['row','headword-row']:
                return True
        except:
            pass
    def GetSpelling(self,tag):
        spelling = tag.find(class_='hword').string
        return spelling
    def GetPoS(self,tag):
        PoS = GetTagString(tag.find(class_='important-blue-link'))
        PoS = ''.join([i for i in PoS if i.isalpha()])
        PoS = GetPoSAbbr(PoS)
        return PoS
    def GetPhonetic(self,tag):
        phonetic = ''.join([i.strip() for i in tag.find(class_='prs').strings])
        return phonetic
    def GetInflect(self,tag):
        try:
            inflect = [i.strip() for i in tag.find(class_='vg-ins').strings if i.strip() != '' ]
        except:
            return []
        inflect = [i for i in inflect if i != ',' and i != ';']
        for i in range(len(inflect)):
            if inflect[i] != '\\':
                inflect[i] = inflect[i]+' '
            else :
                break
        inflect = ''.join(inflect).split()
        return inflect
    def GetDefList(self,tag):
        DefTagList = tag.find_all(class_='sense')
        return DefTagList
    def GetSpecial(self,tag):
        special = GetTagString(tag.find_all(class_='sl')) 
        return special
    def GetDefContent(self,tag,example):
        TagList = tag.find_all(class_='dtText')
        content = ''
        ExampleText = []
        for i in example:
            for j in i :
                ExampleText.append(j)
        for tag in TagList:
            DefContent = [i for i in tag.strings if not i in ExampleText and i.strip() != ':']
            if content:
                content += ', ' + ' '.join([i.strip() for i in DefContent])
            else:
                content += ' '.join([i.strip() for i in DefContent])
        return content
    def GetDefExample(self,tag):
        ExampleList = tag.find_all(class_='ex-sent')
        example = [[i for i in egtag.strings] for egtag in ExampleList]
        return example
    def GetPhrase(self, tag):
        PhraseTag = tag.find(class_='dro')
        if PhraseTag:
            phrase = [i for i in PhraseTag.strings][0]
            PhraseDef = ''.join([i.strip() for i in PhraseTag.strings if i.strip() != ''][1:])
            phrase = Definition(content=PhraseDef,PoS='phrase',inflect=[],phrase=phrase,special=[],example=[])
            return phrase
    def GetWordExample(self):
        ExampleTag = self.soup.find(id='examples-anchor')
        if not ExampleTag:
            return []
        ExampleTagList = ExampleTag.find_all(class_='ex-sent')
        ExampleList = []
        for tag in ExampleTagList:
            ExampleList.append(' '.join([i.strip() for i in tag.strings]))
        return ExampleList
    def parse(self):
        self.CheckNoResult()
        AllTagList = self.GetAllTagList()
        spelling = phonetic = None
        PoS = ''
        inflect = []
        for tag in AllTagList :
            if self.IsWordTag(tag) :
                spelling = self.GetSpelling(tag)
                PoS = self.GetPoS(tag)
            if self.IsPhoneticTag(tag):
                phonetic = self.GetPhonetic(tag)
            if self.IsInflectTag(tag):
                inflect = self.GetInflect(tag)
            if self.IsDefAreaTag(tag):
                phrase = self.GetPhrase(tag)
                DefinitionList = []
                DefTagList = self.GetDefList(tag)
                for DefTag in DefTagList:
                    special = self.GetSpecial(DefTag)
                    example = self.GetDefExample(DefTag)
                    content = self.GetDefContent(DefTag,example)
                    example = [''.join(i).rstrip() for i in example]
                    if phrase:
                        if  not content in phrase.content:
                            NewDef = Definition(content=content,PoS=PoS,inflect=inflect,phrase='',special=special,example=example)
                            DefinitionList.append(NewDef)
                    else:
                        NewDef = Definition(content=content,PoS=PoS,inflect=inflect,phrase='',special=special,example=example)
                        DefinitionList.append(NewDef)
                if phrase:
                    DefinitionList.append(phrase)
                NewWord = Word(spelling=spelling,phonetic=phonetic,definitions=DefinitionList)
                self.WordList.append(NewWord)
                spelling = phonetic = None
                PoS = ''
                inflect = []
        self.ExampleList = self.GetWordExample()



class ParserColins(ParserDic_com):
    def __init__(self, target):
        super().__init__(target)
    def CheckNoResult(self):
        NoResult = self.soup.find(class_='spellcheck_wrapper')
        if NoResult:
            raise NoSuchWord
    def GetSoup(self):
        header = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }
        SearchResult = requests.get('https://www.collinsdictionary.com/dictionary/english/{}'.format(self.target),headers=header).text
        self.soup = bs4.BeautifulSoup(SearchResult, features="html.parser")
    def GetDictArea(self):
        DictAreaTag = self.soup.find(class_='dictionary Cob_Adv_Brit dictentry')
        return DictAreaTag
    def GetSpelling(self, tag):
        spelling = tag.find(class_='orth').string
        return spelling
    def GetPhonetic(self, tag):
        phonetic = tag.find(class_='pron type-').strings
        phonetic = '/'+''.join([i for i in phonetic if i != '\n'])+'/'
        return phonetic
    def GetInflect(self, tag):
        try:
            InflectTagList = tag.find(class_='form inflected_forms type-infl').find_all(class_='orth')
            inflect = [i.string for i in InflectTagList]
        except:
            inflect = []
        return inflect
    def GetDefList(self, tag):
        DefList = tag.find_all(class_='hom')
        return DefList
    def GetPos(self, tag):
        PoS = GetTagString(tag.find(class_='gramGrp pos')) 
        if not PoS:
            PoS = GetTagString(tag.find(class_='gramGrp').find(class_='pos'))
        PoS = GetPoSAbbr(PoS)
        return PoS
    def GetDefContent(self, tag):
        try:
            DefContentTag = tag.find(class_='def').strings
            content = ''.join([i.replace('\n','') for i in DefContentTag])
            return content
        except:
            DefContentTag = tag.strings
            content = ''.join([i.replace('\n','') for i in DefContentTag][1:])
            return content
    def GetDefExample(self, tag):
        example = []
        ExampleTagList = tag.find_all(class_='cit type-example')
        for ExampleTag in ExampleTagList:
            text = ExampleTag.string
            if text is None :
                text = ExampleTag.find(class_='quote').string
            example.append(text)
        return example
    def GetWordExample(self):
        example = []
        ExampleTagList = self.soup.find(class_='assets').find_all(class_='cit')
        for ExampleTag in ExampleTagList:
            text = ''.join([i.replace('\n','') for i in ExampleTag.find(class_='quote').strings])
            example.append(text)
        return example
    def parse(self):
        self.CheckNoResult()
        DefinitionList = []
        DictAreaTag = self.GetDictArea()
        spelling = self.GetSpelling(DictAreaTag)
        phonetic = self.GetPhonetic(DictAreaTag)
        inflect = self.GetInflect(DictAreaTag)
        DefList = self.GetDefList(DictAreaTag)
        for DefTag in DefList:
            PoS = self.GetPos(DefTag)
            content = self.GetDefContent(DefTag)
            example = self.GetDefExample(DefTag)
            definition = Definition(content=content,PoS=PoS,inflect=inflect,phrase='',special=[],example=example)
            DefinitionList.append(definition)
        word = Word(spelling=spelling,phonetic=phonetic,definitions=DefinitionList)
        self.WordList.append(word)
        self.ExampleList = self.GetWordExample()

class ParserHaici(ParserDic_com):
    def __init__(self, target):
        super().__init__(target)
    def CheckNoResult(self):
        NoResult = self.soup.find(class_='oop')
        if NoResult:
            raise NoSuchWord
    def GetSoup(self):
        text = requests.get('http://dict.cn/{}'.format(self.target)).text
        self.soup = bs4.BeautifulSoup(text,features="html.parser")
    def GetWordTag(self):
        return self.soup.find(class_='word')
    def GetSpelling(self, tag):
        spelling = tag.find(class_='word-cont').find(class_='keyword').string
        return spelling
    def GetPhonetic(self, tag):
        phonetic = tag.find(class_='phonetic').find(lang='EN-US').string
        return phonetic
    def GetDefList(self,tag):
        DefTagList = tag.find(class_='dict-basic-ul').find_all('li')
        return DefTagList
    def GetPos(self, tag):
        pos = GetPoSAbbr(tag.find('span').string) 
        return pos
    def GetDefContent(self, tag):
        return tag.find('strong').string
    def GetInflect(self, tag):
        InflectTagList = tag.find(class_='shape').find_all('a')
        InflectList = [i.string.strip() for i in InflectTagList]
        return InflectList
    def GetWordExample(self):
        ExampleTagList = self.soup.find(class_='section sent').find(class_='layout sort').find_all('li')
        ExampleList = ['\n'.join(list(i.strings)) for i in ExampleTagList]
        return ExampleList
    def parse(self):
        self.CheckNoResult()
        DefList = []
        WordTag = self.GetWordTag()
        spelling = self.GetSpelling(WordTag)
        phonetic = self.GetPhonetic(WordTag)
        DefTagList = self.GetDefList(WordTag)
        inflect = self.GetInflect(WordTag)
        for DefTag in DefTagList[:-1]:
            pos = self.GetPos(DefTag)
            content = self.GetDefContent(DefTag)
            def_ = Definition(content,pos,inflect,phrase='',special=[],example=[])
            DefList.append(def_)
        word = Word(spelling,phonetic,DefList)
        self.WordList.append(word)
        self.ExampleList = self.GetWordExample()

ParserDict = {'dictionary.com': ParserDic_com,
              'Merriam-Webster': ParserMer_Web,
              'colins': ParserColins,
              '海词':ParserHaici
              }

class WordSearcher():
    def __init__(self,target,source):
        self.target = target
        self.source = source
    def SearchWord(self):
        searcher = ParserDict[self.source](self.target)
        self.result = searcher.GetResult()
        return self.result
        
'''
word = 'microscopic'
source = 'Merriam-Webster'
NewWordSearcher = WordSearcher(word,source)
result = NewWordSearcher.SearchWord()

for i in result[0] :
    i.show()
for i in result[1] :
    print(i)
'''