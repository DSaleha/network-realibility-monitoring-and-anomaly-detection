import time
from ping3 import ping
from config import ISP_NAME 

#ping 3x repitisi per target
#Return: (Status_Boolean, Latency_ms)
def cek_koneksi(target_ip, retries=3):
    for attempt in range(retries):
        try:
            respon_detik = ping(target_ip, timeout=2)#ambil datanya dulu
            #jika RTO (None) atau Error DNS (False), kita abaikan dan lanjut loop ke target berikutnya
            if respon_detik is not None and respon_detik is not False:
                latency_ms = round(respon_detik * 1000, 2)
                return True, latency_ms
        
        except Exception as e:
            pass #tetap diam agar terminal tidak spam eror
        
        time.sleep(1) #jeda 1 detik sebelum ping ulang
    return False, 0
    
#--- TESTING AREA ---
if __name__ == "__main__":
    print("--- Test Ping Manual ---")
    
    #ambil IP target pertama dari config
    target_test = ISP[0]["ping_target"]
    print(f"Mencoba ping ke {target_test} ...")

    #panggil fungsi
    status, latency = cek_koneksi(target_test)

    if status:
        print(f"Status: OK | Latency: {latency} ms") 
    else:
        print("Status: OFF")
