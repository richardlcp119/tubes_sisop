def hitung_priority_preemptive(arrival_times, burst_times, priorities):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'remaining_time': burst_times[i],
            'priority': priorities[i],
            'first_start_time': -1, 
            'is_completed': False,
            'finish_time': 0,
            'turnaround_time': 0,
            'waiting_time': 0,
            'response_time': 0      
        })
    
    waktu_sekarang = 0
    selesai = 0
    gantt_chart = []
    proses_sebelumnya = None
    start_time_gantt = 0
    total_burst_kerja = sum(burst_times) 
    
    while selesai < n:
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']]
        
        if eligible:
            eligible.sort(key=lambda x: (x['priority'], x['arrival_time']))
            p_terpilih = eligible[0]
            
            # Logika Response Time
            if p_terpilih['first_start_time'] == -1:
                p_terpilih['first_start_time'] = waktu_sekarang
            
            # Jika CPU beralih dari satu proses ke proses lain, atau dari 'Idle' ke proses
            if proses_sebelumnya != p_terpilih['id']:
                if proses_sebelumnya is not None:
                    gantt_chart.append({'id': proses_sebelumnya, 'start': start_time_gantt, 'end': waktu_sekarang})
                start_time_gantt = waktu_sekarang
                proses_sebelumnya = p_terpilih['id']
            
            p_terpilih['remaining_time'] -= 1
            waktu_sekarang += 1
            
            if p_terpilih['remaining_time'] == 0:
                p_terpilih['finish_time'] = waktu_sekarang
                p_terpilih['turnaround_time'] = p_terpilih['finish_time'] - p_terpilih['arrival_time']
                p_terpilih['waiting_time'] = p_terpilih['turnaround_time'] - p_terpilih['burst_time']
                p_terpilih['response_time'] = p_terpilih['first_start_time'] - p_terpilih['arrival_time']
                p_terpilih['is_completed'] = True
                selesai += 1
        else:
            # REVISI: Jika tidak ada proses yang siap (CPU menganggur)
            if proses_sebelumnya != 'Idle':
                if proses_sebelumnya is not None:
                    # Simpan proses terakhir yang berjalan sebelum CPU idle
                    gantt_chart.append({'id': proses_sebelumnya, 'start': start_time_gantt, 'end': waktu_sekarang})
                start_time_gantt = waktu_sekarang
                proses_sebelumnya = 'Idle' # Ubah state menjadi Idle
            
            waktu_sekarang += 1

    # Memasukkan proses terakhir atau idle terakhir ke dalam Gantt Chart setelah loop selesai
    if proses_sebelumnya is not None:
        gantt_chart.append({'id': proses_sebelumnya, 'start': start_time_gantt, 'end': waktu_sekarang})

    # Kalkulasi rata-rata
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    total_rt = sum(p['response_time'] for p in proses) 
    
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