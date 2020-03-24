from multiprocessing import Manager, Process
from time import sleep

from flask import Flask

from config import Config
from metrics import Metrics

app = Flask(__name__)
manager = Manager()
metrics = manager.list()


@app.route("/metrics", methods=["GET"])
def metrics_endpoint():
    if metrics:
        return metrics[0].to_prometheus()
    else:
        return "GitlabStats has not yet finished collecting statistics..."


@app.before_first_request
def background_job():
    def update_metrics():
        while True:
            print("Fetching stats...")
            temp = Metrics()
            if len(metrics) > 0:
                metrics.pop(0)
            metrics.append(temp)
            print("Done!")
            print(f"Sleeping for {Config.update_freq} seconds...")
            sleep(Config.update_freq)

    update_process = Process(target=update_metrics)
    update_process.start()
