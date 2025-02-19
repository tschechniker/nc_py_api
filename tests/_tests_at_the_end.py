import os
import sys
from subprocess import Popen

from ._install_wait import check_heartbeat

# These tests will be run separate, and at the end of all other tests.


def test_ex_app_enable_disable(nc_client, nc_app):
    child_environment = os.environ.copy()
    child_environment["APP_PORT"] = os.environ.get("APP_PORT", "9009")
    r = Popen(
        [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_install_only_enabled_handler.py")],
        env=child_environment,
        cwd=os.getcwd(),
    )
    url = f"http://127.0.0.1:{child_environment['APP_PORT']}/heartbeat"
    try:
        if check_heartbeat(url, '"status":"ok"', 15, 0.3):
            raise RuntimeError("`_install_only_enabled_handler` can not start.")
        if nc_client.apps.ex_app_is_enabled("nc_py_api"):
            nc_client.apps.ex_app_disable("nc_py_api")
        assert nc_client.apps.ex_app_is_disabled("nc_py_api") is True
        assert nc_client.apps.ex_app_is_enabled("nc_py_api") is False
        nc_client.apps.ex_app_enable("nc_py_api")
        assert nc_client.apps.ex_app_is_disabled("nc_py_api") is False
        assert nc_client.apps.ex_app_is_enabled("nc_py_api") is True
    finally:
        r.terminate()
