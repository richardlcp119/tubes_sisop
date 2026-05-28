def hitung_priority(arrival_times, burst_times, priorities):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'priority': priorities[i],
            'is_completed': False
        })
    
    waktu_sekarang = 0
    selesai = 0
    gantt_chart = []
    total_burst_kerja = sum(burst_times) # untuk CPU Utilization
    
    while selesai < n:
        # Ambil proses yang sudah tiba dan belum selesai
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']]
        
        if eligible:
            # Urutkan berdasarkan Prioritas Tertinggi (Angka Terkecil), lalu Arrival Time
            eligible.sort(key=lambda x: (x['priority'], x['arrival_time']))
            p = eligible[0]
            
            start_time = waktu_sekarang
            p['finish_time'] = start_time + p['burst_time']
            p['turnaround_time'] = p['finish_time'] - p['arrival_time']
            p['waiting_time'] = p['turnaround_time'] - p['burst_time']
            
            #  Response Time untuk Non-Preemptive = Waiting Time
            p['response_time'] = p['waiting_time']
            
            p['is_completed'] = True
            
            gantt_chart.append({
                'id': p['id'],
                'start': start_time,
                'end': p['finish_time']
            })
            
            waktu_sekarang = p['finish_time']
            selesai += 1
        else:
            pending = [p for p in proses if not p['is_completed']]
            next_arrival = min(p['arrival_time'] for p in pending)
            
            #  Catat Idle ke Gantt Chart
            gantt_chart.append({
                'id': 'Idle',
                'start': waktu_sekarang,
                'end': next_arrival
            })
            waktu_sekarang = next_arrival

    # Kalkulasi rata-rata
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    total_rt = sum(p['response_time'] for p in proses) 
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    rata_rt = round(total_rt / n, 3) if n > 0 else 0   
    
    total_waktu = waktu_sekarang - min(p['arrival_time'] for p in proses) if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    #  CPU Utilization
    cpu_util = round((total_burst_kerja / total_waktu) * 100, 2) if total_waktu > 0 else 0
    cpu_util_str = f"{cpu_util}%"
    
    proses.sort(key=lambda x: x['id'])
    
    # Mengembalikan 7 nilai yang konsisten
    return proses, gantt_chart, rata_tat, rata_wt, throughput, rata_rt, cpu_util_str