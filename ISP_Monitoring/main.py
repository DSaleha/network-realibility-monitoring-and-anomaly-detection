import time
import socket
import os
import sys
import config
import utils
import db_logger
import ping_check
import speed_check

def check_dns(domains, retries=3):
    if isinstance(domains, str): domains = [domains]
    for domain in domains:
        domain = domain.replace("'", "")
        for attempt in range(retries):
            try:
                socket.gethostbyname(domain)
                return True
            except:
                time.sleep(1)
    return False

def main():
    print("--- MEMULAI DIAGNOSTIC MONITOR ---")
    db_logger.init_db()
    
    # Setup folder cache
    if not os.path.exists(os.path.dirname(config.cache_path)):
        os.makedirs(os.path.dirname(config.cache_path))

    # Inisialisasi data awal
    last_speedtest_time = 0
    st_data = {"dl": 0, "ul": 0, "last_at": "--"}
    ping_spike_counter = 0

    print(f"Target: {config.ISP_NAME}")

    while True:
        try:
            current_time = time.time()
            final_status, interpretasi, tindakan = "UNKNOWN", "", ""
            latency_val = 0
            
            # --- 1. TAHAP DIAGNOSA PING ---
            r1_ok, r1_ms = ping_check.cek_koneksi(config.TARGETS['ROUTER_1'])
            r2_ok, r2_ms = ping_check.cek_koneksi(config.TARGETS['ROUTER_2'])
            
            if not (r1_ok or r2_ok):
                final_status, interpretasi = "INTERNET DOWN", "Router BMO Bermasalah"
                tindakan = "Cek koneksi kabel/listrik Access Point."
            else:
                fw_ok, fw_ms = ping_check.cek_koneksi(config.TARGETS['FIREWALL'])
                if not fw_ok:
                    final_status, interpretasi = "INTERNET DOWN", "Gangguan Firewall"
                    tindakan = "Cek kabel Firewall Softbank."
                    latency_val = (r1_ms + r2_ms) / 2
                else:
                    gw_ok, gw_ms = ping_check.cek_koneksi(config.TARGETS['GATEWAY'])
                    if not gw_ok:
                        final_status, interpretasi = "INTERNET DOWN", "Gangguan ISP Gedung"
                        tindakan = "Konfirmasi ke Biznet."
                        latency_val = fw_ms
                    else:
                        # Cek Internet Global
                        net_ms_list = [ping_check.cek_koneksi(t)[1] for t in config.TARGETS['INTERNET'] if ping_check.cek_koneksi(t)[0]]
                        net_ms = sum(net_ms_list) / len(net_ms_list) if net_ms_list else 0
                        
                        if not net_ms_list:
                            final_status, interpretasi = "INTERNET DOWN", "Akses Internet Terganggu"
                            tindakan = "Cek Routing Biznet"
                            latency_val = gw_ms
                        elif net_ms > 200:
                            ping_spike_counter += 1
                            final_status, interpretasi = ("INTERNET DOWN", "Latency Tinggi") if ping_spike_counter >= 3 else ("INTERNET NORMAL", "Jaringan Stabil")
                            tindakan = "Periksa beban bandwidth." if ping_spike_counter >= 3 else ""
                            latency_val = net_ms
                        else:
                            ping_spike_counter = 0
                            if not check_dns(config.TARGETS['WEBSITE']):
                                final_status, interpretasi = "INTERNET DEGRADED", "Akses Web Perusahaan Bermasalah"
                                tindakan = "Cek Web Jakarta Mori."
                                latency_val = net_ms
                            else:
                                final_status, interpretasi = "INTERNET NORMAL", "Jaringan Stabil"
                                latency_val = net_ms

            # --- 2. LOGIKA SPEEDTEST (Per 300 Detik) ---
            if (current_time - last_speedtest_time) >= config.SPEEDTEST_INTERVAL:
                print(f"\n[{utils.get_current_time()}] Menjalankan Speedtest...")
                hasil = speed_check.run_speed_test()
                if hasil:
                    st_data = {"dl": hasil['download_mbps'], "ul": hasil['upload_mbps'], "last_at": utils.get_current_time()}
                last_speedtest_time = current_time
                # Simpan log ke DB hanya saat speedtest terjadi
                db_logger.simpan_log(config.ISP_NAME, final_status, latency_val, st_data['dl'], st_data['ul'])

            # --- 3. DISPLAY & CACHE ---
            pi = utils.get_pi_status()
            sys.stdout.write(f"\r[{utils.get_current_time()}] {final_status} | {latency_val:.2f}ms | Temp: {pi['temp']}C")
            sys.stdout.flush()
            
            cache_data = {
                "status": final_status, "diagnosis": interpretasi, "action": tindakan,
                "last_ping": round(latency_val, 2), "last_dl": st_data['dl'],
                "last_ul": st_data['ul'], "last_speedtest_at": st_data['last_at']
            }
            utils.save_json(config.cache_path, cache_data)
            time.sleep(config.PING_INTERVAL)

        except Exception as e:
            print(f"\n[ERROR] {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
