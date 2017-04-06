from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import pos_tag
from senticnet4 import *
from nltk.corpus import genesis
from random import sample
import csv
import collections

genesis_ic = wn.ic(genesis, False, 0.0)

def get_mood_tag(this_synset, polarity):
    '''
    Computes closest two mood tags to the input concept using Lin similarity measure. If Lin similarity measure cannot be applied, chooses two random tags within tag constraints.
    '''
    #TODO: Should explore relatedness measure instead of randomly sampling    
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
    This function finds new concepts for SenticNet by finding closest synsets (for 5 semantics) in WordNet to a concept
    '''
    #create two corpora of noun words, one having positive polarity and the other negative polarity
    lmtzr = WordNetLemmatizer()   
    
    #create and write file headers
    f_txt = open('Output/1/new_sentic_concepts_1.txt', 'w')
    f_pos_txt = open('Output/1/new_positive_sentic_concepts_1.txt', 'w')
    f_neg_txt = open('Output/1/new_negative_sentic_concepts_1.txt', 'w')
    f_txt.write('Concept ' + 'MoodTag1 ' + 'MoodTag2 ' + 'Semantic1 ' + 'Semantic2 ' + 'Semantic3 ' + 'Semantic4 ' + 'Semantic5' + '\n\n')
    f_pos_txt.write('Concept ' + 'MoodTag1 ' + 'MoodTag2 ' + 'Semantic1 ' + 'Semantic2 ' + 'Semantic3 ' + 'Semantic4 ' + 'Semantic5' + '\n\n')
    f_neg_txt.write('Concept ' + 'MoodTag1 ' + 'MoodTag2 ' + 'Semantic1 ' + 'Semantic2 ' + 'Semantic3 ' + 'Semantic4 ' + 'Semantic5' + '\n\n')
    csvfile = open('Output/1/new_sentic_concepts_1.csv', 'wb')
    csvfile_pos = open('Output/1/new_positive_sentic_concepts_1.csv', 'wb')
    csvfile_neg = open('Output/1/new_negative_sentic_concepts_1.csv', 'wb')
    f_csv = csv.writer(csvfile, delimiter=',')
    f_pos_csv = csv.writer(csvfile_pos, delimiter=',')
    f_neg_csv = csv.writer(csvfile_neg, delimiter=',')
    f_csv.writerow(['Concept', 'MoodTag1', 'MoodTag2', 'Semantic1', 'Semantic2', 'Semantic3', 'Semantic4', 'Semantic5'])
    f_pos_csv.writerow(['Concept', 'MoodTag1', 'MoodTag2', 'Semantic1', 'Semantic2', 'Semantic3', 'Semantic4', 'Semantic5'])
    f_neg_csv.writerow(['Concept', 'MoodTag1', 'MoodTag2', 'Semantic1', 'Semantic2', 'Semantic3', 'Semantic4', 'Semantic5'])
    
    concept_info = {}
    #stores all words of either polarity
    words = set()    
    #stores all postive words
    pos_words = []
    #stores all negative words
    neg_words = []
    #store positive polarity words intra similarity measure
    pos_word_scores = collections.defaultdict(dict)    
    #store negative polarity words intra similarity measure
    neg_word_scores = collections.defaultdict(dict)  
    
    #iterate over all nouns in wordnet
    #stop when MAX_POS_WORDS postive and MAX_NEG_WORDS negative words are got     
    MAX_POS_WORDS = 100000
    MAX_NEG_WORDS = 100000
    pos_counter = 0   
    neg_counter = 0
    for synset in wn.all_synsets('n'):
        s_synset = swn.senti_synset(synset.name())
        #discard non polar (purely objective) words
        if (s_synset.pos_score() == s_synset.neg_score()):
            continue
        #discard proper nouns
        if (pos_tag([synset.name()])[0][1] == 'NNP' or pos_tag([synset.name()])[0][1] == 'NNPS'):
            continue
        concept_name = str(synset.name()[:-5]).lower()
        lmtz_concept_name = lmtzr.lemmatize(concept_name, synset.pos()) 
        #discard non lemmatized repititions
        if (lmtz_concept_name in words):
            continue
        words.add(lmtz_concept_name)
        #polarity cannot be equal since we have removed purely objective words
        polarity = 'positive' if s_synset.pos_score() > s_synset.neg_score() else 'negative'         
        if (polarity == 'positive' and pos_counter < MAX_POS_WORDS):
            pos_words.append(synset.name())
            pos_counter += 1
        elif (polarity == 'negative' and neg_counter < MAX_NEG_WORDS):
            neg_words.append(synset.name())        
            neg_counter += 1          
        if (pos_counter + neg_counter == MAX_POS_WORDS + MAX_NEG_WORDS):
            break        
     
    #compute Lin similarity measure for all pairs of words in both corpora
    for i in xrange(len(pos_words)):
        for j in xrange(i+1, len(pos_words)): 
            word1 = pos_words[i]
            word2 = pos_words[j]
            score = wn.synset(word1).lin_similarity(wn.synset(word2), genesis_ic)
            pos_word_scores[word1][word2] = score
            pos_word_scores[word2][word1] = score
    for i in xrange(len(neg_words)):
        for j in xrange(i+1, len(neg_words)): 
            word1 = neg_words[i]
            word2 = neg_words[j]
            score = wn.synset(word1).lin_similarity(wn.synset(word2), genesis_ic)
            neg_word_scores[word1][word2] = score
            neg_word_scores[word2][word1] = score            
    
    #create a sorted list of words for each word based on similarity measure
    #add concept_info with appropriate tags
    pos_concept_counter = 0
    neg_concept_counter = 0
    for word in pos_words:
        synset = wn.synset(word)
        s_synset = swn.senti_synset(synset.name())
        concept = str(synset.name()[:-5]).lower() 
        #if we have found a new input concept for SenticNet
        if (concept not in senticnet):
            #flag_length checks if we have 5 semantics
            flag_length = 0
            top_semantics = []
            pos_concept_counter += 1
            #sort all words in same corpus based on similarity measure to this word
            sorted_semantics = sorted(pos_word_scores[word].items(), key=lambda x: x[1], reverse = True)
            #all 5 semantic should have same polarity as the root concept
            for pair in sorted_semantics:
                semantic = swn.senti_synset((str(pair[0]).lower()))
                polarity = 'positive' if semantic.pos_score() > semantic.neg_score() else 'negative'
                if (polarity == 'positive'):
                    top_semantics.append(str(pair[0]).lower())
                if (len(top_semantics) == 5):
                    flag_length = 1              
                    break
            if (flag_length == 0):
                continue             
            #print concept, concept_info[concept]
            #find appropriate tags
            tag1, tag2 = get_mood_tag(synset, 'positive') 
            #add concept to concept_info                  
            lmtz_concept_name = lmtzr.lemmatize(concept, synset.pos())             
            concept_info[concept] = [tag1, tag2] + [lmtzr.lemmatize(str(wn.synset(semantic).name()[:-5]).lower(), wn.synset(semantic).pos()) for semantic in top_semantics]
            f_txt.write(str(lmtz_concept_name) + ' ' + ' '.join([str(item) for item in concept_info[concept]]) + '\n') 
            f_csv.writerow([lmtz_concept_name] + concept_info[concept])                                                           
            f_pos_txt.write(str(lmtz_concept_name) + ' ' + ' '.join([str(item) for item in concept_info[concept]]) + '\n') 
            f_pos_csv.writerow([lmtz_concept_name] + concept_info[concept])             

    for word in neg_words:
        synset = wn.synset(word)
        s_synset = swn.senti_synset(synset.name())
        concept = str(synset.name()[:-5]).lower()     
        #if we have found a new input concept for SenticNet
        if (concept not in senticnet):
            #flag_length checks if we have 5 semantics
            flag_length = 0
            top_semantics = []        
            neg_concept_counter += 1
            #sort all words in same corpus based on similarity measure to this word
            sorted_semantics = sorted(neg_word_scores[word].items(), key=lambda x: x[1], reverse = True)  
            #all 5 semantic should have same polarity as the root concept
            for pair in sorted_semantics:
                semantic = swn.senti_synset((str(pair[0]).lower()))
                polarity = 'positive' if semantic.pos_score() > semantic.neg_score() else 'negative'
                if (polarity == 'negative'):
                    top_semantics.append(str(pair[0]).lower())
                if (len(top_semantics) == 5):
                    flag_length = 1              
                    break
            if (flag_length == 0):
                continue            
            #print concept, concept_info[concept]
            #find appropriate tags
            tag1, tag2 = get_mood_tag(synset, 'negative') 
            #add concept to concept_info                  
            lmtz_concept_name = lmtzr.lemmatize(concept, synset.pos())             
            concept_info[concept] = [tag1, tag2] + [lmtzr.lemmatize(str(wn.synset(semantic).name()[:-5]).lower(), wn.synset(semantic).pos()) for semantic in top_semantics]
            f_txt.write(str(lmtz_concept_name) + ' ' + ' '.join([str(item) for item in concept_info[concept]]) + '\n') 
            f_csv.writerow([lmtz_concept_name] + concept_info[concept])         
            f_neg_txt.write(str(lmtz_concept_name) + ' ' + ' '.join([str(item) for item in concept_info[concept]]) + '\n') 
            f_neg_csv.writerow([lmtz_concept_name] + concept_info[concept])             
    return pos_concept_counter, neg_concept_counter, pos_concept_counter + neg_concept_counter
    
    
if __name__ == '__main__':
    #expand list of concepts by finding new concepts for SenticNet by finding closest synsets (for 5 semantics) in WordNet to a concept
    no_pos, no_neg, total = expand_knowledge()        
    print "Created {} postive concepts + {} negative concepts = {} concepts".format(no_pos, no_neg, total)
