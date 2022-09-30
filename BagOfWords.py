'''*- using code utf-8 -*'''
import re
import random
import time


'''
Realiza a operação de subtração entre conjuntos de palavras A - B
A: Primeiro conjunto de palavras A
B: Segundo conjunto de palavras B
'''
def differenceSetAB(A, B):
    S = []
    
    for a in A:

        # Palavra não aceita (A-B)
        if a in B: continue

        # Palavra em A
        else: S.append(a)
    
    return S

'''
Realiza a operação de união entre conjuntos de palavras A U B
A: Primeiro conjunto de palavras A
B: Segundo conjunto de palavras B
'''
def unionSetAB(A, B):
    S = {}
    
    for a in A:
        if a not in S: S[a] = 0

    for b in B:
        if b not in S: S[b] = 0
    return S

class Data:
    def __init__(self, fpath):
        self.path = fpath
        self.data = self.__loadData__()
        

    def __loadData__(self):
        if not self.path:
            return None
        
        words = []
        with open(self.path) as fd:
        
            for line in fd:
                # Separa por \n
                lw = re.split('\n', line)

                # Linha vazia
                if not lw:
                    continue

                for currw in lw:
                    
                    # Palavra vazia
                    if not currw:
                        continue
                    else:
                        words.append(currw.lower())
                    
        return words

def preprocess(ds):
    sz = len(ds)
    sz_training = int(round(sz * 0.7))
    sz_teste = sz - sz_training
    training = ds
    test = []

    # Separando dados de teste
    for i in range(sz_teste):
        idx = random.randrange(sz - i)  # Aleatoriedade de tamanho range
        test.append(ds[idx])  # Teste
        del training[idx]  # Treino

    return training, test

def clean_data(dt):
    words = []
    for line in dt:
        # Separa por \n \t , . > < * : ( ) <whitespace>
        lw = re.split('\n|\t|,|\.|\>|\<|\*|\:|\(|\)|\-+| ', line)

        # Linha vazia
        if not lw:
            continue

        for currw in lw:
            
            # Palavra vazia
            if not currw:
                continue
            else:
                words.append(currw.lower())
            
    return words

def clean_test(dt):
    words = []
    test_line = []
    for line in dt:
        # Separa por \n \t , . > < * : ( ) <whitespace>
        lw = re.split('\n|\t|,|\.|\>|\<|\*|\:|\(|\)|\-+| ', line)

        # Linha vazia
        if not lw:
            continue
        words =[]
        for currw in lw:
            
            # Palavra vazia
            if not currw:
                continue
            else:
                words.append(currw.lower())
        test_line.append(words)

    return test_line

class BagOfWord:
    def __init__(self, words, cls):
        
        self.cls = cls
        self.words = words
        self.bag = {}
        self.__init_bag__()

    def __init_bag__(self):
        for word in self.words:
            if word not in self.bag:
                self.bag[word] = int(1)
            else:
                self.bag[word] += 1
                    
        #self.bag = sorted(bag.items(), key = lambda x: x[1])

    # Imprime 100 primeiros
    def printBlock(self):
        for w in self.words[:100]:
            print(w)

    def printBag(self):
        it = 0
        for k,v in self.bag.items():
            if it == 100:
                break
            print(k)
            it += 1


class MultipleBags:
    def __init__(self, words_bag):
        self.words_bag = words_bag 
        self.bags = list(dict())
        self.cls = []
        
    def addBag(self, singlebag):
        b0 = singlebag
        self.cls.append(b0.cls)
        
        bag = {}
        for key in self.words_bag:
            if key not in b0.bag:
                bag[key] = 0
            else:
                bag[key] = b0.bag[key]
                
        self.bags.append(bag)

    def KNN(self, test):
        dist = []

        for i in range(len(self.bags)):
            d = 0
            trained = self.bags[i]
            for key in test:
                if key in trained:
                    d += ((test[key] - trained[key])**2)
            dist.append(d**(1/2))

        idx = min(range(len(dist)), key = lambda x : dist[x])
        return idx


def write(fname, content):
    with open(fname, 'w') as fd:
        for line in content:
            fd.write(line + '\t' + str(content[line]))
            fd.write('\n')

