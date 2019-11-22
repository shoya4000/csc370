#!/usr/bin/python

import psycopg2

username = input("username: ")
print(username)
password = getpass.getpass(prompt='database password: ')
conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user=username, password=password)
cur = conn.cursor()

cur.execute('SELECT * FROM user_acc')
print(cur.fetchone())
