from typing import List

import numpy as np
import numpy.typing


def get_showing_together_matrix(noun_dict: dict, headline_list: List[str]) -> np.array:
    noun_list = list(noun_dict.keys())

    showing_together_matrix = np.zeros((len(noun_list), len(noun_dict)), int)

    for i, word1 in enumerate(noun_list):
        for k, word2 in enumerate(noun_list):
            for sentence in headline_list:
                # if word1 in sentence and word2 in sentence.replace(word1, ""):
                if word1 in sentence and word2 in sentence:
                    showing_together_matrix[i][k] += 1
                    # print(f"{word1} and {word2} is in '{sentence}'")

    return showing_together_matrix


def get_adjacency_matrix(noun_dict: dict, headline_list: List[str]) -> np.array:
    showing_together_matrix: np.array = get_showing_together_matrix(noun_dict, headline_list)

    adjacency_matrix = (showing_together_matrix > 0).astype(int)

    return adjacency_matrix

