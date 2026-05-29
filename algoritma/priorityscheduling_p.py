# Fungsi untuk menerima data proses, lalu hitung jawal priority scheduling
def hitung_priority_preemptive(arrival_times, burst_times, priorities):
    n = len(arrival_times) # Menyimpan jumlah proses
    proses = [] # Membuat list kosong untuk menyimpan data proses
    
    for i in range(n): # Loop untuk membuat data proses i = index, range (n) = 0 sampai n-1
        proses.append({ # Menambahkan ke belakang list
            'id': f'P{i+1}', # Memberi nama proses seperti P1, P2, dst
            'arrival_time': arrival_times[i], # Mengambil waktu kedatangan proses ke-i
            'burst_time': burst_times[i], # Mengambil lama waktu proses ke-i membutuhkan CPU
            'remaining_time': burst_times[i], # Menyimpan sisa waktu proses yang belum selesai, awalnya sama dengan burst_time
            'priority': priorities[i], # Mengambil prioritas proses ke-i
            'first_start_time': -1, # Menyimpan waktu pertama kali proses mulai berjalan
            'is_completed': False, # Menyimpan status apakah proses sudah selesai atau belum
            'finish_time': 0, # Menyimpan waktu selesai proses
            'turnaround_time': 0, # Menyimpan waktu turnaround proses
            'waiting_time': 0, # Menyimpan waktu tunggu proses
            'response_time': 0  # Menyimpan waktu respon proses     
        })

# Inisialisasi variabel untuk simulasi  
    waktu_sekarang = 0 # Waktu saat ini, mulai dari 0
    selesai = 0 # Jumlah proses yang sudah selesai
    gantt_chart = [] # List kosong untuk menyimpan data Gantt Chart
    proses_sebelumnya = None # Belum ada proses yang sedang berjalan, jadi None
    start_time_gantt = 0 # Menyimpan waktu mulai untuk Gantt Chart
    total_burst_kerja = sum(burst_times) # Menjumlahkan semua burst time

# Loop utama sampai semua proses selesai   
    while selesai < n: # Selama proses yang selesai masih kurang, terus berjalan
        # Cari proses yang bisa dijalankan
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']] # Buat daftar proses yang sudah datang dan belum selesai
        
        if eligible: # Kalau ada proses yang siap dijalankan
            # Mengurutkan berdasarkan prioritas
            eligible.sort(key=lambda x: (x['priority'], x['arrival_time'])) #  Urutkan berdasarkan prioritas terkecil, kalau sama cek yang datang lebih awal
            p_terpilih = eligible[0] # Ambil proses pertama dari yang sudah diurutkan
            
            # Logika Response Time
            if p_terpilih['first_start_time'] == -1: # Proses belum dijalankan
                p_terpilih['first_start_time'] = waktu_sekarang # Simpan waktu pertama proses mulai berjalan
            
            # Jika CPU beralih dari satu proses ke proses lain, atau dari 'Idle' ke proses
            if proses_sebelumnya != p_terpilih['id']: # Jika proses yang terpilih berbeda dengan proses sebelumnya yang berjalan
                if proses_sebelumnya is not None: # Jika sebelumnya ada proses yang berjalan (bukan pertama kali)
                    gantt_chart.append({'id': proses_sebelumnya, 'start': start_time_gantt, 'end': waktu_sekarang}) # Simpan proses ke sebelumnya ke gantt chart
                start_time_gantt = waktu_sekarang # Mulai blok gantt baru dari waktu sekarang
                proses_sebelumnya = p_terpilih['id'] # Proses sekarang menjadi proses yang sedang berjalan
            
            p_terpilih['remaining_time'] -= 1 # Kurangi sisa waktu proses yang sedang berjalan karena sudah menggunakan CPU selama 1 unit waktu
            waktu_sekarang += 1 # Tambah waktu sekarang karena sudah berjalan selama 1 unit waktu
            
            # Kalau proses sudah selesai
            if p_terpilih['remaining_time'] == 0: # Jika sisa waktu proses sudah mencapai 0
                p_terpilih['finish_time'] = waktu_sekarang # Simpan waktu selesai proses
                # Hitung turnaround time, waiting time, dan response time
                p_terpilih['turnaround_time'] = p_terpilih['finish_time'] - p_terpilih['arrival_time']
                p_terpilih['waiting_time'] = p_terpilih['turnaround_time'] - p_terpilih['burst_time']
                p_terpilih['response_time'] = p_terpilih['first_start_time'] - p_terpilih['arrival_time']
                p_terpilih['is_completed'] = True # Tandai proses sudah selesai
                selesai += 1 # Tambah jumlah proses yang sudah selesai
        
        # Jika tidak ada proses yang siap (CPU menganggur)
        else:
            if proses_sebelumnya != 'Idle': # Jika sebelumnya tidak dalam keadaan idle
                if proses_sebelumnya is not None: # Jika sebelumnya ada proses yang berjalan, simpan ke gantt chart sebelum beralih ke idle
                    # Simpan proses terakhir yang berjalan sebelum CPU idle
                    gantt_chart.append({'id': proses_sebelumnya, 'start': start_time_gantt, 'end': waktu_sekarang}) # Simpan proses terakhir sebelum CPU idle
                start_time_gantt = waktu_sekarang # Mulai blok gantt baru untuk idle dari waktu sekarang
                proses_sebelumnya = 'Idle' # Ubah state menjadi Idle
            
            waktu_sekarang += 1 # Tambah waktu sekarang karena CPU idle selama 1 unit waktu

    # Menutup Gantt Chart
    # Mencatat bagian terakhir dari proses atau idle yang sedang berjalan
    if proses_sebelumnya is not None:
        gantt_chart.append({'id': proses_sebelumnya, 'start': start_time_gantt, 'end': waktu_sekarang})

    # Menghitung total metrik
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    total_rt = sum(p['response_time'] for p in proses) 
    
    # menghitung rata-rata metrik
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    rata_rt = round(total_rt / n, 3) if n > 0 else 0   
    
    total_waktu = waktu_sekarang - min(p['arrival_time'] for p in proses) if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    # CPU Utilization
    cpu_util = round((total_burst_kerja / total_waktu) * 100, 2) if total_waktu > 0 else 0
    cpu_util_str = f"{cpu_util}%"
    
    proses.sort(key=lambda x: x['id'])
    
    return proses, gantt_chart, rata_tat, rata_wt, throughput, rata_rt, cpu_util_str