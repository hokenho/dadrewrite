import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# Drop old audit_change table
c.execute("DROP TABLE IF EXISTS audit_change")
print("Dropped audit_change table")

# ============================================================
# Create all 11 audit tables
# ============================================================

c.execute("""CREATE TABLE IF NOT EXISTS audit_wd_user_profile (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_employee_id INTEGER,
    old_last_name TEXT,
    old_first_name TEXT,
    old_signer_cost_center TEXT,
    old_job_grade TEXT,
    old_job_title TEXT,
    old_limit_amount_max INTEGER,
    old_country_code TEXT,
    old_territory TEXT,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_employee_id INTEGER,
    new_last_name TEXT,
    new_first_name TEXT,
    new_signer_cost_center TEXT,
    new_job_grade TEXT,
    new_job_title TEXT,
    new_limit_amount_max INTEGER,
    new_country_code TEXT,
    new_territory TEXT,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_wd_job_level (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_job_grade TEXT,
    old_job_title TEXT,
    old_limit_amount_max INTEGER,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_job_grade TEXT,
    new_job_title TEXT,
    new_limit_amount_max INTEGER,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_wd_territory (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_country_code TEXT,
    old_territory TEXT,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_country_code TEXT,
    new_territory TEXT,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_gdas_policy (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_country_code TEXT,
    old_category TEXT,
    old_description TEXT,
    old_system TEXT,
    old_approval_count INTEGER,
    old_threshold_amount REAL,
    old_manual_approval INTEGER,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_country_code TEXT,
    new_category TEXT,
    new_description TEXT,
    new_system TEXT,
    new_approval_count INTEGER,
    new_threshold_amount REAL,
    new_manual_approval INTEGER,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_infor_business_unit (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_security_group TEXT,
    old_name TEXT,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_security_group TEXT,
    new_name TEXT,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_infor_cost_center (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_name TEXT,
    old_description TEXT,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_name TEXT,
    new_description TEXT,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_infor_currency (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_name TEXT,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_name TEXT,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_infor_exchange_rate (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_source_currency TEXT,
    old_target_currency TEXT,
    old_plan_rate REAL,
    old_status INTEGER,
    old_last_update_date TEXT,
    new_source_currency TEXT,
    new_target_currency TEXT,
    new_plan_rate REAL,
    new_status INTEGER,
    new_last_update_date TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_user_access (
    id INTEGER PRIMARY KEY,
    record_id TEXT,
    action TEXT,
    old_access TEXT,
    new_access TEXT,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_signer (
    id INTEGER PRIMARY KEY,
    gad_id TEXT,
    action TEXT,
    old_bu_security_group TEXT,
    old_bu_name TEXT,
    old_pickup_cheque INTEGER,
    old_temp INTEGER,
    old_temp_start_date TEXT,
    old_temp_end_date TEXT,
    old_status INTEGER,
    new_bu_security_group TEXT,
    new_bu_name TEXT,
    new_pickup_cheque INTEGER,
    new_temp INTEGER,
    new_temp_start_date TEXT,
    new_temp_end_date TEXT,
    new_status INTEGER,
    change_by TEXT,
    change_date TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS audit_signer_limit (
    id INTEGER PRIMARY KEY,
    signer_limit_id TEXT,
    gad_id TEXT,
    action TEXT,
    old_country_code TEXT,
    old_territory TEXT,
    old_policy_country_code TEXT,
    old_policy_category TEXT,
    old_policy_description TEXT,
    old_policy_system TEXT,
    old_policy_approval_count INTEGER,
    old_policy_threshold_amount REAL,
    old_policy_manual_approval INTEGER,
    old_limit_amount REAL,
    old_cc_name TEXT,
    old_cc_description TEXT,
    old_exception INTEGER,
    old_temp INTEGER,
    old_temp_start_date TEXT,
    old_temp_end_date TEXT,
    old_business_rationale INTEGER,
    old_business_control INTEGER,
    old_account_restriction TEXT,
    old_currency TEXT,
    new_country_code TEXT,
    new_territory TEXT,
    new_policy_country_code TEXT,
    new_policy_category TEXT,
    new_policy_description TEXT,
    new_policy_system TEXT,
    new_policy_approval_count INTEGER,
    new_policy_threshold_amount REAL,
    new_policy_manual_approval INTEGER,
    new_limit_amount REAL,
    new_cc_name TEXT,
    new_cc_description TEXT,
    new_exception INTEGER,
    new_temp INTEGER,
    new_temp_start_date TEXT,
    new_temp_end_date TEXT,
    new_business_rationale INTEGER,
    new_business_control INTEGER,
    new_account_restriction TEXT,
    new_currency TEXT,
    change_by TEXT,
    change_date TEXT
)""")

