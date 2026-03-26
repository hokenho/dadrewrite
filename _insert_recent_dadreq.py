import sqlite3

conn = sqlite3.connect("db/data.db")
cur = conn.cursor()

rows = [
    # 100051: pending approval1 (submitted today)
    (100051, "2026-03-26", "charlie.johnson@manulife.com", "frank.garcia@manulife.com", 1,
     "diana.lee@manulife.com", None, None, "ken.ho@manulife.com", None, None,
     1, 0, None, None, 1, 1, 0, None, None, 1, None),
    # 100052: pending approval2 (approval1 done, submitted yesterday)
    (100052, "2026-03-25", "eric.brown@manulife.com", "george.taylor@manulife.com", 2,
     "fatima.ali@manulife.com", 1, "Looks good", "julia.ng@manulife.com", None, None,
     0, 0, None, None, 1, 1, 0, None, None, 1, None),
    # 100053: pending approval1 (submitted 2 days ago)
    (100053, "2026-03-24", "hannah.ho@manulife.com", "ian.robinson@manulife.com", 3,
     "grant.miller@manulife.com", None, None, "martin.lam@manulife.com", None, None,
     1, 1, "2026-01-01", "2026-06-30", 1, 1, 0, None, None, 1, None),
    # 100054: pending approval2 (approval1 done, submitted 3 days ago)
    (100054, "2026-03-23", "jenny.park@manulife.com", "laura.chen@manulife.com", 1,
     "kevin.oshea@manulife.com", 1, "Approved", "nancy.yang@manulife.com", None, None,
     1, 0, None, None, 1, 1, 1, "2026-04-01", "2026-09-30", 1, None),
]

for r in rows:
    cur.execute("INSERT INTO req_signer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", r)

conn.commit()
print("Inserted 4 recent DADREQs:")
cur.execute("SELECT id, req_date, gad_id, approver1_result, approver2_result FROM req_signer WHERE id >= 100051")
for r in cur.fetchall():
    print(r)
conn.close()
