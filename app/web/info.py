import urllib.request

from flask import Blueprint

bp = Blueprint("info", __name__)


@bp.route("/info")
def info():
    url = "http://169.254.169.254/latest/meta-data/"
    with urllib.request.urlopen(url) as f:
        return f.read()
