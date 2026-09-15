import sqlite3
import datetime
import os
import config 

def init_db():
    folder_logs = os.path.dirname(config.db_path)
    if not os.path.exists(folder_logs):
        os.makedirs(folder_logs)
        print(f"[DB] Folder dibuat: {folder_logs}")

    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    query_tabel = """
    CREATE TABLE IF NOT EXISTS monitoring_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        waktu TEXT,
        isp_name TEXT,
        status TEXT,
        ping_ms REAL,
        download_mbps REAL,
        upload_mbps REAL
    )
    """
    cursor.execute(query_tabel)
    conn.commit()
    conn.close()
    print("[DB] Database siap digunakan.")

# UBAH BATCH SIZE JADI 1
BATCH_SIZE = 1  
MAX_ROWS = 1000  
_log_cache = []  

def simpan_log(isp_name, status, ping=0, dl=0, ul=0):
    global _log_cache
    try:
        waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _log_cache.append((waktu_sekarang, isp_name, status, ping, dl, ul))

        # Karena BATCH_SIZE = 1, ini akan selalu dieksekusi langsung
        if len(_log_cache) >= BATCH_SIZE:
            conn = sqlite3.connect(config.db_path)
            cursor = conn.cursor()
            
            query_insert = """
            INSERT INTO monitoring_logs 
            (waktu, isp_name, status, ping_ms, download_mbps, upload_mbps)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.executemany(query_insert, _log_cache)

            # Batasi maksimal row (Tertimpa)
            cursor.execute(f"""
                DELETE FROM monitoring_logs 
                WHERE id NOT IN (
                    SELECT id FROM monitoring_logs 
                    ORDER BY id DESC 
                    LIMIT {MAX_ROWS}
                )
            """)

            conn.commit()
            conn.close()
            
            _log_cache = []  # Kosongkan cache
            print(f"[DB] 1 Data Log Event tersimpan permanen.")

    except Exception as e:
        print(f"[ERROR DB] Gagal simpan log: {e}")

if __name__ == "__main__":
    init_db()