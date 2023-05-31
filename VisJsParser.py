from typing import List
import numpy as np

NORMAL_VISJS_FONT_SIZE = 15
MAX_VISJS_FONT_SIZE = 200


def noun_dict_to_visjs_nodes(noun_dict: dict[str, int]):

    noun_list: List[str] = list(noun_dict.keys())
    min_num_of_occurrences_for_a_word = min(noun_dict.values())
    font_size_multiplier: int = round(NORMAL_VISJS_FONT_SIZE / min_num_of_occurrences_for_a_word)



    output: str = "["

    for i, word in enumerate(noun_list):
        number_of_occurrences = noun_dict[word]
        font_size = number_of_occurrences*font_size_multiplier
        output += f"{{id: {i}, label: \"{word}\", font:{{size: {font_size} }} }},"

    output = output[:-1] + "]"

    return output

def adjacency_matrix_to_visjs_edges(adjacency_matrix: np.array):

    id_counter: int = 0

    output = "["

    for i, row in enumerate(adjacency_matrix):
        for k, column_item in enumerate(row):
            # print(column_item)

            # If a cell is 1 and is not on the diagonal (avoid self loops)
            if (adjacency_matrix[i][k] == 1) and (i is not k):
                line = f"{{from: {i}, to: {k}, id: \"{i},{k},{id_counter}\"}},"
                output += line

                id_counter += 1

    output = output[:-1] + "]"

    return output


def get_visjs_graph_object(noun_dict: dict[str, int], adjacency_matrix: np.array):
    output: str = "{\n"

    output += "nodes: " + noun_dict_to_visjs_nodes(noun_dict=noun_dict) + ",\n"
    output += "edges: " + adjacency_matrix_to_visjs_edges(adjacency_matrix=adjacency_matrix) + "\n}"

    # print(sum(noun_dict.values()))
    return output
