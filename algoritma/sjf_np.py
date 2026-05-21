def hitung_sjf(arrival_times, burst_times):
    n = len(arrival_times)
    proses = []
    
    # Satukan input menjadi list of dictionary
    for i in range(n):
        proses.append({
            'id': chr(65 + i),  # ID A, B, C...
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'is_completed': False
        })
    
    waktu_sekarang = 0
    selesai = 0
    gantt_chart = []
    
    while selesai < n:
        # Filter proses yang sudah tiba dan belum selesai
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']]
        
        if eligible:
            # Prinsip SJF: Urutkan berdasarkan burst_time terkecil. 
            # Jika sama, prioritaskan arrival_time terkecil.
            eligible.sort(key=lambda x: (x['burst_time'], x['arrival_time']))
            p = eligible[0] # Ambil proses terpendek
            
            start_time = waktu_sekarang
            p['finish_time'] = start_time + p['burst_time']
            p['turnaround_time'] = p['finish_time'] - p['arrival_time']
            p['waiting_time'] = p['turnaround_time'] - p['burst_time']
            p['is_completed'] = True
            
            # Simpan blok untuk visualisasi Gantt Chart
            gantt_chart.append({
                'id': p['id'],
                'start': start_time,
                'end': p['finish_time']
            })
            
            waktu_sekarang = p['finish_time']
            selesai += 1
        else:
            # Jika CPU menganggur, lompat ke waktu kedatangan proses berikutnya
            pending = [p for p in proses if not p['is_completed']]
            waktu_sekarang = min(p['arrival_time'] for p in pending)

    # Hitung nilai rata-rata (Average)
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    
    # Throughput = Jumlah proses / Total rentang waktu eksekusi
    min_arrival = min(p['arrival_time'] for p in proses) if n > 0 else 0
    total_waktu = waktu_sekarang - min_arrival if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    # Kembalikan urutan proses berdasarkan ID (A, B, C) untuk tabel HTML
    proses.sort(key=lambda x: x['id'])
    
    return proses, gantt_chart, rata_tat, rata_wt, throughput