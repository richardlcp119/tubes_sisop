def hitung_sjf(arrival_times, burst_times):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'is_completed': False
        })
    
    waktu_sekarang = 0
    selesai = 0
    gantt_chart = []
    total_burst_kerja = 0 # Untuk hitung CPU Utilization
    
    while selesai < n:
        # Ambil proses yang sudah tiba dan belum selesai
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']]
        
        if eligible:
            # Urutkan berdasarkan Burst Time terpendek, lalu Arrival Time terkecil
            eligible.sort(key=lambda x: (x['burst_time'], x['arrival_time']))
            p = eligible[0]
            
            start_time = waktu_sekarang
            p['finish_time'] = start_time + p['burst_time']
            p['turnaround_time'] = p['finish_time'] - p['arrival_time']
            p['waiting_time'] = p['turnaround_time'] - p['burst_time']
            
            # Response Time untuk Non-Preemptive = Waiting Time
            p['response_time'] = p['waiting_time']
            
            p['is_completed'] = True
            total_burst_kerja += p['burst_time']
            
            gantt_chart.append({
                'id': p['id'],
                'start': start_time,
                'end': p['finish_time']
            })
            
            waktu_sekarang = p['finish_time']
            selesai += 1
        else:
            # Jika CPU idle
            pending = [p for p in proses if not p['is_completed']]
            waktu_sekarang = min(p['arrival_time'] for p in pending)

    # Hitung nilai rata-rata
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    total_rt = sum(p['response_time'] for p in proses) 
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    rata_rt = round(total_rt / n, 3) if n > 0 else 0 
    
    # Hitung Throughput & CPU Utilization
    total_rentang_waktu = waktu_sekarang - min(p['arrival_time'] for p in proses) if n > 0 else 1
    throughput = round(n / total_rentang_waktu, 3) if total_rentang_waktu > 0 else 0
    
    # CPU Utilization = (Total burst waktu kerja / Total rentang waktu) * 100
    cpu_util = round((total_burst_kerja / total_rentang_waktu) * 100, 2) if total_rentang_waktu > 0 else 0
    cpu_util_str = f"{cpu_util}%"
    
    proses.sort(key=lambda x: x['id'])
    
    # Kembalikan 7 variabel
    return proses, gantt_chart, rata_tat, rata_wt, throughput, rata_rt, cpu_util_str