#!/usr/bin/env python

from __future__ import print_function
import sys

# Import the imdb package.
import imdb

# Create the object that will be used to access the IMDb's database.
ia = imdb.IMDb()  # by default access the web.

if len(sys.argv) < 2:
    print("Usage: script [movielist] [manual=0]")
    quit()

filename = ''
manual = 0
for i in range(1, len(sys.argv)):
    if i == 1:
        filename = sys.argv[i]
        print("Movie list filename:", filename)

    if i == 2:
        if int(sys.argv[2]) == 1:
            manual = 1
            print("Manual movie selection enabled")
print("")
num_lines = sum(1 for line in open(filename))

jsonf = open('movielist.json', 'w')

jsonf.write("{")
with open(filename) as mfile:
    for lineidx, line in enumerate(mfile):
        name = line.rstrip("\n")

        s_result = ia.search_movie(name)
        chosen = 0

        if manual == 1:
            if len(s_result) > 1:
                print("All found results for query:", name)
                for idx, item in enumerate(s_result):
                    print(idx, item['long imdb canonical title'], item.movieID)
                print("")
                var = raw_input("Enter the chosen movie number")
                chosen = int(var)

        movid = s_result[chosen].movieID

        movdata = s_result[chosen]
        ia.update(movdata)

        print("Working on", movdata['title'])

        # print("{\"title\":\"", the_unt['title'], "\",\"imdb_id\":\"tt", movid, "\",\"poster_url\":\"", the_unt['cover url'],"\"}", sep='')
        try:
            jsonf.write("{\"title\":\"" + movdata['title'] + "\",\"imdb_id\":\"tt" + movid + "\",\"poster_url\":\"" + movdata['cover url'] + "\"}")

            print(lineidx)
            print(lineidx, num_lines)
            if lineidx != num_lines - 1:
                jsonf.write(",")

        except:
            print("Oops!", sys.exc_info()[0], "occured.")
            print("Next entry.")
            print()

        #break

jsonf.write("}")
