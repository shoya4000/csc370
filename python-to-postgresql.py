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

        table = []

        headers = []
        for header in cur.description:
            headers.append(header.name)
        table.append(headers)

        result = cur.fetchall()
        for row in result:
            string_row = []
            for item in row:
                string_row.append(str(item))
            table.append(string_row)

        row_format = ""
        for i in range(len(headers)):
            row_format += "{:<%d}" % (len(max([row[i]
                                               for row in table], key=len)) + 1)
        for row in table:
            print(row_format.format(*row))

        conn.commit()
    except psycopg2.Error as e:
        print(e.pgerror)
        conn.rollback()
