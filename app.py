from flask import Flask, render_template, request
import json  # Tambahkan import ini
from algoritma.fcfs import hitung_fcfs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    gantt = None
    rata_tat = 0
    rata_wt = 0
    throughput = 0
    
    # State awal: 1 baris input kosong
    inputs_json = '[{"arrival": "", "burst": ""}]'

    if request.method == 'POST':
        try:
            # Ambil data input array (kolom ganda) dari HTML
            arrival_raw = request.form.getlist('arrival[]')
            burst_raw = request.form.getlist('burst[]')
            
            # Ubah data mentah menjadi JSON agar inputan user tidak hilang saat direfresh
            inputs_data = [{'arrival': a, 'burst': b} for a, b in zip(arrival_raw, burst_raw)]
            inputs_json = json.dumps(inputs_data)

            # Konversi teks ke angka (hanya proses data yang tidak kosong)
            arrival_times = [int(x) for x in arrival_raw if x.strip() != '']
            burst_times = [int(x) for x in burst_raw if x.strip() != '']

            if len(arrival_times) == len(burst_times) and len(arrival_times) > 0:
                hasil, gantt, rata_tat, rata_wt, throughput = hitung_fcfs(arrival_times, burst_times)
            else:
                hasil = "error_len"
        except ValueError:
            hasil = "error_val"

    return render_template('index.html', hasil=hasil, gantt=gantt, 
                           rata_tat=rata_tat, rata_wt=rata_wt, 
                           throughput=throughput, inputs_json=inputs_json)

if __name__ == '__main__':
    app.run(debug=True)