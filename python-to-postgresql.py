#!/usr/bin/python

import psycopg2
import getpass

username = raw_input("username: ")
password = getpass.getpass(prompt='database password: ')
conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user=username, password=password)
cur = conn.cursor()
while(True):
    psql = raw_input(">")
    try:
        cur.execute(psql)
    except psycopg2.OperationalError as e:
        print(e)
    result = cur.fetchall()
    for line in result:
        print(line)
