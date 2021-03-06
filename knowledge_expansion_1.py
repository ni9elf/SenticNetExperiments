from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import pos_tag
from nltk.corpus import wordnet_ic
from senticnet4 import *
from nltk.corpus import genesis
from random import sample
import csv

genesis_ic = wn.ic(genesis, False, 0.0)

def get_mood_tag(this_synset, polarity):
    '''
    Computes closest two mood tags to the input concept using Lin's similarity measure. If Lin similarity measure cannot be applied, chooses two random tags within tag constraints.
    '''
    #TODO: Should explore other relatedness measure instead of randomly sampling  
    #since similarity measure will work only for words having same pos, we have to form tags in different pos version to compute similarity
    #if pos is a noun
    #print this_synset.pos()
    if (this_synset.pos() == 'n'):
        positive_tags = ['joy.n.01', 'interest.n.01', 'surprise.n.01', 'admirability.n.01']
        negative_tags = ['sadness.n.01', 'fear.n.01', 'anger.n.01', 'disgust.n.01']
    #if pos is a verb
    elif (this_synset.pos() == 'v'):
        positive_tags = ['rejoice.v.01', 'interest.v.01', 'surprise.v.01', 'admire.v.01']
        negative_tags = ['sadden.v.01', 'fear.v.01', 'anger.v.01', 'disgust.v.01']        
    #if pos is an adjective
    elif (this_synset.pos() == 'a'):
        positive_tags = ['joyful.a.01', 'interesting.a.01', 'surprising.a.01', 'impressive.a.01']
        negative_tags = ['sad.a.01', 'alarming.a.01', 'angry.a.01', 'unsavory.a.01']        
    #if pos is an adverb
    elif (this_synset.pos() == 'r'):
        positive_tags = ['gleefully.r.01', 'curiously.r.01', 'amazingly.r.01', 'admirably.r.01']
        negative_tags = ['sadly.r.01', 'fearfully.r.01', 'angrily.r.01', 'disgustingly.r.01'] 
    #creating a standard tag dictionary for uniformity in tag names
    positive_tags_standard = ['joyful', 'interesting', 'surprising', 'admirable']
    negative_tags_standard = ['sad', 'scared', 'angry', 'disgusting']
    tag_to_name = {}
    for i in xrange(len(positive_tags)):
        tag_to_name[positive_tags[i]] = positive_tags_standard[i]
    for i in xrange(len(negative_tags)):
        tag_to_name[negative_tags[i]] = negative_tags_standard[i]        
    
    if (polarity == 'positive'):
        #if similarity measures are not returning a value
        if (sum([this_synset.lin_similarity(wn.synset(tag), genesis_ic) for tag in positive_tags]) == 0):
            #choose tags randomly - baseline performance
            #randomly sampling 3 elements in case of future conflict (interesting - surprising)
            tags = sample(positive_tags, 3)            
        else:
            tags = sorted(positive_tags, key = lambda tag: this_synset.lin_similarity(wn.synset(tag), genesis_ic), reverse=True)
        #don't use interesting and surprising together as tags
        if ((tag_to_name[tags[0]] == 'interesting' and tag_to_name[tags[1]] == 'surprising') or (tag_to_name[tags[0]] == 'surprising' and tag_to_name[tags[1]] == 'interesting')):
            return tag_to_name[tags[0]], tag_to_name[tags[2]]
        else:
            return tag_to_name[tags[0]], tag_to_name[tags[1]]
    else:   
        if (sum([this_synset.lin_similarity(wn.synset(tag), genesis_ic) for tag in negative_tags]) == 0):
            #choose tags randomly - baseline performance
            #randomly sampling 3 elements in case of future conflict (interesting - surprising)
            tags = sample(negative_tags, 3) 
        else:    
            tags = sorted(negative_tags, key = lambda tag: this_synset.lin_similarity(wn.synset(tag), genesis_ic), reverse=True)
        #don't use scared and angry together as tags
        if ((tag_to_name[tags[0]] == 'scared' and tag_to_name[tags[1]] == 'angry') or (tag_to_name[tags[0]] == 'angry' and tag_to_name[tags[1]] == 'scared')):
            return tag_to_name[tags[0]], tag_to_name[tags[2]]  
        else:
            return tag_to_name[tags[0]], tag_to_name[tags[1]]   
            
            
