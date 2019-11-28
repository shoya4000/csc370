#!/usr/bin/python
import psycopg2
import getpass


describe = '''SELECT n.nspname as "Schema",
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


def formatAndPrintResultTable(cur):
    # format and print the response from the SQL executed
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
    else:
        print(cur.statusmessage)


def runCommand(cur, raw, conn):
        # format and execute the SQL
    # convert command into proper SQL format
    command = cur.mogrify(raw)
    try:
        # run the SQL query
        cur.execute(command)
        # format output
        formatAndPrintResultTable(cur)
    except psycopg2.Error as e:
        print(e.pgerror)
        # rollback error caused
        conn.rollback()


def demo(cur, conn):
    print("Running demo:")
    # run create
    print("\nCommand to run psql script to delete and recreate database:")
    raw_input(">\create")
    with open('psql_create_db.sql', 'r') as file:
        raw = file.read()
    runCommand(cur, raw, conn)
    # run describe
    print("\nCommand to run psql's meta-command \d (describe):")
    raw_input(">\d")
    raw = describe
    runCommand(cur, raw, conn)
    # run select all users
    print("\nSelect and display all users and their information:")
    raw = "SELECT * FROM user_acc;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run select all profiles
    print("\nSelect and display all profiles:")
    raw = "SELECT * FROM Profile;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run select all Follows
    print("\nSelect and display all profiles:")
    raw = "SELECT * FROM Follows;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run select all Posts
    print("\nSelect and display all posts:")
    raw = "SELECT * FROM Post;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run select all Posts
    print("\nSelect and display all content:")
    raw = "SELECT * FROM Content;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run select all PostTags
    print("\nSelect and display all post tags:")
    raw = "SELECT * FROM PostTags;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    print("\nSelect and display all Profile tags:")
    raw = "SELECT * FROM ProfileTags;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    print("\nSelect and display all comments:")
    raw = "SELECT * FROM Comment;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run insert
    print("\nInsert a Test User:")
    raw = "INSERT INTO user_acc (Email, PermissionLevel, Username, Password) VALUES('test@uvic.ca', TRUE, 'Test User', 'TestPassword');"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run select all
    print("Show updated table:")
    raw = "SELECT * FROM user_acc;"
    raw_input(">" + raw)
    runCommand(cur, raw, conn)
    # run delete Martin
    print("\nDelete Martin from the database:")
    raw = '''DELETE FROM Post WHERE ProfileID=(SELECT ProfileID FROM Profile WHERE UserID=(SELECT UserID FROM user_acc WHERE Username='Martin'));
			DELETE FROM Follows WHERE FollowerProfileID=(SELECT ProfileID FROM Profile WHERE UserID=(SELECT UserID FROM user_acc WHERE Username='Martin')) OR FolloweeProfileID=(SELECT ProfileID FROM Profile WHERE UserID=(SELECT UserID FROM user_acc WHERE Username='Martin'));
			DELETE FROM Profile WHERE UserID=(SELECT UserID FROM user_acc WHERE Username='Martin');
			DELETE FROM user_acc WHERE Username='Martin';'''
    raw = cur.mogrify(raw)
    raw_input("\n>" + raw)
    runCommand(cur, raw, conn)
    # run select all
    print("\nShow updated table:")
    raw = "SELECT * FROM user_acc;"
    raw_input("\n>" + raw)
    runCommand(cur, raw, conn)

username = raw_input("username: ")
# securely request password
password = getpass.getpass(prompt='database password: ')
# establish connection
conn = psycopg2.connect(host="studentdb1.csc.uvic.ca",
                        database="the_homies", user=username, password=password)
# set autocommit
conn.autocommit = True
# begin interaction
cur = conn.cursor()

while(True):
    raw = raw_input(">")
    if (str(raw) == '\demo'):
        demo(cur, conn)
        continue
    # handle \d for quick view of schema (psycopg2 can't handle meta-commands)
    elif (str(raw) == '\d'):
        # if you run 'psql -U shoya -h studentdb1.csc.uvic.ca -E' with the -E on
        # the end, it echos back the command. This is what is actually running
        # when \d is entered
        raw = describe
    # handle \q to quit
    elif (str(raw) == '\q'):
        quit()
    elif (str(raw) == '\create'):
        with open('psql_create_db.sql', 'r') as file:
            raw = file.read()
    elif (str(raw) == ''):
        continue
    runCommand(cur, raw, conn)
