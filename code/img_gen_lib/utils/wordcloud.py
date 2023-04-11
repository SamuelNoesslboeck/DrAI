from gensim.models import Word2Vec
import numpy as np
import nltk

def findSimilar( word : str, topSimilar = 10, randomPerNoun = 1 ):
    model = Word2Vec.load( "./data/word2vec.model" )
    sim = model.wv.most_similar( positive = word, topn = topSimilar )

    found = []
    for i in range( randomPerNoun ):
        found.append( sim[ np.random.randint( 0, len( sim ) ) ] ) 
    return found

def getNouns( lines : str, topNNouns = 3 ):
    is_noun = lambda pos: pos[:2] == 'NN'

    tokenized = nltk.word_tokenize(lines)
    nouns = [ word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos) ] 

    #remove nouns which appear more than once
    fNouns = []
    for n in nouns:
        if n not in fNouns:
            fNouns.append( n )
    return fNouns[ : topNNouns ]


if __name__ == "__main__":
    line = "a drawing of a person with a flower in their hand and a line drawing of a person's head, Derf, intricate concept art, an abstract drawing, abstract expressionism"
    nouns = getNouns( line )   
   
    gesAppendingText = ""
    for n in nouns:
        gesAppendingText += findSimilar( n )[ 0 ][ 0 ] + ", "

    print( gesAppendingText )