def expand_knowledge():  
    '''
    This function finds new concepts for SenticNet using lemmas from SentiWordNet
    '''
    lmtzr = WordNetLemmatizer()   
    #create and write file headers
    f_txt = open('Output/1/new_sentic_concepts_2.txt', 'w')
    f_pos_txt = open('Output/1/new_positive_sentic_concepts_2.txt', 'w')
    f_neg_txt = open('Output/1/new_negative_sentic_concepts_2.txt', 'w')
    f_txt.write('Concept ' + 'MoodTag1 ' + 'MoodTag2 ' + 'Semantic1 ' + 'Semantic2 ' + 'Semantic3 ' + 'Semantic4 ' + 'Semantic5' + '\n\n')
    f_pos_txt.write('Concept ' + 'MoodTag1 ' + 'MoodTag2 ' + 'Semantic1 ' + 'Semantic2 ' + 'Semantic3 ' + 'Semantic4 ' + 'Semantic5' + '\n\n')
    f_neg_txt.write('Concept ' + 'MoodTag1 ' + 'MoodTag2 ' + 'Semantic1 ' + 'Semantic2 ' + 'Semantic3 ' + 'Semantic4 ' + 'Semantic5' + '\n\n')
    csvfile = open('Output/1/new_sentic_concepts_2.csv', 'wb')
    csvfile_pos = open('Output/1/new_positive_sentic_concepts_2.csv', 'wb')
    csvfile_neg = open('Output/1/new_negative_sentic_concepts_2.csv', 'wb')
    f_csv = csv.writer(csvfile, delimiter=',')
    f_pos_csv = csv.writer(csvfile_pos, delimiter=',')
    f_neg_csv = csv.writer(csvfile_neg, delimiter=',')
    f_csv.writerow(['Concept', 'MoodTag1', 'MoodTag2', 'Semantic1', 'Semantic2', 'Semantic3', 'Semantic4', 'Semantic5'])
    f_pos_csv.writerow(['Concept', 'MoodTag1', 'MoodTag2', 'Semantic1', 'Semantic2', 'Semantic3', 'Semantic4', 'Semantic5'])
    f_neg_csv.writerow(['Concept', 'MoodTag1', 'MoodTag2', 'Semantic1', 'Semantic2', 'Semantic3', 'Semantic4', 'Semantic5'])
    
    concept_info = {}
    #iterate over all words in wordnet
    #i = 0
    pos_concept_counter = 0
    neg_concept_counter = 0
    for synset in wn.all_synsets():
        semantics = []
        #print synset.name()
        #print type(synset.name())
        #obtain sentiment scores of word by forming a SentiWordNet object
        s_synset = swn.senti_synset(synset.name())
        #print s_synset        
        #discard satellite adjective words since we cannot compute Lin similarity measure over this pos group for obtaining closest tags (for now)
        if (synset.pos() == 's'):
            continue
        #discard non polar (purely objective) words
        if (s_synset.pos_score() == s_synset.neg_score()):
            continue
        #discard proper nouns
        if (pos_tag([synset.name()])[0][1] == 'NNP' or pos_tag([synset.name()])[0][1] == 'NNPS'):
            continue
        #print synset.pos()        
        #collect lemmas of concept as semantics
        #assuming all lemmas will have same polarity as input concept
        #can't check for polarity for lemmas as lemmas > synsets and not half of them are not present in SentiWordNet
        #storing lemmatized versions of words               
        concept_name = str(synset.name()[:-5]).lower()
        lmtz_concept_name = lmtzr.lemmatize(concept_name, synset.pos()) 
        for lemma in wn.synset(synset.name()).lemmas():
            #discard input concept name itself
            lemma_name = str(lemma.name()).lower()
            lmtz_lemma_name = lmtzr.lemmatize(lemma_name, lemma.synset().pos())
            if (lmtz_lemma_name == lmtz_concept_name):
                #print lemma.name()
                continue
            #discard proper nouns
            if (pos_tag([lemma.name()])[0][1] == 'NNP' or pos_tag([lemma.name()])[0][1] == 'NNPS'):
                continue
            semantics.append(lemma.name())  
        #if we have atleast 5 semantics for a concept     
        if (len(semantics) >= 5):                      
            concept = str(synset.name()[:-5]).lower()            
            #if we have found a new input concept for SenticNet
            if (concept not in senticnet):
                #polarity cannot be equal since we have removed purely objective words
                polarity = 'positive' if s_synset.pos_score() > s_synset.neg_score() else 'negative'              
                #print concept, concept_info[concept]
                #find appropriate tags
                tag1, tag2 = get_mood_tag(synset, polarity) 
                #add concept to concept_info                    
                concept_info[concept] = [tag1, tag2] + [str(semantic).lower() for semantic in semantics[0:5]]
                f_txt.write(str(concept) + ' ' + ' '.join([str(item) for item in concept_info[concept]]) + '\n') 
                f_csv.writerow([concept] + concept_info[concept])
                if (polarity == 'positive'):
                    pos_concept_counter += 1
                    f_pos_txt.write(str(concept) + ' ' + ' '.join([str(item) for item in concept_info[concept]]) + '\n') 
                    f_pos_csv.writerow([concept] + concept_info[concept])                    
                else: 
                    neg_concept_counter += 1
                    f_neg_txt.write(str(concept) + ' ' + ' '.join([str(item) for item in concept_info[concept]]) + '\n') 
                    f_neg_csv.writerow([concept] + concept_info[concept])                    
                #i += 1
                #print i                          
    return pos_concept_counter, neg_concept_counter, pos_concept_counter + neg_concept_counter


if __name__ == '__main__':
    #expand list of concepts using lemmas from WordNet
    no_pos, no_neg, total = expand_knowledge()        
    print "Created {} postive concepts + {} negative concepts = {} concepts".format(no_pos, no_neg, total)
