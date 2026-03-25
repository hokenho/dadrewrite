import sqlite3
conn = sqlite3.connect('db/data.db')
conn.execute('DROP TABLE IF EXISTS audit_dadreq')
conn.commit()
print('audit_dadreq dropped')
for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(f'  {r[0]}')
conn.close()
