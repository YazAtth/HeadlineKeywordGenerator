import nltk
from collections import Counter
import numpy as np
import inflect



custom_stop_word_list = ["video", "way", "pictures", "year", "month", "week", "podcast", "new", "New"]

def top_nouns(strings, N):
    # Tokenize the strings into words
    words = [nltk.word_tokenize(string) for string in strings]


    # POS tag the words
    pos_tagged_words = [nltk.pos_tag(word) for word in words]
    # Extract only the nouns
    nouns = [word for pos_tagged_word in pos_tagged_words for word, pos in pos_tagged_word if pos.startswith('N')]

    # Remove punctuation by removing all items that are not alphanumeric
    nouns = [noun for noun in nouns if noun.isalnum()]

    # Removes all one-letter words
    nouns = [noun for noun in nouns if len(noun) > 1]

    # Remove custom words that appear frequently in news headlines
    nouns = [noun for noun in nouns if noun not in custom_stop_word_list]

    # Convert plurals into singular words to prevent a plural and singular version of a word from being treated differently
    p = inflect.engine()
    nouns = [p.singular_noun(noun) or noun for noun in nouns]

    # Count the frequency of each noun
    noun_counts = Counter(nouns)
    # Return the top N nouns and their frequencies
    return dict(noun_counts.most_common(N))