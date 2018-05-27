#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import mydb

CONN_STRING = mydb.get_CONN()
con = mydb.getCon(CONN_STRING)

query = "select distinct value from property_fa where property = '<http://fa.dbpedia.org/property/type>'"

rows = mydb.executeQueryResult(con, query, True)

with open('types_fa.txt', 'w') as fout:
    print len(rows)
    for row in rows:
        fout.write(row[0] + '\n')
