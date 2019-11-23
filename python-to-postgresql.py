#!/usr/bin/python
from __future__ import print_function
import psycopg2
import getpass

username = raw_input("username: ")
password = getpass.getpass(prompt='database password: ')
conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user=username, password=password)
cur = conn.cursor()

while(True):
    raw = raw_input(">")
    if (str(raw) == '\d'):
        raw = '''SELECT n.nspname as "Schema",
  					c.relname as "Name",
  					CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' THEN 'foreign table' WHEN 'p' THEN 'table' END as "Type",
  					pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
				FROM pg_catalog.pg_class c
     				LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
				WHERE c.relkind IN ('r','p','v','m','S','f','')
      					AND n.nspname <> 'pg_catalog'
      					AND n.nspname <> 'information_schema'
      					AND n.nspname !~ '^pg_toast'
  					AND pg_catalog.pg_table_is_visible(c.oid)
				ORDER BY 1,2;'''
    elif (str(raw) == '\q'):
        quit()
    command = cur.mogrify(raw)
    try:
        cur.execute(command)

        row_format = "{:<15}" * (len(cur.description) + 1)
        headers = []
        for header in cur.description:
            headers.append(header.name)
        print(row_format.format(*headers))
        result = cur.fetchall()
        for row in result:
            print(row_format.format("", *row))

        for header in cur.description:
            print(header.name + "\t", end='')
        print()

        for row in result:
            for item in row:
                print(str(item) + "\t", end='')
            print()
        conn.commit()
    except psycopg2.Error as e:
        print(e.pgerror)
        conn.rollback()