print("Created all 11 audit tables")

# ============================================================
# Helper data for realistic dummy rows
# ============================================================
random.seed(42)

actions = ['INSERT', 'UPDATE', 'DELETE']
action_weights = [20, 70, 10]  # mostly updates

admins = ['admin.user', 'john.smith', 'jane.doe', 'system.sync', 'mary.johnson']
gad_ids = [f"user{i:03d}.test" for i in range(1, 31)]
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'David', 'Elizabeth']
cost_centers = ['CC-100', 'CC-200', 'CC-300', 'CC-400', 'CC-500', 'CC-600']
job_grades = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8']
job_titles = ['Analyst', 'Senior Analyst', 'Manager', 'Senior Manager', 'Director', 'VP', 'SVP', 'Associate']
country_codes = ['JP', 'US', 'SG', 'HK', 'AU', 'GB', 'DE', 'FR']
territories = ['Japan', 'United States', 'Singapore', 'Hong Kong', 'Australia', 'United Kingdom', 'Germany', 'France']
categories = ['Travel', 'Procurement', 'IT Services', 'Consulting', 'Marketing']
descriptions_policy = ['Travel expense approval', 'Purchase order approval', 'IT service request', 'Consulting engagement', 'Marketing spend']
systems = ['AP', 'SNOW', 'Concur']
security_groups = ['SG-APAC', 'SG-EMEA', 'SG-AMER', 'SG-GLOBAL']
bu_names = ['APAC Operations', 'EMEA Operations', 'Americas Operations', 'Global Services', 'Corporate']
cc_names = ['Finance', 'IT', 'HR', 'Operations', 'Marketing', 'Sales', 'Legal', 'R&D']
cc_descs = ['Finance Department', 'Information Technology', 'Human Resources', 'Operations Team', 'Marketing Division', 'Sales Division', 'Legal Affairs', 'Research and Development']
currencies = ['USD', 'JPY', 'SGD', 'HKD', 'AUD', 'GBP', 'EUR']
currency_names = ['US Dollar', 'Japanese Yen', 'Singapore Dollar', 'Hong Kong Dollar', 'Australian Dollar', 'British Pound', 'Euro']
access_levels = ['admin', 'viewer', 'submitter', 'approver']
account_restrictions = ['None', 'AP Only', 'GL Only', 'AP+GL', 'Restricted']

def rand_date(start_year=2025, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).strftime('%Y-%m-%d')

def pick_action():
    return random.choices(actions, weights=action_weights, k=1)[0]

# For INSERT: old_* = None; For DELETE: new_* = None; For UPDATE: both populated
# ============================================================
# Insert 100 dummy rows per table
# ============================================================

# 1. audit_wd_user_profile
for i in range(1, 101):
    action = pick_action()
    gad = random.choice(gad_ids)
    cd = rand_date()
    emp_old = random.randint(10000, 99999)
    emp_new = random.randint(10000, 99999)
    ln_old, ln_new = random.choice(last_names), random.choice(last_names)
    fn_old, fn_new = random.choice(first_names), random.choice(first_names)
    cc_old, cc_new = random.choice(cost_centers), random.choice(cost_centers)
    jg_old, jg_new = random.choice(job_grades), random.choice(job_grades)
    jt_old, jt_new = random.choice(job_titles), random.choice(job_titles)
    lam_old, lam_new = random.randint(1000, 50000), random.randint(1000, 50000)
    cidx = random.randint(0, len(country_codes)-1)
    cidx2 = random.randint(0, len(country_codes)-1)
    cc_o, t_o = country_codes[cidx], territories[cidx]
    cc_n, t_n = country_codes[cidx2], territories[cidx2]
    st_old, st_new = random.randint(0,1), random.randint(0,1)
    lud_old, lud_new = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_wd_user_profile VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, gad, action, None,None,None,None,None,None,None,None,None,None,None, emp_new,ln_new,fn_new,cc_new,jg_new,jt_new,lam_new,cc_n,t_n,st_new,lud_new, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_wd_user_profile VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, gad, action, emp_old,ln_old,fn_old,cc_old,jg_old,jt_old,lam_old,cc_o,t_o,st_old,lud_old, None,None,None,None,None,None,None,None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_wd_user_profile VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, gad, action, emp_old,ln_old,fn_old,cc_old,jg_old,jt_old,lam_old,cc_o,t_o,st_old,lud_old, emp_new,ln_new,fn_new,cc_new,jg_new,jt_new,lam_new,cc_n,t_n,st_new,lud_new, random.choice(admins), cd))
