import os

import nltk
from collections import Counter
import inflect
from S3Client import S3Client

nltk.data.path.append("/tmp")
nltk.download("punkt", download_dir="/tmp")
nltk.download('averaged_perceptron_tagger', download_dir="/tmp")

s3_client = S3Client()


custom_stop_word_list = s3_client.read_file_from_s3(bucket_name=os.environ["AWS_S3_BUCKET"], file_name="stop_words.txt", is_list=True)

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


    # Prevents same word appearing in multiple nodes in different cases.
    # Combines versions of words with different cases where words with more capital letters are prioritised
    # e.g. "UK" has priority over "Uk" so "Uk" is absorbed by "UK" to become a single node "Uk"
    noun_frequency_tuple_list_with_no_duplicates = []
    noun_to_tuple_map = {}  # Maps noun to noun-frequency tuple
    nouns_lowercase_list = []
    nouns_lowercase_to_saved_case_map = {}  # Maps the lowercase form of the noun to the noun in whatever case it was saved in the noun_frequency_tuple_list_with_no_duplicates


    for noun_frequency_tuple in noun_frequency_tuple_list:
        noun = noun_frequency_tuple[0]
        frequency_value = noun_frequency_tuple[1]

        if noun.lower() not in nouns_lowercase_list:
            noun_frequency_tuple_list_with_no_duplicates.append(noun_frequency_tuple)  # Adds tuple to final list
            nouns_lowercase_list.append(noun.lower())  # Adds to comparison list
            nouns_lowercase_to_saved_case_map[noun.lower()] = noun  # Allows us to find the saved noun from the lowercase noun
            noun_to_tuple_map[noun.lower()] = noun_frequency_tuple  # Allows us to find the tuple from the lowercase noun later
        else:
            conflicting_noun_num_of_capital_letters = sum(1 for c in noun if c.isupper())
            saved_noun = nouns_lowercase_to_saved_case_map[noun.lower()]
            saved_noun_num_of_capital_letters = sum(1 for c in saved_noun if c.isupper())
            new_noun_has_more_capital_letters = conflicting_noun_num_of_capital_letters > saved_noun_num_of_capital_letters

            # Sum the frequency of the conflicting noun and the saved noun
            saved_tuple = noun_to_tuple_map[noun.lower()]
            saved_frequency = saved_tuple[1]
            new_frequency = frequency_value + saved_frequency

            # The frequency value of the saved tuple needs to be changed, so we delete it
            noun_frequency_tuple_list_with_no_duplicates.remove(saved_tuple)

            if new_noun_has_more_capital_letters:
                # Removed the saved noun-frequency tuple and add the new tuple
                new_noun_and_frequency_tuple = (noun, new_frequency)
                noun_frequency_tuple_list_with_no_duplicates.append(new_noun_and_frequency_tuple)

                nouns_lowercase_to_saved_case_map[noun.lower()] = noun
                noun_to_tuple_map[noun.lower()] = new_noun_and_frequency_tuple
            else:
                new_noun_and_frequency_tuple = (saved_noun, new_frequency)
                noun_frequency_tuple_list_with_no_duplicates.append(new_noun_and_frequency_tuple)

                noun_to_tuple_map[noun.lower()] = new_noun_and_frequency_tuple

    noun_frequency_tuple_list = noun_frequency_tuple_list_with_no_duplicates  # Update the list

    # Uncomment below if nodes need to be examined
    # print(dict(noun_frequency_tuple_list))


    # Return the top N nouns and their frequencies AND the non_plural to original map
    # Output arguments not ideal but saves us from doing expensive calculation twice
    return [dict(noun_frequency_tuple_list), non_plural_to_original_map]