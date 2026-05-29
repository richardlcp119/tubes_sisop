def hitung_fcfs(arrival_times, burst_times):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i]
        })
    
    # Prinsip FCFS: Urutkan dari waktu kedatangan terkecil
    proses.sort(key=lambda x: x['arrival_time'])
    
    waktu_sekarang = 0
    gantt_chart = []
    
    # Variabel untuk Util ---
    total_waktu_kerja = 0
    
    for p in proses:
        # Jika CPU menganggur sebelum proses datang
        if waktu_sekarang < p['arrival_time']:
            gantt_chart.append({
                'id': 'Idle',
                'start': waktu_sekarang,
                'end': p['arrival_time']
            })
            waktu_sekarang = p['arrival_time']
        
        start_time = waktu_sekarang
        p['finish_time'] = start_time + p['burst_time']
        p['turnaround_time'] = p['finish_time'] - p['arrival_time']
        p['waiting_time'] = p['turnaround_time'] - p['burst_time']
        
        # FCFS: Response Time selalu sama dengan Waiting Time
        p['response_time'] = p['waiting_time'] 
        
        gantt_chart.append({
            'id': p['id'],
            'start': start_time,
            'end': p['finish_time']
        })
        
        total_waktu_kerja += p['burst_time']
        waktu_sekarang = p['finish_time']
    
    # Hitung nilai rata-rata
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    total_rt = sum(p['response_time'] for p in proses) 
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    rata_rt = round(total_rt / n, 3) if n > 0 else 0  
    
    # Throughput & CPU Utilization
    total_waktu = waktu_sekarang - proses[0]['arrival_time'] if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    # CPU Util = (Total burst / Total waktu) * 100
    cpu_util = round((total_waktu_kerja / total_waktu) * 100, 2) if total_waktu > 0 else 0
    cpu_util_str = f"{cpu_util}%"
    
    # Kembalikan urut sesuai ID asal (bukan urutan eksekusi)
    proses.sort(key=lambda x: x['id'])
    
    return proses, gantt_chart, rata_tat, rata_wt, throughput, rata_rt, cpu_util_str