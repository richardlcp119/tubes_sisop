def hitung_fcfs(arrival_times, burst_times):
    n = len(arrival_times)
    proses = []
    
    # Satukan input menjadi list of dictionary agar mudah dikelola
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',  # Mengubah indeks 0, 1, 2 menjadi A, B, C...
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i]
        })
    
    # Prinsip FCFS: Urutkan berdasarkan waktu kedatangan terkecil
    proses.sort(key=lambda x: x['arrival_time'])
    
    waktu_sekarang = 0
    gantt_chart = []
    
    for p in proses:
        # Jika CPU sempat menganggur sebelum proses ini datang
        if waktu_sekarang < p['arrival_time']:
            waktu_sekarang = p['arrival_time']
        
        start_time = waktu_sekarang
        p['finish_time'] = start_time + p['burst_time']
        p['turnaround_time'] = p['finish_time'] - p['arrival_time']
        p['waiting_time'] = p['turnaround_time'] - p['burst_time']
        
        # Simpan data urutan blok untuk visualisasi Gantt Chart
        gantt_chart.append({
            'id': p['id'],
            'start': start_time,
            'end': p['finish_time']
        })
        
        waktu_sekarang = p['finish_time']
    
    # Hitung nilai rata-rata (Average)
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    
    # Throughput = Jumlah proses / Total rentang waktu eksekusi
    total_waktu = waktu_sekarang - proses[0]['arrival_time'] if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    return proses, gantt_chart, rata_tat, rata_wt, throughput