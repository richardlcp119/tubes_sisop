from flask import Flask, render_template, request
import json
from algoritma.fcfs import hitung_fcfs
from algoritma.sjf_np import hitung_sjf
from algoritma.priorityscheduling_np import hitung_priority
from algoritma.rr import hitung_rr  
from algoritma.priorityscheduling_p import hitung_priority_preemptive
from algoritma.sjf_p import hitung_sjf_preemptive

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    gantt = None
    rata_tat = 0
    rata_wt = 0
    throughput = 0
    quantum = 2 
    comparison_data = {} # Menampung data untuk tabel perbandingan
    
    inputs_json = '[{"arrival": "", "burst": "", "priority": ""}]'
    selected_algo = 'fcfs'

    if request.method == 'POST':
        try:
            selected_algo = request.form.get('algorithm', 'fcfs')
            
            quantum_raw = request.form.get('quantum', '2')
            if quantum_raw.strip() != '':
                quantum = int(quantum_raw)
            
            arrival_raw = request.form.getlist('arrival[]')
            burst_raw = request.form.getlist('burst[]')
            priority_raw = request.form.getlist('priority[]')
            
            inputs_data = [
                {
                    'arrival': a, 
                    'burst': b, 
                    'priority': priority_raw[i] if i < len(priority_raw) else ""
                } 
                for i, (a, b) in enumerate(zip(arrival_raw, burst_raw))
            ]
            inputs_json = json.dumps(inputs_data)

            arrival_times = [int(x) for x in arrival_raw if x.strip() != '']
            burst_times = [int(x) for x in burst_raw if x.strip() != '']
            priority_times = [int(x) for x in priority_raw if x.strip() != '']

            if len(arrival_times) == len(burst_times) and len(arrival_times) > 0:
                # 1. Hitung Algoritma Utama (Untuk Gantt Chart & Detail)
                if selected_algo == 'fcfs':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_fcfs(arrival_times.copy(), burst_times.copy())
                elif selected_algo == 'sjf':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_sjf(arrival_times.copy(), burst_times.copy())
                elif selected_algo == 'sjf_p':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_sjf_preemptive(arrival_times.copy(), burst_times.copy())
                elif selected_algo == 'priority_np':
                    if len(priority_times) == len(arrival_times):
                        hasil, gantt, rata_tat, rata_wt, throughput = hitung_priority(arrival_times.copy(), burst_times.copy(), priority_times.copy())
                    else:
                        hasil = "error_priority_len"
                elif selected_algo == 'priority_p':
                    if len(priority_times) == len(arrival_times):
                        hasil, gantt, rata_tat, rata_wt, throughput = hitung_priority_preemptive(arrival_times.copy(), burst_times.copy(), priority_times.copy())
                    else:
                        hasil = "error_priority_len"
                elif selected_algo == 'rr':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_rr(arrival_times.copy(), burst_times.copy(), quantum)

                # 2. Hitung Semua Algoritma untuk Tabel Perbandingan
                if hasil not in ["error_len", "error_priority_len", "error_val"]:
                    _, _, c_tat, c_wt, _ = hitung_fcfs(arrival_times.copy(), burst_times.copy())
                    comparison_data['FCFS'] = {'tat': c_tat, 'wt': c_wt}
                    
                    _, _, c_tat, c_wt, _ = hitung_sjf(arrival_times.copy(), burst_times.copy())
                    comparison_data['SJF (Non-Preemptive)'] = {'tat': c_tat, 'wt': c_wt}
                    
                    _, _, c_tat, c_wt, _ = hitung_sjf_preemptive(arrival_times.copy(), burst_times.copy())
                    comparison_data['SJF (Preemptive)'] = {'tat': c_tat, 'wt': c_wt}
                    
                    _, _, c_tat, c_wt, _ = hitung_rr(arrival_times.copy(), burst_times.copy(), quantum)
                    comparison_data[f'Round Robin (Q={quantum})'] = {'tat': c_tat, 'wt': c_wt}
                    
                    if len(priority_times) == len(arrival_times):
                        _, _, c_tat, c_wt, _ = hitung_priority(arrival_times.copy(), burst_times.copy(), priority_times.copy())
                        comparison_data['Priority (Non-Preemptive)'] = {'tat': c_tat, 'wt': c_wt}
                        
                        _, _, c_tat, c_wt, _ = hitung_priority_preemptive(arrival_times.copy(), burst_times.copy(), priority_times.copy())
                        comparison_data['Priority (Preemptive)'] = {'tat': c_tat, 'wt': c_wt}

            else:
                hasil = "error_len"
        except ValueError:
            hasil = "error_val"

    return render_template('index.html', hasil=hasil, gantt=gantt, 
                           rata_tat=rata_tat, rata_wt=rata_wt, 
                           throughput=throughput, inputs_json=inputs_json,
                           selected_algo=selected_algo, quantum=quantum,
                           comparison_data=comparison_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)