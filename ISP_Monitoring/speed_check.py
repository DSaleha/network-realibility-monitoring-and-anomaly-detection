import speedtest

def run_speed_test():
    try:
        st = speedtest.Speedtest()
        print("--- Speedtest: Mencari Server ---")
        st.get_best_server()

        #setelah tau ID server
        #st = speedtest.Speedtest()
        #print("--- Speedtest: Sedang Ping ---")
        #st.get_servers([Servre_id]) #contoh [12345]
        #st.get_best_server()

        print("---Speedtest: Sedang Download ---")
        st.download()

        print("---Speedtest: Sedang Upload ---")
        st.upload()

        #didapat setelah proses get best server
        res = st.results.dict()

        #konversi 1 Mbps = 1.000.000 bits
        #rerason: protokol ISP 
        data_final = {
            "download_mbps": round(res['download'] / 1_000_000, 2),
            "upload_mbps": round(res['upload'] / 1_000_000,2),
            "ping_ms": round(res['ping'], 2),
            "server": res['server']['sponsor'], #mengambil nama server sponsor dari hasil
            "status": "SUCCESS"
        }

        print(f"Hasil: DL: {data_final['download_mbps']} | UL: {data_final['upload_mbps']}")
        return data_final

    except Exception as e:
        print(f"Gagal Speedtest{e}")
        return None

if __name__ == "__main__":
    hasil = run_speed_test()
    print("Output Data:", hasil)