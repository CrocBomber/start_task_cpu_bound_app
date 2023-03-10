import multiprocessing
import time
from datetime import datetime

from flask import Blueprint, current_app, request

from app.constants import default_timeout, default_timeout_value

bp = Blueprint("load", __name__)


def do_math(timeout):
    start = time.time()
    while time.time() - start < timeout:
        # noinspection PyStatementEffect
        65535 * 65535


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
        process = multiprocessing.Process(target=do_math, args=(timeout,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    return f"done at {datetime.now()}"
