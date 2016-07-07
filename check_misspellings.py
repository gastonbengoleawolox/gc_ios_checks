#!/usr/bin/env python

import os
import re
import sys
import argparse


def sources(gcpath):
    return [os.path.join(root, filename)
        for root, dirnames, filenames in os.walk(gcpath + '/GreenCommuter')
        for filename in filenames
        if filename.endswith('.swift')
    ]


def convertToSnake(word):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def splitCompositeWord(word):
    word = convertToSnake(word)
    return word.split("_")


def notNumeric(word):
    return re.match(r'\d+$', word) is None


def wordsInFile(filename):
    with open(filename, 'r') as f:
        result = set()
        for word in set(w for w in re.findall(r'\w+', f.read()) if notNumeric(w)):
            for inner in splitCompositeWord(word):
                if inner:
                    result.add(inner)
        return result


def words(path):
    result = set()
    for sourceFile in sources(path):
        result |= wordsInFile(sourceFile)
    return result


def parse_arguments():
    parser = argparse.ArgumentParser(description="Check that the words are correctly spelled.")
    parser.add_argument('--gcpath', default="../green-commuter-ios",  help='path to green-commuter-ios project folder.')
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    print "\n".join(words(arguments.gcpath))

    # used_keys = get_localised_keys(arguments.gcpath)
    # defined_keys = get_defined_keys(arguments.gcpath)

    # unused_keys = defined_keys - used_keys
    # undefined_keys = used_keys - defined_keys

    # print

    # if unused_keys:
    #   error_list("Unused keys", unused_keys)

    # print

    # if undefined_keys:
    #   error_list("Undefined keys", undefined_keys)

    # print
