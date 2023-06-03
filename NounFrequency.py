import nltk
from collections import Counter
import numpy as np
import inflect


# Must be lowercase
custom_stop_word_list = ["video", "way", "pictures", "year", "month", "week", "podcast", "new", "new", "co", "my", "out",
                         "images", "says", "rise"]

def get_top_nouns_and_plural_hash(strings, N):
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
    nouns = [noun for noun in nouns if noun.lower() not in custom_stop_word_list]

    # Convert plurals into singular words to prevent a plural and singular version of a word from being treated differently
    non_plural_to_original_map = {}  # So we can find the plural word from the non-plural later
    p = inflect.engine()
    # nouns = [p.singular_noun(noun) or noun for noun in nouns]
    updated_nouns = []
    for noun in nouns:
        non_plural_noun = p.singular_noun(noun)
        if not non_plural_noun:  # If we can't un-plural-ise the noun: do nothing
            updated_nouns.append(noun)
        else:  # If we can: do it and add it to the map, so we can find the plural version later
            updated_nouns.append(non_plural_noun)
            non_plural_to_original_map[non_plural_noun] = noun
    nouns = updated_nouns



    # Count the frequency of each noun
    noun_counts = Counter(nouns)
    noun_frequency_tuple_list = []

    # Replace all the plural verbs that were made singular with the original plural verbs
    for noun_and_frequency_tuple in noun_counts.most_common(N):
        noun_key = noun_and_frequency_tuple[0]
        frequency_value = noun_and_frequency_tuple[1]

        # print(non_plural_to_original_map.get(noun_key) or "lol")
        new_noun_key = non_plural_to_original_map.get(noun_key) or noun_key
        new_noun_and_frequency_tuple = (new_noun_key, frequency_value)
        noun_frequency_tuple_list.append(new_noun_and_frequency_tuple)

    # Return the top N nouns and their frequencies AND the non_plural to original map
    # Output arguments not ideal but saves us from doing expensive calculation twice
    return [dict(noun_frequency_tuple_list), non_plural_to_original_map]