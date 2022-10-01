# POS Tagging System - Viterbi Algorithm Implementing Hidden Markov Model

## Running the System:

### Two ways

1) Run the script named system.py to POS tag the file WSJ_23.words

2) To tag a words file with the format "<word>\t<POStag>\n", use the following command to run the script: python3 ms12297_HMMPOSTagging_Viterbi.py your_filename. 
Replace your_filename with the file you want to tag. The output file generated will be called "output.pos". 


## Implementation:

### Training Stage

This stage involves populating the following dictionaries to then use in the Viterbi algorithm that implements the Hidden Markov Model for POS Tagging,

There are a total of 4 dictionaries used in the system for training: likelihood, transition, OOV, and TOTALS, along with a set titled words.
 
The likelihood and transition dictionaries store the likelihood and transition probabilties for each word encountered in training respecitvely.

The OOV dictionary is used to handle Out-Of-Vobulary words (OOV for short) as it stores keys that are the tags of the words that appear once in the training corpus and the values are the frequencies of the tags
of those words divided by the total number of these tags in the training corpus. This achieves a much higher accuracy than just assigning the 1/1000 proability to OOV words since
all the OOV words are now considered a single word, the most likely tag is concluded using the likelihood probability.

The TOTALS dictionary is used to keep track of the total appearances of each tag in the training corpus.

The set titled words simply contains all the unique words encountered in the training corpus to assist with OOV handling.

### Tagging Stage

The tagging stage employs the Viterbi algorithm to calculate as the product of previous viterbi probabilties, transition probability and likelihood probability for every word in a 
sentence until the End_Sent tag is reached (denoted by an empty line) beginning from the Begin_Sent tag.

The dictionaries arr and back are used to keep track of the index of the word within the sentence currently being tagged and the previous tag in the algorithm respectively.


## Further Improving Accuracy

Indeed, handling OOVs well creates a huge improvement in the accuracy of the system. However, it was important to also handle words that return a viterbi probability of 0 in all cases.
This is a result of some words not appearing in a transition not included in the training corpus. Thus, I handle these "noPath" cases separetely. In such cases, the simplest solution I
found was to record the current tag with maximum likelihood and the previous tag with maximum viterbi proability. In essence, this addresses this OOV case by ensuring there is a path
to transition to this word in the algorithm.

