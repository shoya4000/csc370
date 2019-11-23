#!/usr/bin/python

import psycopg2
import getpass
import subprocess

username = raw_input("username: ")
password = getpass.getpass(prompt='database password: ')
conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user=username, password=password)
cur = conn.cursor()
res = subprocess.call('psql -c "\d+ user_acc" test postgres',
                      stdout=subprocess.PIPE)
print(res.stdout.decode(sys.stdout.encoding))
while(True):
    raw = raw_input(">")
    command = cur.mogrify(raw)
    try:
        cur.execute(command)
        result = cur.fetchall()
        for line in result:
            print(line)
        conn.commit()
    except psycopg2.Error as e:
        print(e.pgerror)
        conn.rollback()
