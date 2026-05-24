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
    hasil = None; gantt = None; rata_tat = 0; rata_wt = 0; rata_rt = 0; throughput = 0; cpu_util = "0%"
    quantum = 2 
    comparison_data = {} 
    inputs_json = '[{"arrival": "", "burst": "", "priority": "1"}]'
    selected_algo = 'fcfs'

    if request.method == 'POST':
        try:
            selected_algo = request.form.get('algorithm', 'fcfs')
            quantum = int(request.form.get('quantum', 2))
            
            arrival_raw = request.form.getlist('arrival[]')
            burst_raw = request.form.getlist('burst[]')
            priority_raw = request.form.getlist('priority[]')
            
            inputs_data = [{'arrival': a, 'burst': b, 'priority': priority_raw[i] if i < len(priority_raw) else "1"} 
                           for i, (a, b) in enumerate(zip(arrival_raw, burst_raw))]
            inputs_json = json.dumps(inputs_data)

            arrival_times = [int(x) for x in arrival_raw if x.strip() != '']
            burst_times = [int(x) for x in burst_raw if x.strip() != '']
            priority_times = [int(x) for x in priority_raw if x.strip() != '']

            if len(arrival_times) == len(burst_times) and len(arrival_times) > 0:
                # 1. Hitung Algoritma Utama
                if selected_algo == 'fcfs':
                    hasil, gantt, rata_tat, rata_wt, throughput, rata_rt, cpu_util = hitung_fcfs(arrival_times, burst_times)
                elif selected_algo == 'sjf':
                    hasil, gantt, rata_tat, rata_wt, throughput, rata_rt, cpu_util = hitung_sjf(arrival_times, burst_times)
                elif selected_algo == 'sjf_p':
                    hasil, gantt, rata_tat, rata_wt, throughput, rata_rt, cpu_util = hitung_sjf_preemptive(arrival_times, burst_times)
                elif selected_algo == 'priority_np' and len(priority_times) == len(arrival_times):
                    hasil, gantt, rata_tat, rata_wt, throughput, rata_rt, cpu_util = hitung_priority(arrival_times, burst_times, priority_times)
                elif selected_algo == 'priority_p' and len(priority_times) == len(arrival_times):
                    hasil, gantt, rata_tat, rata_wt, throughput, rata_rt, cpu_util = hitung_priority_preemptive(arrival_times, burst_times, priority_times)
                elif selected_algo == 'rr':
                    hasil, gantt, rata_tat, rata_wt, throughput, rata_rt, cpu_util = hitung_rr(arrival_times, burst_times, quantum)

                # 2. Tabel Perbandingan (Gunakan tuple unpacking untuk mengambil data yang diperlukan saja)
                comparison_data['FCFS'] = {'tat': hitung_fcfs(arrival_times, burst_times)[2], 'wt': hitung_fcfs(arrival_times, burst_times)[3]}
                comparison_data['SJF (Non-Preemptive)'] = {'tat': hitung_sjf(arrival_times, burst_times)[2], 'wt': hitung_sjf(arrival_times, burst_times)[3]}
                comparison_data['SJF (Preemptive)'] = {'tat': hitung_sjf_preemptive(arrival_times, burst_times)[2], 'wt': hitung_sjf_preemptive(arrival_times, burst_times)[3]}
                comparison_data[f'Round Robin (Q={quantum})'] = {'tat': hitung_rr(arrival_times, burst_times, quantum)[2], 'wt': hitung_rr(arrival_times, burst_times, quantum)[3]}
                
                if len(priority_times) == len(arrival_times):
                    comparison_data['PRI (Non-Preemptive)'] = {'tat': hitung_priority(arrival_times, burst_times, priority_times)[2], 'wt': hitung_priority(arrival_times, burst_times, priority_times)[3]}
                    comparison_data['PRI (Preemptive)'] = {'tat': hitung_priority_preemptive(arrival_times, burst_times, priority_times)[2], 'wt': hitung_priority_preemptive(arrival_times, burst_times, priority_times)[3]}

            else:
                hasil = "error_len"
        except Exception as e:
            print(f"Error: {e}")
            hasil = "error_val"

    return render_template('index.html', hasil=hasil, gantt=gantt, rata_tat=rata_tat, 
                           rata_wt=rata_wt, rata_rt=rata_rt, cpu_util=cpu_util, 
                           throughput=throughput, inputs_json=inputs_json, 
                           selected_algo=selected_algo, quantum=quantum, 
                           comparison_data=comparison_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)