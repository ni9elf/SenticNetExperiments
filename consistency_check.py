from senticnet4 import *
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet as swn

#to convert from treebank tag set to wordnet tag set
def get_wordnet_pos(treebank_tag):
    '''
    This function was taken from: http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
    '''
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        #assume pos is NOUN
        return wordnet.NOUN
        
        
def checks_intra():
    '''
    Runs following consistency checks within senticnet:
    1) Checks if the set of semantics of a concept are defined concepts themselves in sentic net
    2) Checks for concepts having duplicate tags
    3) Checks for negative intensity for positive polarity concepts and positive intensity for negative polarity concepts
    4) Checks for the 5 semantics of a concept having the same polarity as the concept
    5) Checks for interest-surprise or fear-anger used together in tags of a concept
    6) Checks if concepts and their related semantics are lemmatized according to wordnet's morphy function called by NLTK
    '''
    not_defined_semantics = set()
    duplicate_tag_concepts = set()
    polarity_intensity_mismatch_concepts = set()
    semantic_concept_polarity_mismatch = set()
    violated_tag_constraint_concepts = set()
    unlemmatized_concepts = set()
    #reading from file 'senticnet4.txt' for a list of concepts to iterate over
    with open('senticnet4.txt', 'r') as f:
        for line in f:            
            line = line.strip().split('\t')
            concept = line[0]
            polarity = line[1]
            intensity = line[2]
                        
            concept_info = senticnet[concept]
            #the 5 semantics of a concept are present in list concept_info[8:13]
            for semantic in concept_info[8:13]:
                #if a semantic is not defined as a concept
                if (semantic not in senticnet):
                    not_defined_semantics.add(semantic)
            
            #checking for duplicate tags
            #checks if tag1 == tag2
            if (concept_info[4] == concept_info[5]):
                duplicate_tag_concepts.add(concept)            
            
            #checking for negative intensity for positive polarity concepts and positive intensity for negative polarity concepts
            if (concept_info[6] == 'positive' and float(concept_info[7]) < 0):
                polarity_intensity_mismatch_concepts.add(concept)
            if (concept_info[6] == 'negative' and float(concept_info[7]) > 0):
                polarity_intensity_mismatch_concepts.add(concept)
            
            #checking if the 5 semantics of a concept have the same polarity as the concept
            for semantic in concept_info[8:13]:
                #if a semantic is not defined as a concept
                if (semantic in senticnet):
                    semantic_polarity = senticnet[semantic][6]
                    #if semantic has does not have polarity as concept
                    if (semantic_polarity != concept_info[6]):
                        print concept, semantic
                        semantic_concept_polarity_mismatch.add((concept, semantic))
                        break

            #checking for interest-surprise or fear-anger used together in tags of a concept
            if ((concept_info[4] == 'interest' and concept_info[5] == 'surprise') or (concept_info[4] == 'surprise' and concept_info[5] == 'interest') or (concept_info[4] == 'fear' and concept_info[5] == 'anger') or (concept_info[4] == 'anger' and concept_info[5] == 'fear')):
                violated_tag_constraint_concepts.add(concept)
            
            
            #checks if concepts and their related semantics are lemmatized according to wordnet's morphy function called by NLTK
            lmtzr = WordNetLemmatizer()         
            #using pos tag to improve accuracy of lemmatizer
            if (lmtzr.lemmatize(concept, get_wordnet_pos(pos_tag([concept])[0][1])) != concept):
                unlemmatized_concepts.add(concept)
            for semantic in concept_info[8:13]:
                if (lmtzr.lemmatize(semantic, get_wordnet_pos(pos_tag([semantic])[0][1])) != semantic):
                    unlemmatized_concepts.add(semantic)                
            
            
    print "Number of not defined semantics are: ", len(not_defined_semantics)
    print "Number of duplicate tag concepts are: ", len(duplicate_tag_concepts) 
    print "Number of polarity - intensity mismatch concepts are: ", len(polarity_intensity_mismatch_concepts)
    print "Number of polarity mismatch between pairs of concept and semantic are: ", len(semantic_concept_polarity_mismatch)
    print "Number of concept having either interest-surprise or fear-anger tags are: ", len(violated_tag_constraint_concepts)
    print "Number of unlemmatized concepts and semantics: ", len(unlemmatized_concepts)
            

def print_comparison_stats(true_positive, true_negative, false_positive, false_negative):
    total = true_positive + false_negative + false_positive + true_negative
    accuracy = float(true_positive + true_negative) / float(total)
    precision = float(true_positive) / float(true_positive + false_positive)
    recall = float(true_positive) / float(true_positive + false_negative)
    f1_score = float(2*true_positive) / float(2*true_positive + false_positive + false_negative)
      
    print 'Confusion Matrix'
    print true_positive, false_negative
    print false_positive, true_negative   
    print 'Accuracy', accuracy
    print 'Precision', precision
    print 'Recall', recall
    print 'F1 score', f1_score


