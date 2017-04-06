from nltk.stem import WordNetLemmatizer
from sentiwordnet_python_wrapper import SentiWordNetCorpusReader, SentiSynset


def expand_knowledge():
    #creating two word sets where the words will be in lemmatized form
    #one set will have words with positive polarity other will have negative polarity words
    swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
    swn = SentiWordNetCorpusReader(swn_filename)


if __name__ == '__main__':
    #expand list of concepts using the SentiWordNet database
    expand_knowledge()

