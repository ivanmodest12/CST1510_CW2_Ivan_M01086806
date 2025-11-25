from ..data.db import connect_database

def migrate_users_from_file(file_path):
    conn = connect_database()
    count = 0
    with open(file_path, "r") as f:
        for line in f:
            username, password = line.strip().split(",")
            try:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                count += 1
            except:
                pass  # skip duplicates
    conn.commit()
    conn.close()
    return count
