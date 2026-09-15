import json
import shutil
import datetime
import os

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_json(path, data):
    backup_path = path + ".bak"

    if os.path.exists(path):
        shutil.copy(path, backup_path)

    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"[Utils] Failed to save JSON: {e}")
        return False
    
def load_json(path):
    backup_path = path + ".bak"

    if not os.path.exists(path):
        return {}
    
    try:
        with open(path, "r") as f:
            return json.load(f)
        
    except json.JSONDecodeError:
        print("[Utils] JSON corrupt. Attempting restore from backup...")

        #restore kalo backup ada
        if os.path.exists(backup_path):
                try:
                    shutil.copy(backup_path, path)
                    print("[Utils] Backup restored.")
                    with open(path, "r") as f:
                        return json.load(f)
                except:
                    print(f"[Utils] Backup also corrupt.")
                    return {}
        
        #kalo backup gak ada
        print("[Utils] No backup available.")
        return{}

    except Exception as e:
        print(f"[Utils] Unexpected load error: {e}")
        return {}
    
def get_pi_status():
    status = {"temp": 0, "disk_percent": 0}
    try:
        total, used, free = shutil.disk_usage("/")
        status["disk_percent"] = round((used / total) * 100, 1)
    except:
        pass

    #cek suhu di Linux/ Rpi
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_raw = f.read()
            status["temp"] = round(int(temp_raw) / 1000, 1)
    except:
        status["temp"] = -1

    return status
