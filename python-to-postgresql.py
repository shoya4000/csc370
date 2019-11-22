#!/usr/bin/python

import psycopg2

conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user="shoya", password="V00730770")
cur = conn.cursor()

cur.execute('SELECT * FROM user_acc')
print(cur.fetchone())
