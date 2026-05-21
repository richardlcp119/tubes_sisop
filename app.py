from flask import Flask, render_template, request
import json
from algoritma.fcfs import hitung_fcfs
from algoritma.sjf_np import hitung_sjf
from algoritma.priorityscheduling_np import hitung_priority
from algoritma.rr import hitung_rr  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    gantt = None
    rata_tat = 0
    rata_wt = 0
    throughput = 0
    quantum = 2  # Nilai default awal Quantum
    
    # State awal untuk baris input dinamis komponen Alpine
    inputs_json = '[{"arrival": "", "burst": "", "priority": ""}]'
    selected_algo = 'fcfs'

    if request.method == 'POST':
        try:
            selected_algo = request.form.get('algorithm', 'fcfs')
            
            # Ambil nilai quantum khusus untuk algoritma Round Robin
            quantum_raw = request.form.get('quantum', '2')
            if quantum_raw.strip() != '':
                quantum = int(quantum_raw)
            
            # Ambil data input array list dari komponen dinamis HTML
            arrival_raw = request.form.getlist('arrival[]')
            burst_raw = request.form.getlist('burst[]')
            priority_raw = request.form.getlist('priority[]')
            
            # Ikat balik semua input ke objek JSON agar data komponen Alpine tidak hilang pasca-POST
            inputs_data = [
                {
                    'arrival': a, 
                    'burst': b, 
                    'priority': priority_raw[i] if i < len(priority_raw) else ""
                } 
                for i, (a, b) in enumerate(zip(arrival_raw, burst_raw))
            ]
            inputs_json = json.dumps(inputs_data)

            # Konversi elemen teks array ke list data integer (abaikan string kosong)
            arrival_times = [int(x) for x in arrival_raw if x.strip() != '']
            burst_times = [int(x) for x in burst_raw if x.strip() != '']
            priority_times = [int(x) for x in priority_raw if x.strip() != '']

            # Validasi panjang array dasar
            if len(arrival_times) == len(burst_times) and len(arrival_times) > 0:
                if selected_algo == 'fcfs':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_fcfs(arrival_times, burst_times)
                elif selected_algo == 'sjf':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_sjf(arrival_times, burst_times)
                elif selected_algo == 'priority_np':
                    # Pastikan jumlah kolom input prioritas terisi lengkap
                    if len(priority_times) == len(arrival_times):
                        hasil, gantt, rata_tat, rata_wt, throughput = hitung_priority(arrival_times, burst_times, priority_times)
                    else:
                        hasil = "error_priority_len"
                elif selected_algo == 'rr':
                    # Jalankan fungsi hitung Round Robin
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_rr(arrival_times, burst_times, quantum)
            else:
                hasil = "error_len"
        except ValueError:
            hasil = "error_val"

    return render_template('index.html', hasil=hasil, gantt=gantt, 
                           rata_tat=rata_tat, rata_wt=rata_wt, 
                           throughput=throughput, inputs_json=inputs_json,
                           selected_algo=selected_algo, quantum=quantum)

if __name__ == '__main__':
    app.run(debug=True)