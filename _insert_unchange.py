import sqlite3
conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# For each req_signer row, find the signer_limit rows for that gad_id
# that are NOT already referenced by a Change/Remove row in req_signer_limit
# (identified by signer_limit_id), and insert them as 'Unchange' rows.

req_rows = c.execute('SELECT id, gad_id FROM req_signer ORDER BY id').fetchall()
print(f'req_signer: {len(req_rows)} rows')

# Get current max id in req_signer_limit
max_id = c.execute('SELECT COALESCE(MAX(id), 0) FROM req_signer_limit').fetchone()[0]
print(f'Current max req_signer_limit.id: {max_id}')

inserted = 0
for req_id, gad_id in req_rows:
    # Get signer_limit_ids already referenced by this req_signer
    existing_sl_ids = set(
        r[0] for r in c.execute(
            'SELECT signer_limit_id FROM req_signer_limit WHERE req_signer_id = ? AND signer_limit_id IS NOT NULL',
            (req_id,)
        ).fetchall()
    )
    
    # Get all signer_limit rows for this gad_id
    sl_rows = c.execute(
        'SELECT id, territory_id, policy_id, limit_amount, approval_cc_id, '
        'exception, temp, temp_start_date, temp_end_date, '
        'business_rationale, business_control, account_restriction, currency '
        'FROM signer_limit WHERE gad_id = ? ORDER BY id',
        (gad_id,)
    ).fetchall()
    
    for sl in sl_rows:
        sl_id = sl[0]
        if sl_id in existing_sl_ids:
            continue  # already has a Change/Remove row
        
        max_id += 1
        # Unchange: signer_limit_id set, old_* columns set, new_* columns NULL
        c.execute(
            'INSERT INTO req_signer_limit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (max_id, req_id, 'Unchange', sl_id,
             sl[1], sl[2], sl[3], sl[4], sl[5], sl[6], sl[7], sl[8], sl[9], sl[10], sl[11], sl[12],
             None, None, None, None, None, None, None, None, None, None, None, None)
        )
        inserted += 1

conn.commit()

print(f'Inserted {inserted} Unchange rows')
print()

# Verify
total = c.execute('SELECT COUNT(1) FROM req_signer_limit').fetchone()[0]
print(f'Total req_signer_limit rows: {total}')

for r in c.execute("SELECT action, COUNT(1) FROM req_signer_limit GROUP BY action ORDER BY action"):
    print(f'  {r[0]}: {r[1]}')

# Sample
print()
print('=== Sample Unchange row ===')
r = c.execute("SELECT * FROM req_signer_limit WHERE action='Unchange' LIMIT 1").fetchone()
if r:
    cols = [d[1] for d in c.execute('PRAGMA table_info(req_signer_limit)').fetchall()]
    for col, val in zip(cols, r):
        print(f'  {col}: {val}')

conn.close()
print('\nDone!')