print("Inserted 100 rows into audit_wd_user_profile")

# 2. audit_wd_job_level
for i in range(1, 101):
    action = pick_action()
    rec = str(random.randint(1, 20))
    cd = rand_date()
    jg_o, jg_n = random.choice(job_grades), random.choice(job_grades)
    jt_o, jt_n = random.choice(job_titles), random.choice(job_titles)
    lam_o, lam_n = random.randint(1000, 50000), random.randint(1000, 50000)
    st_o, st_n = random.randint(0,1), random.randint(0,1)
    lud_o, lud_n = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_wd_job_level VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, None,None,None,None,None, jg_n,jt_n,lam_n,st_n,lud_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_wd_job_level VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, jg_o,jt_o,lam_o,st_o,lud_o, None,None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_wd_job_level VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, jg_o,jt_o,lam_o,st_o,lud_o, jg_n,jt_n,lam_n,st_n,lud_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_wd_job_level")

# 3. audit_wd_territory
for i in range(1, 101):
    action = pick_action()
    rec = str(random.randint(1, 15))
    cd = rand_date()
    cidx1, cidx2 = random.randint(0, len(country_codes)-1), random.randint(0, len(country_codes)-1)
    st_o, st_n = random.randint(0,1), random.randint(0,1)
    lud_o, lud_n = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_wd_territory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, None,None,None,None, country_codes[cidx2],territories[cidx2],st_n,lud_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_wd_territory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, country_codes[cidx1],territories[cidx1],st_o,lud_o, None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_wd_territory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, country_codes[cidx1],territories[cidx1],st_o,lud_o, country_codes[cidx2],territories[cidx2],st_n,lud_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_wd_territory")

# 4. audit_gdas_policy
for i in range(1, 101):
    action = pick_action()
    rec = str(random.randint(1, 30))
    cd = rand_date()
    cidx1, cidx2 = random.randint(0, len(country_codes)-1), random.randint(0, len(country_codes)-1)
    pidx1, pidx2 = random.randint(0, len(categories)-1), random.randint(0, len(categories)-1)
    sys_o, sys_n = random.choice(systems), random.choice(systems)
    ac_o, ac_n = random.randint(1,3), random.randint(1,3)
    ta_o, ta_n = random.randint(1000, 100000), random.randint(1000, 100000)
    ma_o, ma_n = random.randint(0,1), random.randint(0,1)
    st_o, st_n = random.randint(0,1), random.randint(0,1)
    lud_o, lud_n = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_gdas_policy VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, None,None,None,None,None,None,None,None,None, country_codes[cidx2],categories[pidx2],descriptions_policy[pidx2],sys_n,ac_n,ta_n,ma_n,st_n,lud_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_gdas_policy VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, country_codes[cidx1],categories[pidx1],descriptions_policy[pidx1],sys_o,ac_o,ta_o,ma_o,st_o,lud_o, None,None,None,None,None,None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_gdas_policy VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, country_codes[cidx1],categories[pidx1],descriptions_policy[pidx1],sys_o,ac_o,ta_o,ma_o,st_o,lud_o, country_codes[cidx2],categories[pidx2],descriptions_policy[pidx2],sys_n,ac_n,ta_n,ma_n,st_n,lud_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_gdas_policy")