def LOGW(msg):
    path = 'output/log.txt'

    with open(path, 'a') as log:
        log.write('\n' + msg)

if __name__ == '__main__':
    fpath0 = 'talk.politics.misc.txt'
    fpath1 = 'alt.atheism.txt'
    spath = 'NLTK\'s list of english stopwords'
    outpath = 'output/'
    logmsg = []
    
    LOGW('-'*20 + ' Starting Application ' +'-'*20)

    txt0 = Data(fpath0)   # Text
    txt1 = Data(fpath1)   # Text
    stops = Data(spath) # Stop word

    tb = time.process_time()
    tr0, test0 = preprocess(txt0.data) # Division training and test
    tr1, test1 = preprocess(txt1.data)
    ta = time.process_time()
    logmsg.append('Dividing Data in Test/Training: ' +  str(ta-tb) + 's')

    tb = time.process_time()
    tr0 = clean_data(tr0)
    tr1 = clean_data(tr1)
    test0 = clean_test(test0)
    test1 = clean_test(test1)
    ta = time.process_time()
    logmsg.append('Cleaning not words: ' + str(ta-tb) + 's')

    test_bow0 = []
    test_bow1 = []

    # Test BOW
    tb = time.process_time()
    for t in test0:
        test_bow0.append(BagOfWord(t, 0))
        
    for t in test1:
        test_bow1.append(BagOfWord(t, 1))
    ta = time.process_time()
    logmsg.append('Creating test BOW: ' + str(ta-tb) + 's')

    # Removing StopWords from training
    tb = time.process_time()    
    tr0 = differenceSetAB(tr0, stops.data)
    tr1 = differenceSetAB(tr1, stops.data)
    #test0 = differenceSetAB(test0, stops.data)
    #test1 = differenceSetAB(test1, stops.data)
    ta = time.process_time()
    logmsg.append('Removing StopWords: ' + str(ta-tb) + 's')

    # Training BOW
    tb = time.process_time()
    tr_bow0 = BagOfWord(tr0, 0)
    tr_bow1 = BagOfWord(tr1, 1)
    #test_bow0 = BagOfWord(test0, 0)
    #test_bow1 = BagOfWord(test1, 1)
    ta = time.process_time()
    logmsg.append('Creating training BOW: ' + str(ta-tb) + 's')

    # Union Training
    tb = time.process_time()
    words_bag = unionSetAB(tr_bow0.bag, tr_bow1.bag)
    ta = time.process_time()
    logmsg.append('Training Union: ' + str(ta-tb) + 's')

    # Creating Multiple BOW
    tb = time.process_time()
    mb = MultipleBags([key for key in words_bag])
    ta = time.process_time()
    logmsg.append('Creating Multiple BOW: ' + str(ta-tb))

    # Countabilizing MBOW
    tb = time.process_time()
    mb.addBag(tr_bow0)
    mb.addBag(tr_bow1)
    #mb.addBag(test_bow0, False)
    #mb.addBag(test_bow1, False)
    ta = time.process_time()
    logmsg.append('Countablizing MBOW: ' + str(ta-tb) + 's')

    # KNN
    tb = time.process_time()
    err = 0
    tot = 0
    for t in test_bow0:
        predict = mb.KNN(t.bag)
        if predict != 0:
            err += 1
        tot += 1
            
    for t in test_bow1:
        predict = mb.KNN(t.bag)
        if predict != 0:
            err += 1
        tot += 1
    ta = time.process_time()
    logmsg.append('Applying KNN: ' + str(ta-tb) + 's')

    # LOG
    tb = time.process_time()
    write(outpath + 'tr_bag01.txt', mb.bags[0]) # Training BOW1
    write(outpath + 'tr_bag02.txt', mb.bags[1]) # Training BOW2
    ta = time.process_time()
    logmsg.append('Writing outputs: ' + str(ta-tb) + 's')
    
    logmsg.append('KNN accuracy: {0:.2f}'.format(1-(err/tot)))

    for lmsg in logmsg:
        print(lmsg)
        LOGW(lmsg)
