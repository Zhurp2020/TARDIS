class Word(object) :
    def __init__(self,spelling,phonetic=None,definitions=None) :
        self.spelling = spelling
        self.phonetic = phonetic
        self.definitions = definitions 
    def show(self) :
        print(self.spelling,self.phonetic)
        for i in self.definitions :
            i.show()


class Definition(object) :
    def __init__(self,content:str,PoS:str,inflect:list,phrase:str,special:list,example:list) :
        self.content = content
        self.PoS = PoS
        self.inflect = inflect
        self.special = special
        self.example = example
        self.phrase = phrase
    def show(self) :
        if self.PoS :
            print('<{}>'.format(self.PoS),end=' ')
        if self.inflect :
            print('({})'.format(','.join(self.inflect)),end=' ')
        if self.special : 
            for special in self.special :
                print('[{}]'.format(special),end=' ')
        if self.phrase :
            print('[{}]',format(self.phrase),end=' ')
        print(self.content)
        if self.example :
            print('example:',self.example) 
    def get_def(self) :
        result = ''
        if self.PoS :
            result += '<{}>'.format(self.PoS)
        if self.inflect :
            result += '({})'.format(','.join(self.inflect))
        if self.special : 
            for special in self.special :
                result += '[{}]'.format(special) + ' '
        if self.phrase :
            result += '[{}]'.format(self.phrase) + ' '
        result += self.content + '\n'
        if self.example :
            result += 'example: {}'.format(self.example) + '\n'
        return result