# 5. audit_infor_business_unit
for i in range(1, 101):
    action = pick_action()
    rec = str(random.randint(1, 10))
    cd = rand_date()
    sg_o, sg_n = random.choice(security_groups), random.choice(security_groups)
    bn_o, bn_n = random.choice(bu_names), random.choice(bu_names)
    st_o, st_n = random.randint(0,1), random.randint(0,1)
    lud_o, lud_n = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_infor_business_unit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, None,None,None,None, sg_n,bn_n,st_n,lud_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_infor_business_unit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, sg_o,bn_o,st_o,lud_o, None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_infor_business_unit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, sg_o,bn_o,st_o,lud_o, sg_n,bn_n,st_n,lud_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_infor_business_unit")

# 6. audit_infor_cost_center
for i in range(1, 101):
    action = pick_action()
    rec = str(random.randint(1, 15))
    cd = rand_date()
    cidx1, cidx2 = random.randint(0, len(cc_names)-1), random.randint(0, len(cc_names)-1)
    st_o, st_n = random.randint(0,1), random.randint(0,1)
    lud_o, lud_n = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_infor_cost_center VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, None,None,None,None, cc_names[cidx2],cc_descs[cidx2],st_n,lud_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_infor_cost_center VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, cc_names[cidx1],cc_descs[cidx1],st_o,lud_o, None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_infor_cost_center VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, cc_names[cidx1],cc_descs[cidx1],st_o,lud_o, cc_names[cidx2],cc_descs[cidx2],st_n,lud_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_infor_cost_center")

# 7. audit_infor_currency
for i in range(1, 101):
    action = pick_action()
    cidx = random.randint(0, len(currencies)-1)
    rec = currencies[cidx]
    cd = rand_date()
    nidx1, nidx2 = random.randint(0, len(currency_names)-1), random.randint(0, len(currency_names)-1)
    st_o, st_n = random.randint(0,1), random.randint(0,1)
    lud_o, lud_n = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_infor_currency VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, None,None,None, currency_names[nidx2],st_n,lud_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_infor_currency VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, currency_names[nidx1],st_o,lud_o, None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_infor_currency VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, currency_names[nidx1],st_o,lud_o, currency_names[nidx2],st_n,lud_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_infor_currency")

# 8. audit_infor_exchange_rate
for i in range(1, 101):
    action = pick_action()
    src = random.choice(currencies)
    tgt = random.choice([c for c in currencies if c != src])
    rec = f"{src}|{tgt}"
    cd = rand_date()
    pr_o, pr_n = round(random.uniform(0.5, 150.0), 4), round(random.uniform(0.5, 150.0), 4)
    st_o, st_n = random.randint(0,1), random.randint(0,1)
    lud_o, lud_n = rand_date(), rand_date()

    if action == 'INSERT':
        c.execute("INSERT INTO audit_infor_exchange_rate VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, None,None,None,None,None, src,tgt,pr_n,st_n,lud_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_infor_exchange_rate VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, src,tgt,pr_o,st_o,lud_o, None,None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_infor_exchange_rate VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, rec, action, src,tgt,pr_o,st_o,lud_o, src,tgt,pr_n,st_n,lud_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_infor_exchange_rate")

