#!/usr/bin/env python

"""Unit tests for the `rebus.py` file."""

import unittest
from rebus import roundrobin, Rebus, Sentence, Score


class TestRoundRobin(unittest.TestCase):

    def test_roundrobin_with_letters(self):
        generator = roundrobin('ABC', 'D', 'EF')
        output = ''.join(generator)
        self.assertEqual(output, 'ADEBFC')

    def test_roundrobin_against_unequal_iterables(self):
        generator = roundrobin('AB', 'CDEFGHI')
        output = ''.join(generator)
        self.assertEqual(output, 'ACBDEFGHI')

    def test_roundrobin_with_only_one_iterable(self):
        generator = roundrobin('ABC')
        output = ''.join(generator)
        self.assertEqual(output, 'ABC')


class TestRebusClass(unittest.TestCase):

    def test_dove_rebus_to_solve(self):
        output = Rebus(':dove', 'sl', 'd')
        self.assertEqual(str(output), 'solve')

    def test_dove_image_rebus_to_solve(self):
        output = Rebus('dove_symbol.png', 'sl', 'd')
        print output

    def test_rebus_of_rebus_to_solve(self):
        output = Rebus(':dove', Rebus(':castle', subtract=':cat'),
                                Rebus(':badge', subtract=':bag'))
        self.assertEqual(str(output), 'solve')

    def test_rebus_all_the_way_down(self):
        output = Rebus(':dove', Rebus(':castle', subtract=Rebus(':cat')),
                                Rebus(':badge', subtract=Rebus(':bag')))
        self.assertEqual(str(output), 'solve')


class TestReplaceLetters(unittest.TestCase):

    def setUp(self):
        self.r = Rebus('')

    def test_replace_letters_normal(self):
        word = self.r.replace_letters('dove', 'de')
        self.assertEqual(str(word), 'ov')

    def test_replace_letters_for_whole_word(self):
        word = self.r.replace_letters('dove', 'dove')
        self.assertEqual(str(word), '')


class TestWordPermutations(unittest.TestCase):

    def setUp(self):
        self.r = Rebus('')

    def test_permutations_for_dove(self):
        output = self.r.word_permutations('do', 've')
        assert 'dove' in output

    def test_permutations_for_work(self):
        output = self.r.word_permutations('rk', 'wo')
        assert 'work' in output

    def test_permutations_for_solved(self):
        output = self.r.word_permutations('lve', 'so')
        assert 'solve' in output

    def test_permutations_for_this(self):
        output = self.r.word_permutations('hs', 'ti')
        assert 'this' in output

    def test_permutations_for_here(self):
        output = self.r.word_permutations('er', 'he')
        assert 'here' in output


class TestSentenceClass(unittest.TestCase):

    def test_sentence_with_higher_scoring_rebus(self):
        output = Sentence(Rebus(':dove', 'sl', 'd'),
                          Rebus(':tie', 'hs', 'e'),
                          Rebus(':book', 'wr', 'bo'),
                          Rebus(':bee', 'hr', 'b'))
        self.assertEqual(str(output), "solve this work here")
        self.assertEqual(output.score, 57)

    def test_sentence_with_lowering_scoring_rebus(self):
        output = Sentence(Rebus(':love', 'so', 'o'),
                          Rebus(':house', 'ti', 'oue'),
                          Rebus(':rake', 'wo', 'ae'),
                          Rebus(':ear', 'he', 'a'))
        self.assertEqual(str(output), "solve this work here")
        self.assertEqual(output.score, 31)


class TestScoreClass(unittest.TestCase):

    def test_score_class_with_word(self):
        word = Score('hello')
        self.assertEqual(word, 'hello')
        self.assertEqual(word.score, 17)

    def test_score_class_with_image(self):
        word = Score(':image')
        self.assertEqual(word.score, 0)

    def test_score_of_already_scored(self):
        scored = Score(':hi')
        self.assertEqual(Score(scored).score, 0)

    def test_score_class_with_empty_string(self):
        empty = Score('')
        self.assertEqual(empty.score, 0)

    def test_score_class_addition(self):
        hello = Score('hello')
        world = Score('world')
        self.assertEqual(hello + world, 38)


if __name__ == '__main__':
    unittest.main()
