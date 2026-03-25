import sqlite3, json, random
conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# Get existing req_signer data
old_rows = c.execute(
    'SELECT id, req_date, submitter, gad_id, bu_id, '
    'old_pickup_cheque, old_temp, old_temp_start_date, old_temp_end_date, old_status, '
    'new_pickup_cheque, new_temp, new_temp_start_date, new_temp_end_date, new_status '
    'FROM req_signer ORDER BY id'
).fetchall()
print(f'req_signer: {len(old_rows)} rows to migrate')

# Get TSA users for approver2_gad_id
tsa_users = [r[0] for r in c.execute("SELECT gad_id FROM user_access WHERE access='TSA'").fetchall()]
print(f'TSA users: {tsa_users}')

# Get all user gad_ids for approver1_gad_id
all_users = [r[0] for r in c.execute('SELECT gad_id FROM wd_user_profile').fetchall()]
avp_pool = [u for u in all_users if u not in tsa_users][:15]
print(f'AVP pool: {len(avp_pool)} users')

# Rebuild req_signer with new schema
c.execute('DROP TABLE req_signer')
c.execute('''CREATE TABLE req_signer (
    id              INTEGER PRIMARY KEY,
    req_date        TEXT,
    submitter       TEXT,
    gad_id          TEXT,
    bu_id           INTEGER,
    approver1_gad_id TEXT,
    approver1_result INTEGER,
    approver1_note TEXT,
    approver2_gad_id TEXT,
    approver2_result INTEGER,
    approver2_note TEXT,
    old_pickup_cheque   INTEGER,
    old_temp            INTEGER,
    old_temp_start_date TEXT,
    old_temp_end_date   TEXT,
    old_status          INTEGER,
    new_pickup_cheque   INTEGER,
    new_temp            INTEGER,
    new_temp_start_date TEXT,
    new_temp_end_date   TEXT,
    new_status          INTEGER,
    status_reason   TEXT
)''')

random.seed(42)
approval_reasons = [
    'Approved per gdas_policy', 'Business need confirmed',
    'Verified by manager', 'Aligned with delegation gdas_policy', 'Within threshold'
]
reject_reasons = [
    'Exceeds delegation limit', 'Missing business rationale',
    'Duplicate request', 'Not aligned with gdas_policy'
]

for row in old_rows:
    (rid, req_date, submitter, gad_id, bu_id,
     old_pickup, old_temp, old_temp_start, old_temp_end, old_st,
     pickup_cheque, temp, temp_start, temp_end, _) = row
    
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
    
    c.execute('INSERT INTO req_signer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (rid, req_date, submitter, gad_id, bu_id,
         avp_gad, avp_result, avp_reason,
         tsa_gad, tsa_result, tsa_reason,
         old_pickup, old_temp, old_temp_start, old_temp_end, old_st,
         pickup_cheque, temp, temp_start, temp_end,
         status, status_reason))

conn.commit()
print()
print('=== new req_signer schema ===')
for r in c.execute('PRAGMA table_info(req_signer)'): print(r)
print()
cnt = c.execute('SELECT COUNT(1) FROM req_signer').fetchone()[0]
print(f'=== req_signer count: {cnt} ===')
print()
print('=== sample row ===')
r = c.execute('SELECT * FROM req_signer LIMIT 1').fetchone()
cols = [d[1] for d in c.execute('PRAGMA table_info(req_signer)').fetchall()]
for col, val in zip(cols, r):
    print(f'  {col}: {val}')
print()
print('=== status distribution ===')
for r in c.execute('SELECT status, COUNT(1) FROM req_signer GROUP BY status'):
    label = {None: 'Pending (NULL)', 0: 'Rejected', 1: 'Approved'}
    print(f'  {label.get(r[0], r[0])}: {r[1]}')

# =========================================================
# Now rebuild req_signer_limit with correct column order
# =========================================================
print()
print('=' * 50)
print('Rebuilding req_signer_limit...')

