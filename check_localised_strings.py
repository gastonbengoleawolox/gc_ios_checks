#!/usr/bin/env python

import os
import re
import sys
import argparse


def error(description):
	print >>sys.stderr, description
	# sys.exit(1)


def error_list(title, elements):
	error("%s:\n\n%s" % (title, "\n".join(map(lambda s: " - " + s, elements))))


def sources(gcpath):
	return [os.path.join(root, filename)
		for root, dirnames, filenames in os.walk(gcpath + '/GreenCommuter')
		for filename in filenames
		if filename.endswith(('.swift', '.m'))
	]

def localised_keys_in_file(filename):
	with open(filename) as file:
		return set(re.findall(r'\"([^\"]+)\"\.localize', file.read(), re.MULTILINE))


def get_localised_keys(gcpath):
	return reduce(set.union, map(localised_keys_in_file, sources(gcpath)), set())


# TODO: handle interpolated strings...

def get_defined_keys(gcpath):
	with open(gcpath + "/GreenCommuter/Supporting Files/en.lproj/Localizable.strings") as localizable_file:
		keys = set()
		for line_number, line in enumerate(map(lambda s: s.rstrip("\n").strip(), localizable_file)):
			if not line or re.match(r'\/\*.*\*\/', line) or re.match(r'\/\/.*$', line):
				continue

			match = re.match(r'"([^"]*)"\s*=\s*".*";', line)
			if not match:
				error("Localizable file line #%d not valid: '%s'" % (line_number, line))
				continue
			
			key = match.group(1)
			if key in keys:
				error("Duplicated key '%s' at line #%d" % (key, line_number))
				continue

			keys.add(key)
		return keys


def parse_arguments():
	parser = argparse.ArgumentParser(description="Check that the localised strings are properly set.")
	parser.add_argument('--gcpath', default="../green-commuter-ios",  help='sum the integers (default: find the max)')
	return parser.parse_args()


if __name__ == "__main__":

	arguments = parse_arguments()

	used_keys = get_localised_keys(arguments.gcpath)
	defined_keys = get_defined_keys(arguments.gcpath)

	unused_keys = defined_keys - used_keys
	undefined_keys = used_keys - defined_keys

	print

	if unused_keys:
		error_list("Unused keys", unused_keys)

	print

	if undefined_keys:
		error_list("Undefined keys", undefined_keys)

	print
