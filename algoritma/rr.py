def hitung_rr(arrival_times, burst_times, quantum):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'remaining_time': burst_times[i],
            'finish_time': 0,
            'turnaround_time': 0,
            'waiting_time': 0
        })
    
    # Urutkan berdasarkan waktu kedatangan awal
    proses_sorted = sorted(proses, key=lambda x: x['arrival_time'])
    
    waktu_sekarang = 0
    gantt_chart = []
    ready_queue = []
    completed = 0
    idx_proses = 0 
    
    # Masukkan proses yang datang pada waktu 0 ke dalam antrean
    while idx_proses < n and proses_sorted[idx_proses]['arrival_time'] <= waktu_sekarang:
        ready_queue.append(proses_sorted[idx_proses])
        idx_proses += 1
        
    while completed < n:
        if not ready_queue:
            # Jika CPU menganggur, majukan waktu ke waktu kedatangan proses berikutnya
            if idx_proses < n:
                waktu_sekarang = proses_sorted[idx_proses]['arrival_time']
                while idx_proses < n and proses_sorted[idx_proses]['arrival_time'] <= waktu_sekarang:
                    ready_queue.append(proses_sorted[idx_proses])
                    idx_proses += 1
            continue
        
        p = ready_queue.pop(0)
        start_time = waktu_sekarang
        
        # Eksekusi proses selama quantum atau sisa waktunya
        time_to_run = min(quantum, p['remaining_time'])
        waktu_sekarang += time_to_run
        p['remaining_time'] -= time_to_run
        
        # Simpan state untuk Gantt Chart
        gantt_chart.append({
            'id': p['id'],
            'start': start_time,
            'end': waktu_sekarang
        })
        
        # Periksa proses baru yang datang selama proses ini dieksekusi
        while idx_proses < n and proses_sorted[idx_proses]['arrival_time'] <= waktu_sekarang:
            ready_queue.append(proses_sorted[idx_proses])
            idx_proses += 1
            
        # Jika proses belum selesai, masukkan kembali ke antrean
        if p['remaining_time'] > 0:
            ready_queue.append(p)
        else:
            completed += 1
            p['finish_time'] = waktu_sekarang
            p['turnaround_time'] = p['finish_time'] - p['arrival_time']
            p['waiting_time'] = p['turnaround_time'] - p['burst_time']
            
    # Hitung nilai rata-rata (Average)
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    
    # Throughput
    waktu_awal = min(p['arrival_time'] for p in proses) if n > 0 else 0
    total_waktu = waktu_sekarang - waktu_awal if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    # Kembalikan ke urutan ID asli untuk tampilan tabel
    proses.sort(key=lambda x: int(x['id'][1:]))
    
    return proses, gantt_chart, rata_tat, rata_wt, throughput