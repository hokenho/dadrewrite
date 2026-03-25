import sqlite3

conn = sqlite3.connect('db/data.db')
c = conn.cursor()

# Show current tables
tables = c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
print("=== Current tables ===")
for t in tables:
    print(f"  {t[0]}")

# Rename mapping
renames = {
    'user_profile': 'wd_user_profile',
    'job': 'wd_job_level',
    'territory': 'wd_territory',
    'policy': 'gdas_policy',
    'business_unit': 'infor_business_unit',
    'cost_center': 'infor_cost_center',
    'currency': 'infor_currency',
    'exchange_rate': 'infor_exchange_rate',
    'signer_req': 'req_signer',
    'signer_limit_req': 'req_signer_limit',
}

# Also rename signer_req_id column in signer_limit_req -> req_signer_limit
# SQLite ALTER TABLE RENAME TO
print("\n=== Renaming tables ===")
for old, new in renames.items():
    # Check if old table exists
    exists = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (old,)).fetchone()
    if exists:
        c.execute(f'ALTER TABLE [{old}] RENAME TO [{new}]')
        print(f"  {old} -> {new}")
    else:
        # Check if already renamed
        already = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (new,)).fetchone()
        if already:
            print(f"  {old} -> {new} (already done)")
        else:
            print(f"  {old} -> SKIPPED (not found)")

conn.commit()

# Verify
tables = c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
print("\n=== Tables after rename ===")
for t in tables:
    print(f"  {t[0]}")

conn.close()
print("\nDone.")
