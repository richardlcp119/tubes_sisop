from flask import Flask, render_template, request
from algoritma.fcfs import hitung_fcfs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    gantt = None
    rata_tat = 0
    rata_wt = 0
    throughput = 0
    inputs = {'arrival': '', 'burst': ''}

    if request.method == 'POST':
        try:
            # Ambil data string dari form HTML
            arrival_raw = request.form.get('arrival_times', '')
            burst_raw = request.form.get('burst_times', '')
            
            # Simpan kembali ke form agar input tidak hilang saat di-refresh
            inputs['arrival'] = arrival_raw
            inputs['burst'] = burst_raw

            # Ubah string spasi "2 4 6" menjadi list angka [2, 4, 6]
            arrival_times = [int(x) for x in arrival_raw.split()]
            burst_times = [int(x) for x in burst_raw.split()]

            if len(arrival_times) == len(burst_times) and len(arrival_times) > 0:
                hasil, gantt, rata_tat, rata_wt, throughput = hitung_fcfs(arrival_times, burst_times)
            else:
                hasil = "error_len"
        except ValueError:
            hasil = "error_val"

    return render_template('index.html', hasil=hasil, gantt=gantt, 
                           rata_tat=rata_tat, rata_wt=rata_wt, 
                           throughput=throughput, inputs=inputs)

if __name__ == '__main__':
    app.run(debug=True)