from nltk.stem import WordNetLemmatizer
from sentiwordnet_python_wrapper import SentiWordNetCorpusReader, SentiSynset
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from senticnet4 import *


#to convert from treebank tag set to wordnet tag set
def get_wordnet_pos(treebank_tag):
    '''
    This function was taken from: http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
    '''
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        #assume pos is NOUN
        return wn.NOUN
        

def get_mood_tag(word, polarity):
    positive_tags = ['joy', 'interest', 'surprise', 'admiration']
    negative_tags = ['sadness', 'fear', 'anger', 'disgust']
    if (polarity == 'positive'):
        tags = sorted(positive_tags, key = lambda tag: wn.wup_similarity(wn.synset(word+'.n.01'), wn.synset(tag+'.n.01')), reverse=True)
        #don't use interesting and surprising together as tags
        if ((tags[0] == 'interesting' and tags[1] == 'surprising') or (tags[0] == 'surprising' and tags[1] == 'interesting')):
            return tags[0], tags[2]
        else:
            return tags[0], tags[1]
    else:   
        tags = sorted(negative_tags, key = lambda tag: wn.wup_similarity(wn.synset(word+'.n.01'), wn.synset(tag+'.n.01')), reverse=True)
        #don't use scared and angry together as tags
        if ((tags[0] == 'scared' and tags[1] == 'angry') or (tags[0] == 'angry' and tags[1] == 'scared')):
            return tags[0], tags[2]   
        else:
            return tags[0], tags[1]                    


def expand_knowledge():  
    '''
    TODO: check if semantics have same polarity
    '''
    f = open('new_sentic_concepts.txt', 'w')
    lmtzr = WordNetLemmatizer()   
    swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
    swn = SentiWordNetCorpusReader(swn_filename)
    concepts = {}
    no = 0
    for senti_synset in swn.all_senti_synsets():
        print senti_synset.synset.name()
        word = str(senti_synset.synset.name()[:-5]).lower()
        pos = senti_synset.synset.name()[-4]
        #keep nouns but remove proper nouns (NN and NNP in Penn Treebank Project)
        #print 'word', word
        if (pos != 'n' or pos_tag([word])[0][1] == 'NNP' or pos_tag([word])[0][1] == 'NNPS'):
            continue
        lemm_word = lmtzr.lemmatize(word, get_wordnet_pos(pos_tag([word])[0][1]))
        if (lemm_word in concepts):
            continue
        pos_score = senti_synset.pos_score
        neg_score = senti_synset.neg_score
        #ignore non sentiment words
        if (pos_score == neg_score):
            continue
        polarity = 'positive' if pos_score >= neg_score else 'negative'
        semantics = set()
        for syn in wn.synsets(word):        
            for lemma in syn.lemmas():  
                lemma_temp = str(lemma)[7:].split('.')
                lemma_temp = '.'.join(lemma_temp[:-1])
                print lemma_temp
                lemma_new = swn.senti_synset(lemma_temp)
                pos_score = lemma_new.pos_score                
                neg_score =  lemma_new.neg_score
                if (pos_score == neg_score):
                    continue                
                
                #swn.senti_synset()
                #print lemma, lemma.name()
                lemma_name = str(lemma.name()).lower()
                pos = lemma.synset().pos()
                if (lemma.synset().pos() != 'n' or pos_tag([lemma_name])[0][1] == 'NNP' or pos_tag([lemma_name])[0][1] == 'NNPS'):
                    continue
                else:
                    semantics.add(lemma_name)
        semantics = sorted(semantics, key = lambda semantic: wn.wup_similarity(wn.synset(word+'.n.01'), wn.synset(semantic+'.n.01')), reverse=True)                    
        final_semantics = [word]
        for semantic in semantics:
            lemm_semantic = lmtzr.lemmatize(semantic, get_wordnet_pos(pos_tag([semantic])[0][1]))
            if (lemm_semantic not in final_semantics):
                final_semantics.append(lemm_semantic)
        final_semantics.remove(word)
        if (len(final_semantics) < 5):
            continue
        else:
            #compute best mood tags
            tag1, tag2 = get_mood_tag(word, polarity)           
            concepts[lemm_word] = [tag1, tag2] + [semantic for semantic in final_semantics[0:5]]            
            #if we have found a new input concept for SenticNet
            if (word not in senticnet):
                print word, concepts[lemm_word]
                f.write(str(word) + ' ' + ' '.join([str(item) for item in concepts[word]]) + '\n') 
                no += 1
                print no
        break
        
            
if __name__ == '__main__':
    #expand list of concepts using lemmas from WordNet
    expand_knowledge()
