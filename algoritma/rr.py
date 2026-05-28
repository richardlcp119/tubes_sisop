def hitung_rr(arrival_times, burst_times, quantum):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'remaining_time': burst_times[i],
            'first_start_time': -1, 
            'finish_time': 0,
            'turnaround_time': 0,
            'waiting_time': 0
        })
    
    proses_sorted = sorted(proses, key=lambda x: x['arrival_time'])
    waktu_sekarang = 0
    gantt_chart = []
    ready_queue = []
    completed = 0
    idx_proses = 0 
    total_burst_kerja = sum(burst_times) # Untuk CPU Utilization

    # Masukkan proses awal ke ready queue
    while idx_proses < n and proses_sorted[idx_proses]['arrival_time'] <= waktu_sekarang:
        ready_queue.append(proses_sorted[idx_proses])
        idx_proses += 1

    # Proses utama Round Robin    
    while completed < n:
        if not ready_queue:
            if idx_proses < n:
                # Jika ready queue kosong, lompat ke waktu kedatangan proses berikutnya
                next_arrival = proses_sorted[idx_proses]['arrival_time']
                
                if waktu_sekarang < next_arrival:
                    gantt_chart.append({
                        'id': 'Idle',
                        'start': waktu_sekarang,
                        'end': next_arrival
                    })
                
                waktu_sekarang = next_arrival
                
                # Masukkan proses yang sudah tiba setelah CPU idle
                while idx_proses < n and proses_sorted[idx_proses]['arrival_time'] <= waktu_sekarang:
                    ready_queue.append(proses_sorted[idx_proses])
                    idx_proses += 1
            continue
        
        # Ambil proses pertama dari ready queue
        p = ready_queue.pop(0)
        
        #  Logika Response Time ---
        if p['first_start_time'] == -1:
            p['first_start_time'] = waktu_sekarang
            
        start_time = waktu_sekarang
        time_to_run = min(quantum, p['remaining_time'])
        waktu_sekarang += time_to_run
        p['remaining_time'] -= time_to_run
        
        # Tambahkan ke Gantt Chart ---
        gantt_chart.append({
            'id': p['id'],
            'start': start_time,
            'end': waktu_sekarang
        })
        
        # Masukkan proses baru yang tiba selama eksekusi ke ready queue ---
        while idx_proses < n and proses_sorted[idx_proses]['arrival_time'] <= waktu_sekarang:
            ready_queue.append(proses_sorted[idx_proses])
            idx_proses += 1
            
        # Update proses setelah eksekusi ---    
        if p['remaining_time'] > 0:
            ready_queue.append(p)
        else:
            completed += 1
            p['finish_time'] = waktu_sekarang
            p['turnaround_time'] = p['finish_time'] - p['arrival_time']
            p['waiting_time'] = p['turnaround_time'] - p['burst_time']
            p['response_time'] = p['first_start_time'] - p['arrival_time']
            
    # Hitung rata-rata
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    total_rt = sum(p['response_time'] for p in proses) 
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    rata_rt = round(total_rt / n, 3) if n > 0 else 0   
    
    waktu_awal = min(p['arrival_time'] for p in proses) if n > 0 else 0
    total_waktu = waktu_sekarang - waktu_awal if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    #  CPU Utilization ---
    cpu_util = round((total_burst_kerja / total_waktu) * 100, 2) if total_waktu > 0 else 0
    cpu_util_str = f"{cpu_util}%"
    
    proses.sort(key=lambda x: int(x['id'][1:]))
    
    return proses, gantt_chart, rata_tat, rata_wt, throughput, rata_rt, cpu_util_str