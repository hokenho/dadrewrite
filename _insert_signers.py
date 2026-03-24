import sqlite3
import random

conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# Clear existing
c.execute('DELETE FROM signer')
c.execute('DELETE FROM signer_limit')

# Get lookup data
bu_ids = [r[0] for r in c.execute('SELECT id FROM business_unit').fetchall()]
terr_ids = [r[0] for r in c.execute('SELECT id FROM territory').fetchall()]
policy_ids = [r[0] for r in c.execute('SELECT id FROM policy').fetchall()]
cc_ids = [r[0] for r in c.execute('SELECT id FROM cost_center').fetchall()]

# Get existing user gad_ids from user_profile
gad_ids = [r[0] for r in c.execute('SELECT gad_id FROM user_profile').fetchall()]

# Generate additional dummy users to reach 50 signers
extra_names = [
    ('alex.martinez', 'Alex', 'Martinez'), ('beth.wong', 'Beth', 'Wong'),
    ('carl.davis', 'Carl', 'Davis'), ('debra.kumar', 'Debra', 'Kumar'),
    ('ethan.zhao', 'Ethan', 'Zhao'), ('fatima.ali', 'Fatima', 'Ali'),
    ('grant.miller', 'Grant', 'Miller'), ('heidi.nakamura', 'Heidi', 'Nakamura'),
    ('ian.robinson', 'Ian', 'Robinson'), ('jenny.park', 'Jenny', 'Park'),
    ('kevin.oshea', 'Kevin', "O'Shea"), ('lisa.fernandez', 'Lisa', 'Fernandez'),
    ('martin.lam', 'Martin', 'Lam'), ('nora.singh', 'Nora', 'Singh'),
    ('oliver.tan', 'Oliver', 'Tan'), ('priya.shah', 'Priya', 'Shah'),
    ('raymond.cheng', 'Raymond', 'Cheng'), ('sarah.bennett', 'Sarah', 'Bennett'),
    ('thomas.xu', 'Thomas', 'Xu'), ('uma.patel', 'Uma', 'Patel'),
    ('victor.leung', 'Victor', 'Leung'), ('wendy.scott', 'Wendy', 'Scott'),
    ('xavier.reyes', 'Xavier', 'Reyes'), ('yuki.tanaka', 'Yuki', 'Tanaka'),
    ('zara.ahmed', 'Zara', 'Ahmed'), ('adam.clark', 'Adam', 'Clark'),
    ('barbara.wu', 'Barbara', 'Wu'), ('chris.nguyen', 'Chris', 'Nguyen'),
    ('donna.li', 'Donna', 'Li'), ('frank.garcia', 'Frank', 'Garcia'),
]

# Insert extra users into user_profile
emp_base = 20000001
for i, (local, fn, ln) in enumerate(extra_names):
    gad = local + '@manulife.com'
    if gad not in gad_ids:
        cc_id = random.choice(cc_ids)
        job_id = random.randint(1, 10)
        terr_id = random.choice(terr_ids)
        c.execute('INSERT INTO user_profile (gad_id, employee_id, last_name, first_name, signer_cc_id, job_level_id, territory_id) VALUES (?,?,?,?,?,?,?)',
                  (gad, emp_base + i, ln, fn, cc_id, job_id, terr_id))
        gad_ids.append(gad)

# Pick 50 signers from all available gad_ids
random.seed(42)
signer_gad_ids = gad_ids[:50]

# Insert signers
for gad_id in signer_gad_ids:
    bu_id = random.choice(bu_ids)
    pickup = random.choice([0, 1])
    c.execute('INSERT INTO signer (gad_id, bu_id, pickup_cheque) VALUES (?,?,?)',
              (gad_id, bu_id, pickup))

# Insert signer_limit (1-4 limits per signer)
limit_id = 1
for gad_id in signer_gad_ids:
    num_limits = random.randint(1, 4)
    for _ in range(num_limits):
        terr_id = random.choice(terr_ids)
        pol_id = random.choice(policy_ids)
        amounts = [5000, 10000, 15000, 20000, 25000, 50000, 75000, 100000]
        amount = random.choice(amounts)
        cc_id = random.choice(cc_ids)
        exc = random.choice([0, 0, 0, 1])
        temp = random.choice([0, 0, 0, 1])
        br = random.choice([0, 0, 1])
        bc = random.choice([0, 0, 1])

        c.execute('''INSERT INTO signer_limit
            (id, territory_id, policy_id, limit_amount, approval_cc_id,
             exception, temporary, business_rationale, business_control,
             system_id, account_restriction, gad_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            (limit_id, terr_id, pol_id, amount, cc_id,
             exc, temp, br, bc, None, None, gad_id))
        limit_id += 1

conn.commit()

signer_cnt = c.execute('SELECT count(*) FROM signer').fetchone()[0]
limit_cnt = c.execute('SELECT count(*) FROM signer_limit').fetchone()[0]
profile_cnt = c.execute('SELECT count(*) FROM user_profile').fetchone()[0]
print(f'signer: {signer_cnt} rows')
print(f'signer_limit: {limit_cnt} rows')
print(f'user_profile: {profile_cnt} rows')

conn.close()
print('Done')
