from categories import items
from database_services.RDBService import _get_db_connection

conn = _get_db_connection()
cur = conn.cursor()

for i in items:
    alias = i['alias']
    title = i['title']

    if len(i['parents']) > 0:
        parent = i['parents'][0]
    else:
        parent = None
    sql = "INSERT INTO UsersGroups.Activities (alias, title, parent) VALUES" + f" (\"{alias}\", \"{title}\", \"{parent}\")"
    cur.execute(sql)

conn.commit()
conn.close()