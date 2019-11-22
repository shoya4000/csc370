#!/usr/bin/python

import psycopg2

user = input("username: ")
password = getpass.getpass(prompt='database password: ')
conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user=user, password=password)
cur = conn.cursor()

cur.execute('SELECT * FROM user_acc')
print(cur.fetchone())
