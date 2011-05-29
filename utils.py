#!/usr/bin/env python

"""Useful utility functions."""

import csv


def image_mappings(filename):
    """Get the mappings for files and corresponding names."""
    with open(filename) as f:
        dialect = csv.Sniffer().sniff(f.read(200))
        f.seek(0)  # Go back to beginning of file.
        image_dict = dict((key, value) for key, value in \
                           csv.reader(f, dialect=dialect))
    return image_dict


def read_word_list(filename):
    """
    Read in a word list, and use it as a corpus. Even though it takes up
    more memory to use a set (Python hash tables are never more than 2/3 full),
    it's worth the O(1) lookup times for word permutations.
    """
    with open(filename) as f:
        words = frozenset(word.strip() for word in f)
    return words


def main():
    print read_word_list('word_list.txt')


if __name__ == '__main__':
    main()
