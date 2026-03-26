import sqlite3

conn = sqlite3.connect('db/data.db')
cur = conn.cursor()

# Map old dummy values to correct DAD wording
mapping = {
    'submitter': 'DAD User',
    'viewer': 'DAD User',
    'admin': 'TSA',
    'approver': 'TSA',
}

for old_val, new_val in mapping.items():
    cur.execute("UPDATE audit_user_access SET old_access = ? WHERE old_access = ?", (new_val, old_val))
    cur.execute("UPDATE audit_user_access SET new_access = ? WHERE new_access = ?", (new_val, old_val))

conn.commit()

# Verify
cur.execute("SELECT DISTINCT old_access FROM audit_user_access UNION SELECT DISTINCT new_access FROM audit_user_access")
print("Distinct values now:", [r[0] for r in cur.fetchall()])

conn.close()
print("Done")
