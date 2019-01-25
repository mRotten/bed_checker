#!/usr/bin/env python
# bed_checker.py

import sys
import argparse

__doc__=="""
Checks a bed file for several issues, reports on the issues it finds.
"""

global header
header = False

def detect_overlaps(path):
    sys.stdout.write("Looking for overlaps...\n")
    curr_chr, last_end = None, 0
    overlaps = 0
    with open(path,'r') as infile:
        if header:
            a = infile.readline()
        for i, line in enumerate(infile):
            line1 = line.split("\t")
            if line1[0] == curr_chr and last_end >= int(line1[1]):
                overlaps += 1
            curr_chr = line1[0]
            last_end = int(line1[2])
        if overlaps > 0:
            sys.stdout.write(f'    File HAS {overlaps} overlapping interval pairs.\n')
            return
    sys.stdout.write("    No overlaps detected.\n")

def detect_header(path):
    global header
    sys.stdout.write("Looking for header...\n")
    with open(path,'r') as infile:
        try:
            int(infile.readline().split("\t")[1])
        except ValueError:
            sys.stdout.write("    File HAS a header.\n")
            header = True
            return
    sys.stdout.write("    No header found.\n")

def detect_unsorted(path):
    sys.stdout.write("Looking for unsorted lines...\n")
    curr_chr, last_start = None, 0
    with open(path,'r') as infile:
        if header:
            a = infile.readline()
        for line in infile:
            line1 = line.split("\t")
            if curr_chr == line1[0] and int(line1[1]) < last_start:
                sys.stdout.write("    File is NOT sorted.\n")
                return
            curr_chr = line1[0]
            last_start = int(line1[1])
    sys.stdout.write("    File is sorted.\n")

def detect_chr_prefix(path):
    sys.stdout.write("Looking for chromosome format...\n")
    with open(path,'r') as infile:
        for line in infile:
            if line.lower().startswith("chr"):
                sys.stdout.write("    File chromosome column HAS 'chr' prefix.\n")
                return
    sys.stdout.write("    File chromosome column does not have 'chr' prefix.\n")

def detect_incorrect_col_count(path):
    sys.stdout.write("Looking for uniform column count...\n")
    with open(path,'r') as infile:
        col_count = len(infile.readline().split("\t"))
        for i, line in enumerate(infile):
            line_len = len(line.split("\t"))
            if len(line.split("\t")) != col_count:
                sys.stdout.write(f'    Expecting {col_count} columns, line {i+2} '\
                                 f'has {line_len} columns.\n')
                return
    sys.stdout.write(f'    All lines have {col_count} columns.\n')

def detect_zero_len_col(path):
    sys.stdout.write("Looking for zero-length columns...\n")
    with open(path,'r') as infile:
        for i, line in enumerate(infile):
            line1 = line.split('\t')
            if '' in line1 or '\n' in line1:
                sys.stdout.write(f'    File line {i+1} has zero-length column entries.\n')
                return
    sys.stdout.write("    All columns have data or placeholders.\n")

def process_file(path):
    detect_header(path)
    detect_chr_prefix(path)
    detect_overlaps(path)
    detect_unsorted(path)
    detect_incorrect_col_count(path)
    detect_zero_len_col(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bed", help="Input BED file")
    args = parser.parse_args()
    process_file(args.bed)
