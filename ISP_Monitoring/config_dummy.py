import os

TARGETS = {
    #1. Router Internal
    #"ROUTER_1": "192.xxx.x.xxx",  
    #"ROUTER_2": "192.xxx.x.xxx",  

    #2. Router Firewall
    #"FIREWALL": "192.xxx.x.xxx", 
    
    #3. MDF
    #"GATEWAY": "xxx.xxx.xx.xxx", 
    
    #4. Internet Umum (Google DNS)
    "INTERNET": ['8.8.8.8', '1.1.1.1', '9.9.9.9'], #tambah cloudflare & quad9
    
    #5. Cek koneksi ke website
    "WEBSITE": ["google.com", "microsoft.com", "wikipedia.com", "github.com"]
} 

# Info Display
ISP_NAME = "MID Biznet Dedicated" 
COMMITTED_BANDWIDTH = "xx" #Mbps, sesuai kontrak SLA utk UI
 
# Interval
PING_INTERVAL = 5   #Detik
SPEEDTEST_INTERVAL = 300 #5 Menit

#path handling
base_dir = os.path.dirname(os.path.abspath(__file__))
#gabung agar aman saat running di cron/ systemd
cache_path = os.path.join(base_dir, "cache", "last_result.json")
db_path = os.path.join(base_dir, "logs", "history.sqlite")