old_lr = c.execute(
    'SELECT id, req_signer_id, action, signer_limit_id, '
    'old_territory_id, old_policy_id, old_limit_amount, old_approval_cc_id, old_exception, '
    'old_temp, old_temp_start_date, old_temp_end_date, old_business_rationale, old_business_control, '
    'old_account_restriction, old_currency, '
    'new_territory_id, new_policy_id, new_limit_amount, new_approval_cc_id, new_exception, '
    'new_temp, new_temp_start_date, new_temp_end_date, new_business_rationale, new_business_control, '
    'new_account_restriction, new_currency '
    'FROM req_signer_limit ORDER BY id'
).fetchall()
print(f'req_signer_limit: {len(old_lr)} rows to migrate')

c.execute('DROP TABLE req_signer_limit')
c.execute('''CREATE TABLE req_signer_limit (
    id              INTEGER PRIMARY KEY,
    req_signer_id   INTEGER,
    action          TEXT,
    signer_limit_id INTEGER,
    old_territory_id    INTEGER,
    old_policy_id       INTEGER,
    old_limit_amount    REAL,
    old_approval_cc_id  INTEGER,
    old_exception       INTEGER,
    old_temp            INTEGER,
    old_temp_start_date TEXT,
    old_temp_end_date   TEXT,
    old_business_rationale INTEGER,
    old_business_control   INTEGER,
    old_account_restriction TEXT,
    old_currency        TEXT,
    new_territory_id    INTEGER,
    new_policy_id       INTEGER,
    new_limit_amount    REAL,
    new_approval_cc_id  INTEGER,
    new_exception       INTEGER,
    new_temp            INTEGER,
    new_temp_start_date TEXT,
    new_temp_end_date   TEXT,
    new_business_rationale INTEGER,
    new_business_control   INTEGER,
    new_account_restriction TEXT,
    new_currency        TEXT
)''')

for lr in old_lr:
    c.execute('INSERT INTO req_signer_limit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', lr)

# Insert Unchange rows for signer_limit rows not already referenced
max_id = c.execute('SELECT COALESCE(MAX(id), 0) FROM req_signer_limit').fetchone()[0]
req_rows = c.execute('SELECT id, gad_id FROM req_signer ORDER BY id').fetchall()
unchange_count = 0
for req_id, gad_id in req_rows:
    existing_sl_ids = set(
        r[0] for r in c.execute(
            'SELECT signer_limit_id FROM req_signer_limit WHERE req_signer_id = ? AND signer_limit_id IS NOT NULL',
            (req_id,)
        ).fetchall()
    )
    sl_rows = c.execute(
        'SELECT id, territory_id, policy_id, limit_amount, approval_cc_id, '
        'exception, temp, temp_start_date, temp_end_date, '
        'business_rationale, business_control, account_restriction, currency '
        'FROM signer_limit WHERE gad_id = ? ORDER BY id',
        (gad_id,)
    ).fetchall()
    for sl in sl_rows:
        if sl[0] in existing_sl_ids:
            continue
        max_id += 1
        c.execute('INSERT INTO req_signer_limit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (max_id, req_id, 'Unchange', sl[0],
             sl[1], sl[2], sl[3], sl[4], sl[5], sl[6], sl[7], sl[8], sl[9], sl[10], sl[11], sl[12],
             None, None, None, None, None, None, None, None, None, None, None, None))
        unchange_count += 1
print(f'Inserted {unchange_count} Unchange rows')

conn.commit()
print()
print('=== new req_signer_limit schema ===')
for r in c.execute('PRAGMA table_info(req_signer_limit)'): print(r)
print()
cnt2 = c.execute('SELECT COUNT(1) FROM req_signer_limit').fetchone()[0]
print(f'=== req_signer_limit count: {cnt2} ===')
print()
print('=== sample row ===')
r = c.execute('SELECT * FROM req_signer_limit LIMIT 1').fetchone()
cols = [d[1] for d in c.execute('PRAGMA table_info(req_signer_limit)').fetchall()]
for col, val in zip(cols, r):
    print(f'  {col}: {val}')

conn.close()
print()
print('Done!')
