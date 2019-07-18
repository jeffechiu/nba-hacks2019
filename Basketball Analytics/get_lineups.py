import psycopg2 as pg2

con = pg2.connect(database='basketball', user='isdb')
con.autocommit = True
cur = con.cursor()

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

get_one_sect = cur.mogrify('''

		SELECT *
		  FROM Play_by_Play
		 WHERE game_id='006728e4c10e957011e1f24878e6054a' and period=1;
'''
	)

cur.execute(get_one_sect)
rows = cur.fetchall()

game_table = cur.mogrify('''

	INSERT INTO Games(game_id)
	SELECT DISTINCT game_id
	  FROM Play_by_Play
	 ORDER by game_id
	  '''
	)
cur.execute(game_table)

num_games = cur.mogrify('''

	SELECT COUNT(*)
	  FROM Games

	''')

cur.execute(num_games)
rows = cur.fetchall()
print_rows(rows)