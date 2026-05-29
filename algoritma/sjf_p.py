def hitung_sjf_preemptive(arrival_times, burst_times):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'remaining_time': burst_times[i],
            'first_start_time': -1, 
            'is_completed': False
        })
    
    waktu_sekarang = 0
    selesai = 0
    gantt_chart = []
    current_id = None
    start_time = 0
    
    while selesai < n:
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']]
        
        if eligible:
            eligible.sort(key=lambda x: (x['remaining_time'], x['arrival_time']))
            p = eligible[0]
            
            # --- Logika Response Time ---
            if p['first_start_time'] == -1:
                p['first_start_time'] = waktu_sekarang
            
            if current_id != p['id']:
                if current_id is not None:
                    gantt_chart.append({'id': current_id, 'start': start_time, 'end': waktu_sekarang})
                current_id = p['id']
                start_time = waktu_sekarang
            
            p['remaining_time'] -= 1
            waktu_sekarang += 1
            
            if p['remaining_time'] == 0:
                p['finish_time'] = waktu_sekarang
                p['turnaround_time'] = p['finish_time'] - p['arrival_time']
                p['waiting_time'] = p['turnaround_time'] - p['burst_time']
                p['response_time'] = p['first_start_time'] - p['arrival_time']
                p['is_completed'] = True
                selesai += 1
        else:
            if current_id is not None:
                gantt_chart.append({
                    'id': current_id,
                    'start': start_time,
                    'end': waktu_sekarang
                })
                current_id = None


            pending = [p for p in proses if not p['is_completed']]
            next_arrival = min(p['arrival_time'] for p in pending)

    
            gantt_chart.append({
                'id': 'idle',
                'start': waktu_sekarang,
                'end': next_arrival
            })

            waktu_sekarang = next_arrival

    if current_id is not None:
        gantt_chart.append({'id': current_id, 'start': start_time, 'end': waktu_sekarang})

    # Hitung rata-rata
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    total_rt = sum(p['response_time'] for p in proses) 
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    rata_rt = round(total_rt / n, 3) if n > 0 else 0  
    
    total_waktu = waktu_sekarang - min(p['arrival_time'] for p in proses) if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    #  CPU Utilization ---
    total_burst = sum(p['burst_time'] for p in proses)
    cpu_util = round((total_burst / total_waktu) * 100, 2) if total_waktu > 0 else 0
    cpu_util_str = f"{cpu_util}%"
    
    proses.sort(key=lambda x: x['id'])
    return proses, gantt_chart, rata_tat, rata_wt, throughput, rata_rt, cpu_util_str