import sqlite3
import json

conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# ============================================================
# 1. Migrate user_access_temp -> user_access
# ============================================================
c.execute('DELETE FROM user_access')
c.execute('INSERT INTO user_access (id, access) SELECT gad_id, access FROM user_access_temp')
print(f'user_access: migrated {c.rowcount} rows')

# ============================================================
# 2. Create user_profile entries for all unique users
# ============================================================
# Collect names from user_access_temp
ua_names = {}
for r in c.execute('SELECT gad_id, first_name, last_name FROM user_access_temp'):
    ua_names[r[0]] = (r[1], r[2])

# Generate names from email for users not in user_access_temp
extra_names = {
    'ken.ho@manulife.com': ('Ken', 'Ho'),
    'laura.chen@manulife.com': ('Laura', 'Chen'),
    'mike.thomas@manulife.com': ('Mike', 'Thomas'),
    'nancy.yang@manulife.com': ('Nancy', 'Yang'),
    'oscar.jackson@manulife.com': ('Oscar', 'Jackson'),
    'patricia.wu@manulife.com': ('Patricia', 'Wu'),
    'quinn.white@manulife.com': ('Quinn', 'White'),
    'rachel.liu@manulife.com': ('Rachel', 'Liu'),
    'sam.harris@manulife.com': ('Sam', 'Harris'),
    'tina.kim@manulife.com': ('Tina', 'Kim'),
}
all_names = {**ua_names, **extra_names}

# Collect all unique users
users = set()
for r in c.execute('SELECT submitter, submittedFor FROM dadreq'):
    users.add(r[0])
    users.add(r[1])
for r in c.execute('SELECT gad_id FROM user_access_temp'):
    users.add(r[0])

c.execute('DELETE FROM user_profile')
emp_id = 10000001
for i, gad_id in enumerate(sorted(users)):
    first, last = all_names.get(gad_id, ('Unknown', 'User'))
    c.execute('INSERT INTO user_profile (gad_id, employee_id, last_name, first_name) VALUES (?,?,?,?)',
              (gad_id, emp_id + i, last, first))
print(f'user_profile: inserted {len(users)} rows')

# ============================================================
# 3. Add dadreq_id column to dadreq_limit_open (for 1:many link)
# ============================================================
existing_cols = [col[1] for col in c.execute('PRAGMA table_info(dadreq_limit_open)').fetchall()]
if 'dadreq_id' not in existing_cols:
    c.execute('ALTER TABLE dadreq_limit_open ADD COLUMN dadreq_id INTEGER')
    print('dadreq_limit_open: added dadreq_id column')

# ============================================================
# 4. Migrate dadreq (Open) -> dadreq_open + dadreq_limit_open
# ============================================================
c.execute('DELETE FROM dadreq_open')
c.execute('DELETE FROM dadreq_limit_open')

open_rows = c.execute(
    "SELECT reqId, date, submitter, submittedFor, reason, profile, limits FROM dadreq WHERE status = 'Open'"
).fetchall()

# Territory code -> id lookup
terr_map = {}
for r in c.execute('SELECT id, country_code FROM territory'):
    terr_map[r[1]] = r[0]

# Cost center cc -> id lookup
cc_map = {}
for r in c.execute('SELECT id, cc FROM cost_center'):
    cc_map[r[1]] = r[0]

limit_id = 1
for row in open_rows:
    req_id_num = int(row[0].replace('DADREQ', ''))
    gad_id = row[3]      # submittedFor
    req_date = row[1]
    submitter = row[2]
    limits_json = json.loads(row[6] or '[]')

    c.execute('INSERT INTO dadreq_open (id, gad_id, req_date, submitter, [limit]) VALUES (?,?,?,?,NULL)',
              (req_id_num, gad_id, req_date, submitter))

    for lim in limits_json:
        action_map = {'update': 'Change', 'delete': 'Remove', 'new': 'Add'}
        action = action_map.get(lim.get('type', ''), lim.get('type', ''))
        source_id = lim.get('rowIndex')

        # Parse newData if present: [territory, policy_cat, amount, currency, cc, exc, temp, br, bc, system, acct]
        nd = lim.get('newData', [])
        territory_id = terr_map.get(nd[0]) if len(nd) > 0 else None
        limit_amount = float(nd[2].replace(',', '')) if len(nd) > 2 and nd[2] else None
        approval_cc_id = cc_map.get(nd[4]) if len(nd) > 4 else None
        exception = 1 if (len(nd) > 5 and nd[5] == 'Y') else 0
        temporary = 1 if (len(nd) > 6 and nd[6] == 'Y') else 0
        biz_rationale = 1 if (len(nd) > 7 and nd[7] == 'Y') else 0
        biz_control = 1 if (len(nd) > 8 and nd[8] == 'Y') else 0

        c.execute('''INSERT INTO dadreq_limit_open
            (id, action, source_id, territory_id, policy_id, limit_amount, approval_cc_id,
             exception, temporary, business_rationale, business_control, system_id, account_restriction, dadreq_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (limit_id, action, source_id, territory_id, None, limit_amount, approval_cc_id,
             exception, temporary, biz_rationale, biz_control, None, None, req_id_num))
        limit_id += 1

print(f'dadreq_open: inserted {len(open_rows)} rows')
print(f'dadreq_limit_open: inserted {limit_id - 1} rows')

# ============================================================
# 5. Migrate dadreq (Complete/Reject/Cancel) -> audit_dadreq
# ============================================================
c.execute('DELETE FROM audit_dadreq')

closed_rows = c.execute(
    "SELECT reqId, date, submitter, submittedFor, status, reason, profile, limits FROM dadreq WHERE status != 'Open'"
).fetchall()

for i, row in enumerate(closed_rows):
    req_id = row[0]
    data_new = json.dumps({'profile': json.loads(row[6] or '{}'), 'limits': json.loads(row[7] or '[]')})
    c.execute('''INSERT INTO audit_dadreq (id, gad_id, req_date, submitter, status, reason, data_old, data_new, audit_date)
                 VALUES (?,?,?,?,?,?,?,?,?)''',
              (i + 1, row[3], row[1], row[2], row[4], row[5], None, data_new, row[1]))

print(f'audit_dadreq: inserted {len(closed_rows)} rows')

conn.commit()

# ============================================================
# Verify
# ============================================================
print('\n=== Verification ===')
for tbl in ['user_profile', 'user_access', 'dadreq_open', 'dadreq_limit_open', 'audit_dadreq']:
    cnt = c.execute(f'SELECT count(*) FROM [{tbl}]').fetchone()[0]
    print(f'  {tbl}: {cnt} rows')

conn.close()
print('\nMigration complete.')
