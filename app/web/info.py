import http
import logging
import urllib.error
import urllib.request

from flask import Blueprint

logger = logging.getLogger(__name__)
bp = Blueprint("info", __name__)


def retrieve_data(url: str) -> str | None:
    try:
        with urllib.request.urlopen(url) as f:
            logger.info(url, f.status)
            return f.read().decode()
    except urllib.error.HTTPError as ex:
        logger.warning(url, ex.status)
        if ex.status == http.HTTPStatus.NOT_FOUND:
            return None
        else:
            raise ex


def walk(url: str) -> str | dict | None:
    value = retrieve_data(url)
    if not value:
        return None
    if url.endswith("/"):
        info = dict()
        for node in value.split("\n"):
            info[node.rstrip("/")] = walk(url + node)
        return info
    else:
        return value


@bp.route("/info")
def info():
    url = "http://169.254.169.254/latest/meta-data/"
    result = walk(url)
    return result
