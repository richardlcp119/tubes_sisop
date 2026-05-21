from flask import Flask, render_template, request
from algoritma.fcfs import hitung_fcfs
from algoritma.sjf_np import hitung_sjf
from algoritma.priorityscheduling_np import hitung_priority

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    gantt = None
    rata_tat = 0
    rata_wt = 0
    throughput = 0
    inputs = {'arrival': '', 'burst': '', 'priority': '', 'algo': 'fcfs'}

    if request.method == 'POST':
        try:
            algo = request.form.get('algorithm', 'fcfs')
            arrival_raw = request.form.get('arrival_times', '')
            burst_raw = request.form.get('burst_times', '')
            priority_raw = request.form.get('priority_times', '')
            
            inputs['arrival'] = arrival_raw
            inputs['burst'] = burst_raw
            inputs['priority'] = priority_raw
            inputs['algo'] = algo

            arrival_times = [int(x) for x in arrival_raw.split()]
            burst_times = [int(x) for x in burst_raw.split()]

            if len(arrival_times) != len(burst_times) or len(arrival_times) == 0:
                hasil = "error_len"
            else:
                if algo == 'fcfs':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_fcfs(arrival_times, burst_times)
                elif algo == 'sjf':
                    hasil, gantt, rata_tat, rata_wt, throughput = hitung_sjf(arrival_times, burst_times)
                elif algo == 'priority_np':
                    priorities = [int(x) for x in priority_raw.split()]
                    if len(priorities) != len(arrival_times):
                        hasil = "error_priority_len"
                    else:
                        hasil, gantt, rata_tat, rata_wt, throughput = hitung_priority(arrival_times, burst_times, priorities)
        except ValueError:
            hasil = "error_val"

    return render_template('index.html', hasil=hasil, gantt=gantt, 
                           rata_tat=rata_tat, rata_wt=rata_wt, 
                           throughput=throughput, inputs=inputs)

if __name__ == '__main__':
    app.run(debug=True)