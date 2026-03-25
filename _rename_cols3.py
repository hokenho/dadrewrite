import sqlite3
conn = sqlite3.connect('db/data.db')
c = conn.cursor()

renames = [
    ('req_signer', 'approver_avp_gad_id', 'approver1_gad_id'),
    ('req_signer', 'approver_avp_result', 'approver1_result'),
    ('req_signer', 'approver_avp_reason', 'approver1_reason'),
    ('req_signer', 'approver_tsa_gad_id', 'approver2_gad_id'),
    ('req_signer', 'approver_tsa_result', 'approver2_result'),
    ('req_signer', 'approver_tsa_reason', 'approver2_reason'),
]

for tbl, old, new in renames:
    c.execute(f'ALTER TABLE {tbl} RENAME COLUMN {old} TO {new}')
    print(f'{tbl}: {old} -> {new}')

conn.commit()

print('\n=== Verification ===')
cols = [r[1] for r in c.execute('PRAGMA table_info(req_signer)')]
print(f'  req_signer: {cols}')

conn.close()
print('\nDone!')
