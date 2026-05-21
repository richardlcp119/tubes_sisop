from flask import Flask, render_template, request
import json
from algoritma.fcfs import hitung_fcfs
from algoritma.rr import hitung_rr  

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    gantt = None
    rata_tat = 0
    rata_wt = 0
    throughput = 0
    
    algoritma_terpilih = 'fcfs'
    quantum = ""
    inputs_json = '[{"arrival": "", "burst": ""}]'

    if request.method == 'POST':
        try:
            arrival_raw = request.form.getlist('arrival[]')
            burst_raw = request.form.getlist('burst[]')
            algoritma_terpilih = request.form.get('algorithm')
            quantum_raw = request.form.get('quantum')
            
            inputs_data = [{'arrival': a, 'burst': b} for a, b in zip(arrival_raw, burst_raw)]
            inputs_json = json.dumps(inputs_data)

            arrival_times = [int(x) for x in arrival_raw if x.strip() != '']
            burst_times = [int(x) for x in burst_raw if x.strip() != '']

            if len(arrival_times) == len(burst_times) and len(arrival_times) > 0:
                if algoritma_terpilih == 'fcfs':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_fcfs(arrival_times, burst_times)
                elif algoritma_terpilih == 'rr':
                    quantum = int(quantum_raw) if quantum_raw and quantum_raw.strip() != '' else 2
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_rr(arrival_times, burst_times, quantum)
            else:
                hasil = "error_len"
        except ValueError:
            hasil = "error_val"

    return render_template('index.html', hasil=hasil, gantt=gantt, 
                           rata_tat=rata_tat, rata_wt=rata_wt, 
                           throughput=throughput, inputs_json=inputs_json,
                           algoritma_terpilih=algoritma_terpilih, quantum=quantum)

if __name__ == '__main__':
    app.run(debug=True)