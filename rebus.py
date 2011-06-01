#!/usr/bin/env python

"""
Python rebus generator. More information is available in the README.md file.

>>> Rebus(':dove', 'sl', 'd')
'solve'
>>> Rebus(':dove', Rebus(':castle', subtract=':cat'),
...                Rebus(':badge', subtract=':bag'))
'solve'

"""

import re
from itertools import cycle, islice, permutations

from utils import image_mappings, read_word_list

IMAGE_NAMES = image_mappings('files/images.txt')
CORPUS = read_word_list('files/word_list.txt')


def roundrobin(*iterables):
    """
    From itertools' recipes:  http://bit.ly/iter_recipes

    >>> ''.join(roundrobin('ABC', 'D', 'EF'))
    'ADEBFC'
    """
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


class Rebus(object):
    """
    Take an image name, additional word, and subtraction letters and return the
    correct rebus word.

    >>> Rebus(':dove', 'sl', 'd')
    'solve'
    """

    def __init__(self, image, add='', subtract=''):
        names = IMAGE_NAMES  # Local variable is faster.
        if image in names:
            image = names[image]
            image_split = image.split()
            if len(image_split) > 1:
                letters = set([letter for letter in subtract])
                image = self._match_image(image_split, letters)
        elif not add:
            self.score = Score(subtract)
            self.value = self.replace_letters(image, subtract)
            return None
        self.score = Score(add) + Score(subtract)
        add = self.replace_letters(add)  # Get rid of any colons.
        word = self.replace_letters(image, subtract)
        self.value = self.logic(word, add)

    def _match_image(self, names, letters):
        """
        Some images have multiple meanings, such as 'dove_symbol.png'
        meaning both 'dove' and 'peace'. This method checks the subtraction
        letters against the image meanings to return the right one.
        """
        for index, image_name in enumerate(names):
            for letter in letters:
                if image_name and letter not in image_name:
                    names[index] = None
        # Return the first true image name.
        for image_name in names:
            if image_name:
                return image_name

    def __iter__(self):
        return iter(self.value)

    def __repr__(self):
        return self.value

    def startswith(self, letter):
        """Mimic string startswith method."""
        if letter == ':':
            return True

    def replace_letters(self, word, replace=''):
        """Replace letters in a word."""
        if isinstance(word, str):
            word = re.sub(':', '', word)
        else:
            # It's a Rebus object.
            word = word.value
        if not replace:
            return word
        for letter in replace:
            # The 'book' example threw me off, so now using a regex for loop:
            # Rebus(':book', 'wr', 'bo') => 'work'
            word = re.sub(letter, '', word, 1)
        return word

    def logic(self, word, add):
        """
        Rebus logic. Since it's not straightforward as to how the final
        word is formed, this is still being tweaked -- along with the
        `word_permutations` method.
        """
        corpus = CORPUS
        possible = [''.join(roundrobin(add, word)),
                    ''.join(roundrobin(word, add)),
                    ''.join([add, word]),
                    ''.join([word, add])]
        for answer in possible:
            if answer in corpus:
                return answer
        # No answer in possible -- must use word_permutations method.
        possible = self.word_permutations(word, add)
        return possible.pop()

    def word_permutations(self, word, add):
        """Permutations for all possible words when combining two."""
        corpus = CORPUS
        letters = ''.join([word, add])
        words = (''.join(p) for p in permutations(letters, len(letters)))
        possible = set([w for w in words if w in corpus])
        return possible


class Sentence(object):
    """Create a sentence from a group of Rebus objects."""

    def __init__(self, *iterables):
        self.score = 0
        self.iterables = iterables
        for rebus in iterables:
            self.score += rebus.score

    def __repr__(self):
        return ' '.join(rebus.value for rebus in self.iterables)


class Score(str):
    """
    Keep score on add and subtract word values. The word is checked against
    the known image name dictionary and a set of vowels -- both have lookup
    times of O(1).
    """
    def __init__(self, word):
        if 'score' in self:
            return  # No need to assign a score.
        self._get_score(word)

    def _get_score(self, word):
        """Get the score for a given word/image."""
        self.score = 0
        names = IMAGE_NAMES
        vowels = set(['a', 'e', 'i', 'o', 'u'])
        # Check the word's not an image.
        if not word.startswith(':') and word not in names:
            for letter in word:
                if letter in vowels:
                    self.score += 1
                else:
                    self.score += 5

    def __add__(self, other):
        return self.score + other.score


def main():
    print 'zoological' in CORPUS
    print Rebus(':dove', 'sl', 'd')


if __name__ == '__main__':
    main()
