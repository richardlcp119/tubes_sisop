def hitung_priority_preemptive(arrival_times, burst_times, priorities):
    n = len(arrival_times)
    proses = []
    
    for i in range(n):
        proses.append({
            'id': f'P{i+1}',
            'arrival_time': arrival_times[i],
            'burst_time': burst_times[i],
            'remaining_time': burst_times[i], # Tambahan: Menyimpan sisa waktu eksekusi
            'priority': priorities[i],
            'is_completed': False,
            'finish_time': 0,
            'turnaround_time': 0,
            'waiting_time': 0
        })
    
    waktu_sekarang = 0
    selesai = 0
    gantt_chart = []
    
    # Variabel tambahan untuk melacak history proses pada Gantt Chart
    proses_sebelumnya = None
    start_time_gantt = 0
    
    while selesai < n:
        # Ambil proses yang sudah tiba dan belum selesai
        eligible = [p for p in proses if p['arrival_time'] <= waktu_sekarang and not p['is_completed']]
        
        if eligible:
            # Urutkan berdasarkan Prioritas Tertinggi (Angka Terkecil), lalu Arrival Time
            eligible.sort(key=lambda x: (x['priority'], x['arrival_time']))
            p_terpilih = eligible[0]
            
            # Jika proses yang dieksekusi berubah (Context Switch), simpan ke Gantt Chart
            if proses_sebelumnya != p_terpilih['id']:
                if proses_sebelumnya is not None:
                    gantt_chart.append({
                        'id': proses_sebelumnya,
                        'start': start_time_gantt,
                        'end': waktu_sekarang
                    })
                start_time_gantt = waktu_sekarang
                proses_sebelumnya = p_terpilih['id']
            
            # Eksekusi proses terpilih selama 1 satuan waktu (Preemptive)
            p_terpilih['remaining_time'] -= 1
            waktu_sekarang += 1
            
            # Jika proses sudah selesai
            if p_terpilih['remaining_time'] == 0:
                p_terpilih['is_completed'] = True
                selesai += 1
                
                # Kalkulasi waktu untuk proses yang selesai
                p_terpilih['finish_time'] = waktu_sekarang
                p_terpilih['turnaround_time'] = p_terpilih['finish_time'] - p_terpilih['arrival_time']
                p_terpilih['waiting_time'] = p_terpilih['turnaround_time'] - p_terpilih['burst_time']
        else:
            # Jika tidak ada proses yang siap (CPU Idle)
            if proses_sebelumnya is not None:
                gantt_chart.append({
                    'id': proses_sebelumnya,
                    'start': start_time_gantt,
                    'end': waktu_sekarang
                })
                proses_sebelumnya = None
            
            waktu_sekarang += 1

    # Masukkan proses terakhir ke dalam Gantt Chart setelah loop selesai
    if proses_sebelumnya is not None:
        gantt_chart.append({
            'id': proses_sebelumnya,
            'start': start_time_gantt,
            'end': waktu_sekarang
        })

    # Kalkulasi rata-rata (Sama seperti Non-Preemptive)
    total_tat = sum(p['turnaround_time'] for p in proses)
    total_wt = sum(p['waiting_time'] for p in proses)
    
    rata_tat = round(total_tat / n, 3) if n > 0 else 0
    rata_wt = round(total_wt / n, 3) if n > 0 else 0
    
    total_waktu = waktu_sekarang - min(p['arrival_time'] for p in proses) if n > 0 else 1
    throughput = round(n / total_waktu, 3) if total_waktu > 0 else 0
    
    proses.sort(key=lambda x: x['id'])
    return proses, gantt_chart, rata_tat, rata_wt, throughput