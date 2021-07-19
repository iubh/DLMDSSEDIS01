# Define a map function that returns (word, 1) as key-value pair for each word in the text.
def map_function(text):
    for word in text.lower().split():
        yield word, 1

# Apply map function all elements in the dataset
def apply_map(data):
    map_results = []
    for element in data:
        for map_result in map_function(element):
            map_results.append(map_result)
    return map_results


def group_function(map_results):
    # Group the key-value pairs produced by the map step by their key.
    group_results = dict()
    for key, value in map_results:
        if key not in group_results:
            group_results[key] = []
        group_results[key].append(value)
    return group_results

# Define a reduce function that sums up the counts of words.
def reduce_function(key, values):
    total = 0
    for count in values:
        total += count
    return key, total


def apply_reduce(group_results):
    # Apply the reduce function to each key-value pair
    reduce_results = dict()
    for key, values in group_results.items():
        _, count = reduce_function(key, values)
        reduce_results[key] = count
    return reduce_results


def filter_function(results, min_occurrences=4):
    return {k: v for k, v in results.items() if v >= min_occurrences}


def count_words_naive(corpus):
    map_results = apply_map(data_set)
    group_results = group_function(map_results)
    reduce_results = apply_reduce(group_results)
    return reduce_results

from typing import List, Optional, Dict
import warnings
import os


def count_words(corpus: List[str], filter: Optional[int] = None) -> Dict[str, int]:
    """Count all words in a corpus of documents.

    :param corpus: A list of strings, where each string contains the text of a document.
    :param filter: int or None. If None, don't filter the result. Else return words with at
                   least 'filter' occurrences in the corpus.
    
    :return: A dictionary of words and their respective counts, filtered by count
             as specified.
    """

    assert type(corpus) is list, "The corpus to analyse needs to be list of strings"

    map_results = apply_map(corpus)
    group_results = group_function(map_results)
    reduce_results = apply_reduce(group_results)
    if filter is None:
        return reduce_results
    else:
        assert type(filter) is int, f"The 'filter' argument needs to be a Python int, you specified: '{filter}' which is of type {type(filter)}"
        return filter_function(reduce_results, min_occurrences=filter)


def count_words_from_files(files: List[str], skip_corrupted_files=False, filter=None):
    """Count all words in a corpus of documents provided as files.

    :param files: A list of file names (str) on your local file system. The files
                  contain the text you want to count words for. 
    :param skip_corrupted_files: boolean. If True, ignore all files that can't be
                                 read, otherwise abort.
    ...
    """
    corpus = []
    for file_name in files:
        with open(file_name, 'r') as f:
            try:
                text = f.read()
                corpus.append(text)
            except:
                msg = f"The file {file_name} cannot be read. Remove it from the corpus."
                if skip_corrupted_files:
                    warnings.warn(msg)
                else:
                    raise ValueError(msg)
    return count_words(corpus, filter) # reuse function


if __name__ == "__main__":
    # Create a toy data set to run the program on.
    text_1 = "Lorem ipsum dolor sit amet, consetetur et sadipscing elitr."
    text_1b = "Lorem ipsum dolor sit amet, consetetur et sadipscing elitr."
    text_2 = "At vero lorem et accusam et justo duo ipsum et ea rebum."
    text_2b = "At vero lorem et accusam et justo duo ipsum et ea rebum. At vero lorem et accusam et justo duo ipsum et ea rebum."

    data_set = [text_1, text_1b, text_2, text_2b]

    map_results = apply_map(data_set)
    print(map_results)
    # Output: [('lorem', 1), ('ipsum', 1), ('dolor', 1), ...]

    group_results = group_function(map_results)
    print(group_results)
    # Output: {'lorem': [1, 1, 1, 1, 1], 'ipsum': [1, 1, 1, 1, 1], 'dolor': [1, 1] ...}

    reduce_results = apply_reduce(group_results)
    print(reduce_results)
    # Output: {'lorem': 5, 'ipsum': 5, 'dolor': 2 ...}

    filter_results = filter_function(reduce_results)
    print(filter_results)
    # Output: {'lorem': 5, 'ipsum': 5, 'et': 11}

    assert reduce_results == count_words(data_set)

    files = ["./data/file_1.txt", "./data/file_2.txt", 
    "./data/file_3.txt", "./data/file_4.txt", "./data/corrupt.rtf"]
    assert reduce_results == count_words_from_files(files, skip_corrupted_files=True)