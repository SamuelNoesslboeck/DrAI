from gensim.models import Word2Vec
from datasets import load_dataset
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import sklearn.manifold
import numpy as np
import nltk
import tqdm
import re

def preprocess_text(text: str, remove_stopwords: bool) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub("[^A-Za-z]+", " ", text)

    if remove_stopwords:
        tokens = nltk.word_tokenize( text )
        tokens = [ w.lower().strip() for w in tokens if not w.lower() in nltk.corpus.stopwords.words("italian") ]
        return tokens


def reduce_dimensions( model ):
    num_components = 2

    vectors = np.asarray( model.wv.vectors )
    labels = np.asarray( model.wv.index_to_key )  

    tsne = sklearn.manifold.TSNE( n_components = num_components, random_state = 0 ) 
    vectors = tsne.fit_transform( vectors )

    x_vals = [ v[ 0 ] for v in vectors ]
    y_vals = [ v[ 1 ] for v in vectors ] 
    return x_vals, y_vals, labels


def plot_embeddings(x_vals, y_vals, labels):
    fig = go.Figure()
    trace = go.Scatter(x=x_vals, y=y_vals, mode='markers', text=labels)
    fig.add_trace(trace)
    fig.update_layout(title="Word2Vec - Visualizzazione embedding con TSNE")
    plt.show()
    fig.show()


if __name__ == "__main__":
    num_texts = 1_000_000
    vec_size = 128

    nltk.download('stopwords')
    nltk.download('punkt')

    texts = []
    for batch in tqdm.tqdm( load_dataset( "bookcorpus" )[ "train" ] ):
        texts.append( batch[ "text" ] )
        if len( texts ) > num_texts:
            break

    texts = list( map( lambda x: preprocess_text( x, remove_stopwords = True ), texts ) )
    model = Word2Vec( texts, min_count = 1, vector_size = vec_size )
    model.save( "./data/word2vec.model" )

    x_vals, y_vals, labels = reduce_dimensions(model)

    plot = plot_embeddings(x_vals, y_vals, labels)