# 9. audit_user_access
for i in range(1, 101):
    action = pick_action()
    rec = random.choice(gad_ids)
    cd = rand_date()
    acc_o, acc_n = random.choice(access_levels), random.choice(access_levels)

    if action == 'INSERT':
        c.execute("INSERT INTO audit_user_access VALUES (?,?,?,?,?,?,?)",
            (i, rec, action, None, acc_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_user_access VALUES (?,?,?,?,?,?,?)",
            (i, rec, action, acc_o, None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_user_access VALUES (?,?,?,?,?,?,?)",
            (i, rec, action, acc_o, acc_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_user_access")

# 10. audit_signer
for i in range(1, 101):
    action = pick_action()
    gad = random.choice(gad_ids)
    cd = rand_date()
    sg_o, sg_n = random.choice(security_groups), random.choice(security_groups)
    bn_o, bn_n = random.choice(bu_names), random.choice(bu_names)
    pc_o, pc_n = random.randint(0,1), random.randint(0,1)
    tmp_o, tmp_n = random.randint(0,1), random.randint(0,1)
    tsd_o = rand_date() if tmp_o else None
    ted_o = rand_date() if tmp_o else None
    tsd_n = rand_date() if tmp_n else None
    ted_n = rand_date() if tmp_n else None
    st_o, st_n = random.randint(0,1), random.randint(0,1)

    if action == 'INSERT':
        c.execute("INSERT INTO audit_signer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, gad, action, None,None,None,None,None,None,None, sg_n,bn_n,pc_n,tmp_n,tsd_n,ted_n,st_n, random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_signer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, gad, action, sg_o,bn_o,pc_o,tmp_o,tsd_o,ted_o,st_o, None,None,None,None,None,None,None, random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_signer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (i, gad, action, sg_o,bn_o,pc_o,tmp_o,tsd_o,ted_o,st_o, sg_n,bn_n,pc_n,tmp_n,tsd_n,ted_n,st_n, random.choice(admins), cd))
print("Inserted 100 rows into audit_signer")

# 11. audit_signer_limit
for i in range(1, 101):
    action = pick_action()
    sl_id = str(random.randint(1, 50))
    gad = random.choice(gad_ids)
    cd = rand_date()
    cidx1, cidx2 = random.randint(0, len(country_codes)-1), random.randint(0, len(country_codes)-1)
    pidx1, pidx2 = random.randint(0, len(categories)-1), random.randint(0, len(categories)-1)
    sys_o, sys_n = random.choice(systems), random.choice(systems)
    ac_o, ac_n = random.randint(1,3), random.randint(1,3)
    ta_o, ta_n = random.randint(1000, 100000), random.randint(1000, 100000)
    ma_o, ma_n = random.randint(0,1), random.randint(0,1)
    la_o, la_n = random.randint(500, 50000), random.randint(500, 50000)
    ccidx1, ccidx2 = random.randint(0, len(cc_names)-1), random.randint(0, len(cc_names)-1)
    ex_o, ex_n = random.randint(0,1), random.randint(0,1)
    tmp_o, tmp_n = random.randint(0,1), random.randint(0,1)
    tsd_o = rand_date() if tmp_o else None
    ted_o = rand_date() if tmp_o else None
    tsd_n = rand_date() if tmp_n else None
    ted_n = rand_date() if tmp_n else None
    br_o, br_n = random.randint(0,1), random.randint(0,1)
    bc_o, bc_n = random.randint(0,1), random.randint(0,1)
    ar_o, ar_n = random.choice(account_restrictions), random.choice(account_restrictions)
    cur_o, cur_n = random.choice(currencies), random.choice(currencies)

    old_vals = (country_codes[cidx1],territories[cidx1], country_codes[cidx1],categories[pidx1],descriptions_policy[pidx1],sys_o,ac_o,ta_o,ma_o, la_o, cc_names[ccidx1],cc_descs[ccidx1], ex_o,tmp_o,tsd_o,ted_o,br_o,bc_o,ar_o,cur_o)
    new_vals = (country_codes[cidx2],territories[cidx2], country_codes[cidx2],categories[pidx2],descriptions_policy[pidx2],sys_n,ac_n,ta_n,ma_n, la_n, cc_names[ccidx2],cc_descs[ccidx2], ex_n,tmp_n,tsd_n,ted_n,br_n,bc_n,ar_n,cur_n)
    null_vals = tuple([None]*20)

    if action == 'INSERT':
        c.execute("INSERT INTO audit_signer_limit VALUES (?,?,?,?," + ",".join(["?"]*20) + "," + ",".join(["?"]*20) + ",?,?)",
            (i, sl_id, gad, action) + null_vals + new_vals + (random.choice(admins), cd))
    elif action == 'DELETE':
        c.execute("INSERT INTO audit_signer_limit VALUES (?,?,?,?," + ",".join(["?"]*20) + "," + ",".join(["?"]*20) + ",?,?)",
            (i, sl_id, gad, action) + old_vals + null_vals + (random.choice(admins), cd))
    else:
        c.execute("INSERT INTO audit_signer_limit VALUES (?,?,?,?," + ",".join(["?"]*20) + "," + ",".join(["?"]*20) + ",?,?)",
            (i, sl_id, gad, action) + old_vals + new_vals + (random.choice(admins), cd))
print("Inserted 100 rows into audit_signer_limit")

conn.commit()

# Verify
print("\n=== Verification ===")
audit_tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'audit_%' ORDER BY name").fetchall()]
for t in audit_tables:
    count = c.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
    print(f"  {t}: {count} rows")

conn.close()
print("\nDone!")
