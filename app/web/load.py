import multiprocessing
import time
from datetime import datetime

from flask import Blueprint, current_app, request

from app.constants import default_timeout, default_timeout_value

bp = Blueprint("load", __name__)


def do_fibonacci() -> (int, int):
    f1, f2 = 0, 1  # 1, 2, 3, 5, 8, 13, 21, 44...
    while True:
        f1, f2 = f2, f1 + f2


@bp.route("/load")
def load():
    # query parameter ?timeout=
    timeout = int(
        request.args.get(
            "timeout",
            current_app.config.get(default_timeout, default_timeout_value),
        )
    )
    processes = list()
    for _ in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(target=do_fibonacci)
        process.start()
        processes.append(process)
    time.sleep(timeout)
    for process in processes:
        process.terminate()
    return f"done at {datetime.now()}"
