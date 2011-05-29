Rebus Generator
===============

From [ITA puzzles](http://goo.gl/F0z1W).


Instructions
------------

A rebus is a phrase or sentence expressed all or in part through
pictures. For this puzzle, you will use pictures from this archive (use
the included file "images.txt" to map pictures to the associated words).
Write a program that will take an English sentence ([here’s a list of
test cases for you to
use](http://www.itasoftware.com/images/careers/Rebus%20Icons/Rebus%20Test%20Cases.txt))
and generate a rebus from it. Here’s a simple example:


    (:dove + sl - d) (:tie + hs - e) (:book + wr - bo) (:bee + hr - b)
                          solve this work here


That is, each word becomes a parenthesized expression with up to three
components: a word corresponding to a picture from the clipart library,
a sequence of letters to be added to the name of the picture, and a
sequence of letters to be deleted from the name. Distinguish words used
as pictures from other sequences of letters by prepending a colon. The
order of letters must match: the letters to be added must be in the
order in which they would appear in the target word, and the letters to
be deleted must be in the order in which they appear in the image name.
Your program should produce plain text output.

But there’s more to the puzzle than that. Suppose we charge 5 points for
every consonant you add or delete, and 1 point for every vowel. Now come
up with a rebus that costs the fewest points. The example above costs 57
points, but this rebus of the same phrase: 


    (:love + so - o) (:house + ti - oue) (:rake + wo - ae) (:ear + he - a)
                          solve this work here


Finally, you can reduce the cost even further by adding or subtracting
images (which cost nothing) instead of letters. If you use recursive
encodings, you can get rid of letters altogether. For instance, a
recursive rebus for “solve” is:


              (:dove + (:castle - :cat) - (:badge - :bag))
                                 solve


Write a program to generate recursive rebuses like the one above. Your
program may use a mix of letters and pictures; balance performance
against optimal scores as you see fit. Even for all-picture rebuses, a
shorter rebus is better.
