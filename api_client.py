import requests
from requests.auth import HTTPBasicAuth
from config import LOL_LOCKFILE_PATH

# --- LCU (League Client Update) API Communication ---
def read_lockfile(path=LOL_LOCKFILE_PATH):
    """
    Reads the lockfile created by the League Client to get the port and
    authentication password for the LCU API.
    """
    with open(path, "r") as f:
        name, pid, port, password, protocol = f.read().split(":")
    return port, password

# Read the lockfile to get connection details
try:
    port, password = read_lockfile()
    lcu_auth = HTTPBasicAuth("riot", password)
except (FileNotFoundError, ValueError) as e:
    print(f"Error reading lockfile: {e}. LCU API functions will not work.")
    port, lcu_auth = None, None

def lcu_request(endpoint):
    """Generic GET request to the LCU API."""
    if not port or not lcu_auth:
        return {}
    lcu_url = f"https://127.0.0.1:{port}{endpoint}"
    # The 'verify=False' flag is necessary because the LCU API uses a self-signed certificate.
    try:
        resp = requests.get(lcu_url, auth=lcu_auth, verify=False)
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"LCU API request failed: {e}")
        return {}

# --- Live Client API Communication ---
def live_request(endpoint):
    """Generic GET request to the Live Client API."""
    # The Live Client API uses a fixed port (2999) and no authentication.
    url = f"https://127.0.0.1:2999{endpoint}"
    try:
        resp = requests.get(url, verify=False)
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Live Client API request failed: {e}")
        return {}