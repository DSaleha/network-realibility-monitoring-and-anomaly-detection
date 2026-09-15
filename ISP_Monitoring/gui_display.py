import tkinter as tk
import config
import utils

# KONFIGURASI WARNA (LIGHT MODE)
COLORS = {
    "BG": "#FFFFFF",           
    "TEXT_MAIN": "#333333",    
    "TEXT_SUB": "#666666",     
    "NORMAL": "#28a745",       
    "WARNING": "#FFDE4D",      
    "CRITICAL": "#E35167",     
    "BIZNET_BLUE": "#005baa"   
}

FONT_MAIN = "Segoe UI"

class MonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("INTERNET NETWORK MONITORING")
        self.attributes('-fullscreen', True)
        self.configure(bg=COLORS["BG"])
        self.bind("<Escape>", lambda e: self.destroy())
        
        # Simpan reference logo biar gak dihapus oleh Garbage Collector
        self.logo_img = None 
        
        self.build_ui()
        self.update_ui()

    def build_ui(self):
        # --- HEADER FRAME ---
        # Pakai fill=tk.X biar header membentang dari kiri ke kanan
        frame_header = tk.Frame(self, bg=COLORS["BG"])
        frame_header.pack(fill=tk.X, padx=25, pady=15)
        
        # Kiri: Logo & Realtime
        frame_kiri = tk.Frame(frame_header, bg=COLORS["BG"])
        frame_kiri.pack(side=tk.LEFT)
        
        # LOGIC UNTUK LOGO BIZNET 
        try:
            # subsample(x, y) untuk mengecilkan gambar. 
            # Contoh (4, 4) berarti dikecilkan 4x lipat. Ubah angkanya kalau masih kebesaran/kekecilan.
            self.logo_img = tk.PhotoImage(file="logo_biznet.png").subsample(8, 8) 
            tk.Label(frame_kiri, image=self.logo_img, bg=COLORS["BG"]).pack(anchor="w")
        except:
            # Fallback kalau file gambar gak ketemu
            tk.Label(frame_kiri, text="Biznet", font=(FONT_MAIN, 30, "bold"), fg=COLORS["BIZNET_BLUE"], bg=COLORS["BG"]).pack(anchor="w")
            
        self.lbl_time = tk.Label(frame_kiri, text="Realtime: --", font=(FONT_MAIN, 14, "italic"), fg=COLORS["TEXT_SUB"], bg=COLORS["BG"])
        self.lbl_time.pack(anchor="w", pady=(5, 0))

        # Kanan: Title & Last Speedtest
        frame_kanan = tk.Frame(frame_header, bg=COLORS["BG"])
        frame_kanan.pack(side=tk.RIGHT)
        tk.Label(frame_kanan, text="INTERNET NETWORK MONITORING", font=(FONT_MAIN, 20, "bold"), fg=COLORS["TEXT_MAIN"], bg=COLORS["BG"]).pack(anchor="e")
        self.lbl_last_speedtest = tk.Label(frame_kanan, text="Last Speedtest: --", font=(FONT_MAIN, 12, "italic"), fg=COLORS["TEXT_SUB"], bg=COLORS["BG"])
        self.lbl_last_speedtest.pack(anchor="e", pady=(5, 0))


        # --- CENTER FRAME (STATUS & PING) ---
        # Pakai expand=True biar dia bener-bener di tengah layar
        frame_center = tk.Frame(self, bg=COLORS["BG"])
        frame_center.pack(expand=True)

        self.lbl_ping = tk.Label(frame_center, text="Ping: -- ms", font=(FONT_MAIN, 20), fg=COLORS["TEXT_MAIN"], bg=COLORS["BG"])
        self.lbl_ping.pack(pady=(0, 5))

        # Frame pembungkus Lingkaran & Teks Status
        frame_status = tk.Frame(frame_center, bg=COLORS["BG"])
        frame_status.pack()

        # Lingkaran Indikator (Canvas)
        self.canvas_status = tk.Canvas(frame_status, width=40, height=40, bg=COLORS["BG"], highlightthickness=0)
        self.canvas_status.pack(side=tk.LEFT, padx=(0, 15))
        self.circle_indicator = self.canvas_status.create_oval(5, 5, 35, 35, fill="gray", outline="")

        # Teks Status Utama
        self.lbl_status = tk.Label(frame_status, text="STARTING...", font=(FONT_MAIN, 30, "bold"), fg=COLORS["TEXT_MAIN"], bg=COLORS["BG"])
        self.lbl_status.pack(side=tk.LEFT)

        # Teks Interpretasi
        self.lbl_diag = tk.Label(frame_center, text="Menyiapkan sistem...", font=(FONT_MAIN, 25), fg=COLORS["CRITICAL"], bg=COLORS["BG"])
        self.lbl_diag.pack(pady=(15, 0))

        # Teks Tindakan
        self.lbl_action = tk.Label(frame_center, text="", font=(FONT_MAIN, 20), fg=COLORS["TEXT_SUB"], bg=COLORS["BG"])
        self.lbl_action.pack(pady=(5, 0))


        # --- BOTTOM FRAME (SPEEDTEST) ---
        frame_bottom = tk.Frame(self, bg=COLORS["BG"])
        frame_bottom.pack(fill=tk.X, padx=40, pady=25)
        
        tk.Label(frame_bottom, text="Speedtest:", font=(FONT_MAIN, 16), fg=COLORS["TEXT_MAIN"], bg=COLORS["BG"]).pack(pady=(0, 15))

        frame_speed = tk.Frame(frame_bottom, bg=COLORS["BG"])
        frame_speed.pack(expand=True)

        # Kolom Kiri: Download
        frame_dl = tk.Frame(frame_speed, bg=COLORS["BG"])
        frame_dl.pack(side=tk.LEFT, padx=20)
        self.lbl_dl = tk.Label(frame_dl, text="Download: -- Mbps", font=(FONT_MAIN, 18, "bold"), fg=COLORS["TEXT_MAIN"], bg=COLORS["BG"])
        self.lbl_dl.pack()
        tk.Label(frame_dl, text=f"Committed bandwidth: {config.COMMITTED_BANDWIDTH} Mbps", font=(FONT_MAIN, 12), fg=COLORS["TEXT_SUB"], bg=COLORS["BG"]).pack()

        # Kolom Kanan: Upload
        frame_ul = tk.Frame(frame_speed, bg=COLORS["BG"])
        frame_ul.pack(side=tk.LEFT, padx=20)
        self.lbl_ul = tk.Label(frame_ul, text="Upload: -- Mbps", font=(FONT_MAIN, 18, "bold"), fg=COLORS["TEXT_MAIN"], bg=COLORS["BG"])
        self.lbl_ul.pack()
        tk.Label(frame_ul, text=f"Committed bandwidth: {config.COMMITTED_BANDWIDTH} Mbps", font=(FONT_MAIN, 12), fg=COLORS["TEXT_SUB"], bg=COLORS["BG"]).pack()


    def update_ui(self):
        try:
            # 1. Update waktu realtime
            full_time = utils.get_current_time()
            self.lbl_time.config(text=f"Realtime: {full_time}")

            # 2. Ambil data dari cache
            data = utils.load_json(config.cache_path)
            
            # Jika data kosong, jangan diproses agar tidak error
            if not data:
                self.after(1000, self.update_ui)
                return

            # 3. Ekstrak data dengan nilai default agar tidak KeyError
            status_cat = data.get("status", "UNKNOWN")    
            diagnosis = data.get("diagnosis", "Menunggu data...") 
            action_text = data.get("action", "") 
            ping = data.get("last_ping", 0)
            dl = data.get("last_dl", 0)
            ul = data.get("last_ul", 0)
            last_st = data.get("last_speedtest_at", "--")

            # 4. Update widget dasar
            self.lbl_last_speedtest.config(text=f"Last Speedtest: {last_st}")
            self.lbl_dl.config(text=f"Download: {dl} Mbps")
            self.lbl_ul.config(text=f"Upload: {ul} Mbps")
            self.lbl_ping.config(text=f"Ping: {ping} ms" if ping > 0 else "Ping: -- ms")
            self.lbl_status.config(text=status_cat)
            
            # 5. Tampilkan Interpretasi (Sekarang selalu nampil)
            self.lbl_diag.config(text=diagnosis)
            
            # 6. Logika Warna dan Tindakan
            # Default color jika tidak ada yang cocok
            color = COLORS["TEXT_SUB"] 

            if status_cat == "INTERNET NORMAL":
                color = COLORS["NORMAL"]
                self.lbl_action.config(text="")
            elif "DEGRADED" in status_cat:
                color = COLORS["WARNING"]
                self.lbl_action.config(text=f"Tindakan -> {action_text}" if action_text else "")
            else:
                # Untuk status DOWN atau UNKNOWN
                color = COLORS["CRITICAL"]
                self.lbl_action.config(text=f"Tindakan -> {action_text}" if action_text else "")

            # 7. Terapkan warna ke UI
            self.lbl_status.config(fg=color)
            self.lbl_diag.config(fg=color) 
            self.canvas_status.itemconfig(self.circle_indicator, fill=color)

        except Exception as e:
            # Ini akan memunculkan pesan error spesifik di terminal tanpa mematikan aplikasi
            print(f"[GUI ERROR] Terjadi kesalahan: {e}")

        # Jalankan ulang fungsi setelah 1 detik
        self.after(1000, self.update_ui)

if __name__ == "__main__":
    app = MonitoringApp()
    app.mainloop()
