import sqlite3, json, random
conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# Get existing signer_req data
old_rows = c.execute(
    'SELECT id, req_date, submitter, gad_id, bu_id, pickup_cheque, '
    'temp, temp_start_date, temp_end_date, status, source_data '
    'FROM signer_req ORDER BY id'
).fetchall()
print(f'signer_req: {len(old_rows)} rows to migrate')

# Get TSA users for approver_tsa_gad_id
tsa_users = [r[0] for r in c.execute("SELECT gad_id FROM user_access WHERE access='TSA'").fetchall()]
print(f'TSA users: {tsa_users}')

# Get all user gad_ids for approver_avp_gad_id
all_users = [r[0] for r in c.execute('SELECT gad_id FROM user_profile').fetchall()]
avp_pool = [u for u in all_users if u not in tsa_users][:15]
print(f'AVP pool: {len(avp_pool)} users')

# Rebuild signer_req with new schema
c.execute('DROP TABLE signer_req')
c.execute('''CREATE TABLE signer_req (
    id              INTEGER PRIMARY KEY,
    req_date        TEXT,
    submitter       TEXT,
    gad_id          TEXT,
    bu_id           INTEGER,
    approver_avp_gad_id TEXT,
    approver_avp_result INTEGER,
    approver_avp_reason TEXT,
    approver_tsa_gad_id TEXT,
    approver_tsa_result INTEGER,
    approver_tsa_reason TEXT,
    source_data     TEXT,
    pickup_cheque   INTEGER,
    temp            INTEGER,
    temp_start_date TEXT,
    temp_end_date   TEXT,
    status          INTEGER,
    status_reason   TEXT
)''')

random.seed(42)
approval_reasons = [
    'Approved per policy', 'Business need confirmed',
    'Verified by manager', 'Aligned with delegation policy', 'Within threshold'
]
reject_reasons = [
    'Exceeds delegation limit', 'Missing business rationale',
    'Duplicate request', 'Not aligned with policy'
]

for row in old_rows:
    rid, req_date, submitter, gad_id, bu_id, pickup_cheque, temp, temp_start, temp_end, old_status, source_data = row
    
    avp_gad = random.choice(avp_pool)
    tsa_gad = random.choice(tsa_users)
    
    # Distribute: ~60% both approved, ~15% pending AVP, ~10% AVP approved pending TSA, ~15% rejected
    roll = random.random()
    if roll < 0.60:
        avp_result = 1; avp_reason = random.choice(approval_reasons)
        tsa_result = 1; tsa_reason = random.choice(approval_reasons)
        status = 1; status_reason = None
    elif roll < 0.75:
        avp_result = None; avp_reason = None
        tsa_result = None; tsa_reason = None
        status = None; status_reason = None
    elif roll < 0.85:
        avp_result = 1; avp_reason = random.choice(approval_reasons)
        tsa_result = None; tsa_reason = None
        status = None; status_reason = None
    else:
        if random.random() < 0.5:
            avp_result = 0; avp_reason = random.choice(reject_reasons)
            tsa_result = None; tsa_reason = None
        else:
            avp_result = 1; avp_reason = random.choice(approval_reasons)
            tsa_result = 0; tsa_reason = random.choice(reject_reasons)
        status = 0; status_reason = random.choice(reject_reasons)
    
    c.execute('INSERT INTO signer_req VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (rid, req_date, submitter, gad_id, bu_id,
         avp_gad, avp_result, avp_reason,
         tsa_gad, tsa_result, tsa_reason,
         source_data, pickup_cheque, temp, temp_start, temp_end,
         status, status_reason))

conn.commit()
print()
print('=== new signer_req schema ===')
for r in c.execute('PRAGMA table_info(signer_req)'): print(r)
print()
cnt = c.execute('SELECT COUNT(1) FROM signer_req').fetchone()[0]
print(f'=== signer_req count: {cnt} ===')
print()
print('=== sample row ===')
r = c.execute('SELECT * FROM signer_req LIMIT 1').fetchone()
cols = [d[1] for d in c.execute('PRAGMA table_info(signer_req)').fetchall()]
for col, val in zip(cols, r):
    print(f'  {col}: {val}')
print()
print('=== status distribution ===')
for r in c.execute('SELECT status, COUNT(1) FROM signer_req GROUP BY status'):
    label = {None: 'Pending (NULL)', 0: 'Rejected', 1: 'Approved'}
    print(f'  {label.get(r[0], r[0])}: {r[1]}')

# =========================================================
# Now rebuild signer_limit_req with correct column order
# =========================================================
print()
print('=' * 50)
print('Rebuilding signer_limit_req...')

old_lr = c.execute(
    'SELECT id, signer_req_id, action, source_id, source_data, '
    'territory_id, policy_id, limit_amount, approval_cc_id, exception, '
    'temp, temp_start_date, temp_end_date, business_rationale, business_control, '
    'account_restriction, currency '
    'FROM signer_limit_req ORDER BY id'
).fetchall()
print(f'signer_limit_req: {len(old_lr)} rows to migrate')

c.execute('DROP TABLE signer_limit_req')
c.execute('''CREATE TABLE signer_limit_req (
    id              INTEGER PRIMARY KEY,
    signer_req_id   INTEGER,
    action          TEXT,
    source_id       INTEGER,
    source_data     TEXT,
    territory_id    INTEGER,
    policy_id       INTEGER,
    limit_amount    REAL,
    approval_cc_id  INTEGER,
    exception       INTEGER,
    temp            INTEGER,
    temp_start_date TEXT,
    temp_end_date   TEXT,
    business_rationale INTEGER,
    business_control   INTEGER,
    account_restriction TEXT,
    currency        TEXT
)''')

for lr in old_lr:
    c.execute('INSERT INTO signer_limit_req VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', lr)

conn.commit()
print()
print('=== new signer_limit_req schema ===')
for r in c.execute('PRAGMA table_info(signer_limit_req)'): print(r)
print()
cnt2 = c.execute('SELECT COUNT(1) FROM signer_limit_req').fetchone()[0]
print(f'=== signer_limit_req count: {cnt2} ===')
print()
print('=== sample row ===')
r = c.execute('SELECT * FROM signer_limit_req LIMIT 1').fetchone()
cols = [d[1] for d in c.execute('PRAGMA table_info(signer_limit_req)').fetchall()]
for col, val in zip(cols, r):
    print(f'  {col}: {val}')

conn.close()
print()
print('Done!')
