import random
import string
from warnings import resetwarnings
import requests
import time
import statistics
import queue
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np

from requests.api import request

ALLOWED_CHARS = string.ascii_letters
MAX = 1000
WORKERS = 16


print("Initializing tests...")
def randstr(a, b):
    return "".join((random.choice(ALLOWED_CHARS) for k in range(random.randint(a, b))))

def generate_random_data():
    return {
        "vr_username": randstr(5, 10),
        "first_name": randstr(5, 15),
        "last_name": randstr(5, 15),
        "email": randstr(5, 15) + "@" + randstr(3, 10) + "." + randstr(2, 4),
        "phone_number": "".join((str(random.randint(0, 9)) for k in range(10)))
    }

def make_request(payload):
    ts = time.perf_counter()
    r = requests.post("http://localhost:1337/shotgun-cotisant/", json=payload)
    t = time.perf_counter()-ts
    return t, r

class Worker(Thread):
    def __init__(self, request_queue):
        Thread.__init__(self)
        self.queue = request_queue
        self.times = []
        self.responses = []
    def run(self):
        while True:
            payload = self.queue.get()
            if not payload:
                break
            t, r = make_request(payload)
            self.times.append(t)
            self.responses.append(r)
            self.queue.task_done()

def test(w_nb):
    status_codes = {}
    errors = []
    q = queue.Queue()
    responses = []
    times = []
    workers = []
    for k in range(w_nb):
        q.put(generate_random_data())
    time_start = time.perf_counter()
    for _ in range(WORKERS):
        worker = Worker(q)
        worker.start()
        workers.append(worker)
    for _ in workers:
        q.put("")
    for w in workers:
        w.join()
    for w in workers:
        times.extend(w.times)
        responses.extend(w.responses)
    for r in responses:
        if r.status_code in status_codes.keys():
            status_codes[r.status_code] += 1
        else:
            status_codes[r.status_code] = 1
        if str(r.status_code)[0] == "4":
            errors.append(r.json()["detail"])
    total_time = time.perf_counter() - time_start
    mean_request_time = statistics.mean(times)
    return total_time, mean_request_time, errors

print("Beggining workers test")
total_times = []
mean_times = []
errors = []
for w in range(1, 17):
    t, m, e = test(w)
    total_times.append(t)
    mean_times.append(m)
    errors.extend(e)
print("Tests ended, plotting")
X = np.array(range(1, 17))
Y1 = np.array(total_times)
# Y2 = np.array(mean_times)
print(total_times)
print(errors)
# print(mean_times)
plt.plot(X, Y1)
plt.show()

