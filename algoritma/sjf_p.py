def hitung_sjf_preemptive(arrival_times, burst_times):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'remaining_time': burst_times[i],  # Tambahan: melacak sisa waktu eksekusi
            'is_completed': False
        })
    
    waktu_sekarang = 0
    selesai = 0
    gantt_chart = []
    
    # Tambahan: Variabel untuk merekam kapan sebuah proses mulai dieksekusi secara beruntun
    current_id = None
    start_time = 0
    
    while selesai < n:
        # Ambil proses yang sudah tiba dan belum selesai
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']]
        
        if eligible:
            # Urutkan berdasarkan REMAINING TIME terpendek, lalu Arrival Time terkecil
            eligible.sort(key=lambda x: (x['remaining_time'], x['arrival_time']))
            p = eligible[0]
            
            # Jika CPU beralih mengeksekusi proses lain, catat proses sebelumnya ke Gantt Chart
            if current_id != p['id']:
                if current_id is not None:
                    gantt_chart.append({
                        'id': current_id,
                        'start': start_time,
                        'end': waktu_sekarang
                    })
                current_id = p['id']
                start_time = waktu_sekarang
            
            # Eksekusi proses selama 1 satuan waktu (Preemption check)
            p['remaining_time'] -= 1
            waktu_sekarang += 1
            
            # Jika proses selesai
            if p['remaining_time'] == 0:
                p['finish_time'] = waktu_sekarang
                p['turnaround_time'] = p['finish_time'] - p['arrival_time']
                p['waiting_time'] = p['turnaround_time'] - p['burst_time']
                p['is_completed'] = True
                selesai += 1
        else:
            # Jika CPU idle
            if current_id is not None:
                gantt_chart.append({
                    'id': current_id,
                    'start': start_time,
                    'end': waktu_sekarang
                })
                current_id = None
            
            # Lompat ke waktu kedatangan proses terdekat
            pending = [p for p in proses if not p['is_completed']]
            next_arrival = min(p['arrival_time'] for p in pending)
            waktu_sekarang = next_arrival

    # Memasukkan blok proses terakhir ke dalam Gantt Chart setelah loop selesai
    if current_id is not None:
        gantt_chart.append({
            'id': current_id,
            'start': start_time,
            'end': waktu_sekarang
        })

    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    
    total_waktu = waktu_sekarang - min(p['arrival_time'] for p in proses) if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    proses.sort(key=lambda x: x['id'])
    return proses, gantt_chart, rata_tat, rata_wt, throughput

# --- Contoh Cara Memanggilnya ---
# arrival_times = [0, 1, 2, 3]
# burst_times = [8, 4, 9, 5]
# hasil_proses, chart, rata_tat, rata_wt, throughput = hitung_sjf_preemptive(arrival_times, burst_times)