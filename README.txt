These Python scripts perform knowledge expansion and consistency checks on SenticNet. Refer to report.pdf (download and view for best reading experience) for description and results of experiments.

$ Knowledge expansion:
In knowledge expansion I created new Sentic vectors to augment the existing data base of 50,000 vectors. A total of 6175 new Sentic vectors were created with varying (subjective) accuracy. My expansion strategies are based on two related algorithms to find semantically similar words to a given word.

Algorithm 1:
Execute the script by running "python knowledge_expansion_1.py"

The output will be in the directory "Output/1/" and contain txt and csv files for positive sentic vectors, negative sentic vectors and both polarity combined.

Algorithm 2:
Execute the script by running "python knowledge_expansion_2.py"

The output will be in the directory "Output/2/" and contain txt and csv files for positive sentic vectors, negative sentic vectors and both polarity combined.

$ Consistency checks:
In my consistency checking experiments, I performed both checks within SenticNet and similarity checks between SenticNet and other models.

Execute the script by running "python consistency_check.py"

Results for the following checks should be displayed:
(Intra checks)
Check if the set of 5 semantics of a concept are defined concepts themselves in SenticNet
Check if concepts have duplicate tags
Check for negative intensity for positive polarity concepts and positive intensity for negative polarity concepts
Check if 5 semantics of a concept have the same polarity as the concept
Check for interest-surprise or fear-anger used together in tags of a concept
Check if concepts and their related semantics are lemmatized according to the Morphy function of WordNet called by NLTK
(Inter checks)
Bing Liu’s Opinion Lexicon
MPQA Subjectivity Lexicon
SentiWordNet
Harvard General Inquirer

The Data folder contains the database of other word models used in the inter similarity checks.
