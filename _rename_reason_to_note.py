import sqlite3
conn = sqlite3.connect('db/data.db')
c = conn.cursor()
c.execute('ALTER TABLE req_signer RENAME COLUMN approver1_reason TO approver1_note')
c.execute('ALTER TABLE req_signer RENAME COLUMN approver2_reason TO approver2_note')
conn.commit()
# Verify
cols = [row[1] for row in c.execute('PRAGMA table_info(req_signer)').fetchall()]
print('req_signer columns:', cols)
conn.close()
print('Done.')