def check_inter_bing_liu_opinion_lexicon():
    '''
    Runs consistency check between SenticNet and Bing Liu's Opinion Lexicon
    '''       
    #polarity confusion matrix between SenticNet and Bing Liu's Opinion Lexicon for overlapping words taking the later as the correct labels
    negative_words_bing_liu = []
    positive_words_bing_liu = []
    with open('BingLiuOpinionLexiconEnglish/negative_words.txt') as f_neg:
        i = 0
        for line in f_neg:                    
            if (i >= 35):
                negative_words_bing_liu.append(line.strip())
            i += 1;
    with open('BingLiuOpinionLexiconEnglish/positive_words.txt') as f_pos:
        i = 0
        for line in f_pos:                    
            if (i >= 35):
                positive_words_bing_liu.append(line.strip())
            i += 1;            

    false_positive = 0
    false_negative = 0
    true_positive = 0
    true_negative = 0 
    for neg_word in negative_words_bing_liu:
        if (neg_word in senticnet):
            if (senticnet[neg_word][6] == 'positive'):
                false_positive += 1
            else:
                true_negative += 1              
    for pos_word in positive_words_bing_liu:
        if (pos_word in senticnet):
            if (senticnet[pos_word][6] == 'negative'):
                false_negative += 1
            else:
                true_positive += 1               
    print "\nComparison Statistics with Bing Liu's Opinion Lexicon\n"
    print_comparison_stats(true_positive, true_negative, false_positive, false_negative)        


    '''
    2) MPQA Subjectivity Lexicon
    3) SentiWordNet
    4) Harvard General Inquirer 
    '''
    

def check_inter_mpqa_subjectivity_lexicon():
    '''
    Runs consistency check between SenticNet and MPQA Subjectivity Lexicon
    '''      
    #polarity confusion matrix between SenticNet and MPQA Subjectivity Lexicon for overlapping words taking the later as the correct labels
    negative_words = []
    positive_words = []
    with open('MPQASubjectivityLexicon/subjectivity_clues.tff', 'r') as f:
        for line in f:
            line = line.strip().split()
            word = line[2][6:]
            polarity = line[5][14:]
            if (polarity == 'positive'):
                positive_words.append(word)
            else:
                negative_words.append(word)
        
    false_positive = 0
    false_negative = 0
    true_positive = 0
    true_negative = 0 
    for neg_word in negative_words:
        if (neg_word in senticnet):
            if (senticnet[neg_word][6] == 'positive'):
                false_positive += 1
            else:
                true_negative += 1              
    for pos_word in positive_words:
        if (pos_word in senticnet):
            if (senticnet[pos_word][6] == 'negative'):
                false_negative += 1
            else:
                true_positive += 1     
    print "\nComparison Statistics with MPQA Subjectivity Lexicon\n"
    print_comparison_stats(true_positive, true_negative, false_positive, false_negative)            


def check_inter_sentiwordnet():
    '''
    Runs consistency check between SenticNet and SentiWordNet
    '''
    #polarity confusion matrix between SenticNet and SentiWordNet for overlapping words taking the later as the correct labels
    #assumes positive polarity if pos score > neg score and negative polarity if neg score < pos score
    #ignore comparisons for non sentiment words, i.e., words having same positive and negative polarity value in SentiWordNet
    false_positive = 0
    false_negative = 0
    true_positive = 0
    true_negative = 0     
    for senti_synset in swn.all_senti_synsets():
        word = senti_synset.synset.name()[:-5]
        pos_score = senti_synset.pos_score()
        neg_score = senti_synset.neg_score()
        #ignore non sentiment words
        if (pos_score == neg_score):
            continue
        polarity = 'positive' if pos_score > neg_score else 'negative'
        if (word in senticnet):
            if (polarity == 'positive'):
                if (senticnet[word][6] == 'negative'):
                    false_negative += 1
                else:
                    true_positive += 1         
            else:
                if (senticnet[word][6] == 'positive'):
                    false_positive += 1
                else:
                    true_negative += 1                       
    print "\nComparison Statistics with SentiWordNet\n"
    print_comparison_stats(true_positive, true_negative, false_positive, false_negative)     
    

def check_inter_harvard_general_inquirer():
    '''
    Runs consistency check between SenticNet and Harvard General Inquirer
    '''      
    #polarity confusion matrix between SenticNet and Harvard General Inquirer for overlapping words taking the later as the correct labels
    #only considering words from the inquirer labelled as positiv or negativ (discarding other labeled words) 
    #note that pstv is an older tag for positive and ngtv is an older tag for negative
    negative_words = []
    positive_words = []
    with open('harvard_general_inquirer.txt', 'r') as f:
        for line in f:        
            #skip first line
            line = line.strip().split(' ')
            if (line[0] == 'Entryword'):
                continue
            if ('Neg' in line):
                negative_words.append(line[0].lower())
            elif ('Pos' in line):
                positive_words.append(line[0].lower())                
    
    false_positive = 0
    false_negative = 0
    true_positive = 0
    true_negative = 0 
    for neg_word in negative_words:
        if (neg_word in senticnet):
            if (senticnet[neg_word][6] == 'positive'):
                false_positive += 1
            else:
                true_negative += 1              
    for pos_word in positive_words:
        if (pos_word in senticnet):
            if (senticnet[pos_word][6] == 'negative'):
                false_negative += 1
            else:
                true_positive += 1     
    print "\nComparison Statistics with Harvard General Inquirer\n"   
    print_comparison_stats(true_positive, true_negative, false_positive, false_negative)              
    
    
if __name__ == '__main__':
    #runs various consistency checks within SenticNet
    checks_intra()       
    #runs various consistency checks between SenticNet and other models:
    #Bing Liu's Opinion Lexicon, MPQA Subjectivity Lexicon, SentiWordNet, Harvard General Inquirer
    check_inter_bing_liu_opinion_lexicon()
    check_inter_mpqa_subjectivity_lexicon()
    check_inter_sentiwordnet()
    check_inter_harvard_general_inquirer()    
