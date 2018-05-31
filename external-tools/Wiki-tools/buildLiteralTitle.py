#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Build a literal-title table

import sys
import psycopg2
import codecs
import psycopg2.extras
import get_paragraph_prefer


CONN_STRING = "host='localhost' dbname='yago' user='yago' password='yago'"


def generateLiteral():
    # EN:
    # generate a file contains all items.

    query = "select distinct object from yagofacts where object ~ '\".*\"@eng'"
    rows = get_paragraph_prefer.searchDB(CONN_STRING, query)
    print len(rows)
    with open('eng.txt', 'w') as fout:
        for row in rows:
            fout.write(row['object'] + "\n")


def writeRecord():
    literalFile = open('eng.txt', 'r')
    ltFile = open('eng.lt.txt', 'w')
    while True:
        line = literalFile.readline()
        if line is None:
            break
        word = line.replace(" ", "_")[1:-6]
        print word
        break


def main():
    writeRecord()


if __name__ == "__main__":
    main()
