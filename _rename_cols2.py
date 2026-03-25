import sqlite3
conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# 1. req_signer: source_data -> old_data
c.execute('ALTER TABLE req_signer RENAME COLUMN source_data TO old_data')
print('req_signer: source_data -> old_data')

# 2. req_signer_limit: source_id -> signer_limit_id
c.execute('ALTER TABLE req_signer_limit RENAME COLUMN source_id TO signer_limit_id')
print('req_signer_limit: source_id -> signer_limit_id')

# 3. req_signer_limit: source_data -> old_data
c.execute('ALTER TABLE req_signer_limit RENAME COLUMN source_data TO old_data')
print('req_signer_limit: source_data -> old_data')

# 4. gdas_policy: country -> country_code
c.execute('ALTER TABLE gdas_policy RENAME COLUMN country TO country_code')
print('gdas_policy: country -> country_code')

conn.commit()

# Verify
print('\n=== Verification ===')
for tbl in ['req_signer', 'req_signer_limit', 'gdas_policy']:
    cols = [r[1] for r in c.execute(f'PRAGMA table_info({tbl})')]
    print(f'  {tbl}: {cols}')

conn.close()
print('\nDone!')
