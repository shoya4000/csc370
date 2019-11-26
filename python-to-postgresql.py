#!/usr/bin/python
import psycopg2
import getpass


def formatAndPrintResultTable(cur):
    # instantiate table to fill for printing
    table = []
    # gather headers
    if cur.description:
        headers = []
        for header in cur.description:
            headers.append(header.name)
        table.append(headers)
    # gather rows
    result = cur.fetchall()
    print(result)
    for row in result:
        string_row = []
        for item in row:
            string_row.append(str(item))
        table.append(string_row)
    # define column width (longest item + 1)
    row_format = ""
    for i in range(len(headers)):
        row_format += "{:<%d}" % (len(max([row[i]
                                           for row in table], key=len)) + 1)
    # print the result table
    for row in table:
        print(row_format.format(*row))
    # commit the change to the database

username = raw_input("username: ")
# securely request password
password = getpass.getpass(prompt='database password: ')
# establish connection
conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user=username, password=password)
# begin interaction
cur = conn.cursor()

while(True):
    raw = raw_input(">")
    # handle \d for quick view of schema (psycopg2 can't handle meta-commands)
    if (str(raw) == '\d'):
        # if you run 'psql -U shoya -h studentdb1.csc.uvic.ca -E' with the E on
        # the end, it echos back the command, this is what is actually running
        # when \d is entered
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
    # handle \q to quit
    elif (str(raw) == '\q'):
        quit()
    # convert command into proper SQL format
    command = cur.mogrify(raw)
    try:
        # run the SQL query
        cur.execute(command)
        # format output
        formatAndPrintResultTable(cur)
        # commit the change to the database
        conn.commit()
    except psycopg2.Error as e:
        print(e.pgerror)
        # rollback error caused
        conn.rollback()
