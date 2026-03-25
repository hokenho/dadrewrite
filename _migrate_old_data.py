import sqlite3, json

conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# ============================================================
# 1. Migrate req_signer: old_data JSON -> old_* columns, rename columns to new_*
# ============================================================
print('=== Migrating req_signer ===')
old_rows = c.execute(
    'SELECT id, req_date, submitter, gad_id, bu_id, '
    'approver1_gad_id, approver1_result, approver1_note, '
    'approver2_gad_id, approver2_result, approver2_note, '
    'old_data, pickup_cheque, temp, temp_start_date, temp_end_date, status, status_reason '
    'FROM req_signer ORDER BY id'
).fetchall()
print(f'  {len(old_rows)} rows to migrate')

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
    status_reason       TEXT
)''')

for row in old_rows:
    (rid, req_date, submitter, gad_id, bu_id,
     a1_gad, a1_result, a1_reason, a2_gad, a2_result, a2_reason,
     old_data_json, pickup_cheque, temp, temp_start, temp_end, status, status_reason) = row

    # Parse old_data JSON
    if old_data_json:
        od = json.loads(old_data_json)
        old_pickup = od.get('pickup_cheque')
        old_temp = od.get('temp')
        old_temp_start = od.get('temp_start_date')
        old_temp_end = od.get('temp_end_date')
        old_status = od.get('status')
    else:
        old_pickup = old_temp = old_temp_start = old_temp_end = old_status = None

    c.execute('INSERT INTO req_signer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (rid, req_date, submitter, gad_id, bu_id,
         a1_gad, a1_result, a1_reason, a2_gad, a2_result, a2_reason,
         old_pickup, old_temp, old_temp_start, old_temp_end, old_status,
         pickup_cheque, temp, temp_start, temp_end, status, status_reason))

print('  req_signer migrated')

# ============================================================
# 2. Migrate req_signer_limit: old_data JSON -> old_* columns, rename columns to new_*
# ============================================================
print()
print('=== Migrating req_signer_limit ===')
old_lr = c.execute(
    'SELECT id, req_signer_id, action, signer_limit_id, old_data, '
    'territory_id, policy_id, limit_amount, approval_cc_id, exception, '
    'temp, temp_start_date, temp_end_date, business_rationale, business_control, '
    'account_restriction, currency '
    'FROM req_signer_limit ORDER BY id'
).fetchall()
print(f'  {len(old_lr)} rows to migrate')

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
    (lid, req_sid, action, sl_id, old_data_json,
     territory_id, policy_id, limit_amount, approval_cc_id, exception,
     temp, temp_start, temp_end, biz_rat, biz_ctrl, acct_restrict, currency) = lr

    # Parse old_data JSON
    if old_data_json:
        od = json.loads(old_data_json)
        o_territory = od.get('territory_id')
        o_policy = od.get('policy_id')
        o_limit = od.get('limit_amount')
        o_cc = od.get('approval_cc_id')
        o_exc = od.get('exception')
        o_temp = od.get('temp')
        o_temp_start = od.get('temp_start_date')
        o_temp_end = od.get('temp_end_date')
        o_biz_rat = od.get('business_rationale')
        o_biz_ctrl = od.get('business_control')
        o_acct = od.get('account_restriction')
        o_currency = od.get('currency')
    else:
        o_territory = o_policy = o_limit = o_cc = o_exc = o_temp = None
        o_temp_start = o_temp_end = o_biz_rat = o_biz_ctrl = o_acct = o_currency = None

    c.execute('INSERT INTO req_signer_limit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        (lid, req_sid, action, sl_id,
         o_territory, o_policy, o_limit, o_cc, o_exc, o_temp,
         o_temp_start, o_temp_end, o_biz_rat, o_biz_ctrl, o_acct, o_currency,
         territory_id, policy_id, limit_amount, approval_cc_id, exception,
         temp, temp_start, temp_end, biz_rat, biz_ctrl, acct_restrict, currency))

conn.commit()
print('  req_signer_limit migrated')

# ============================================================
# Verify
# ============================================================
print()
print('=== Verification ===')
print()
print('req_signer schema:')
for r in c.execute('PRAGMA table_info(req_signer)'):
    print(f'  {r}')
print()
print('req_signer_limit schema:')
for r in c.execute('PRAGMA table_info(req_signer_limit)'):
    print(f'  {r}')
print()

cnt1 = c.execute('SELECT COUNT(1) FROM req_signer').fetchone()[0]
cnt2 = c.execute('SELECT COUNT(1) FROM req_signer_limit').fetchone()[0]
print(f'req_signer: {cnt1} rows')
print(f'req_signer_limit: {cnt2} rows')

print()
print('=== Sample req_signer row ===')
r = c.execute('SELECT * FROM req_signer LIMIT 1').fetchone()
cols = [d[1] for d in c.execute('PRAGMA table_info(req_signer)').fetchall()]
for col, val in zip(cols, r):
    print(f'  {col}: {val}')

print()
print('=== Sample req_signer_limit (Change) ===')
r = c.execute("SELECT * FROM req_signer_limit WHERE action='Change' LIMIT 1").fetchone()
if r:
    cols = [d[1] for d in c.execute('PRAGMA table_info(req_signer_limit)').fetchall()]
    for col, val in zip(cols, r):
        print(f'  {col}: {val}')

print()
print('=== Sample req_signer_limit (Unchange) ===')
r = c.execute("SELECT * FROM req_signer_limit WHERE action='Unchange' LIMIT 1").fetchone()
if r:
    cols = [d[1] for d in c.execute('PRAGMA table_info(req_signer_limit)').fetchall()]
    for col, val in zip(cols, r):
        print(f'  {col}: {val}')

print()
print('=== Action distribution ===')
for r in c.execute("SELECT action, COUNT(1) FROM req_signer_limit GROUP BY action ORDER BY action"):
    print(f'  {r[0]}: {r[1]}')

conn.close()
print()
print('Done!')
