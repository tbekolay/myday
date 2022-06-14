from datetime import date, datetime
import os
import pickle
import webbrowser

import black
import click
import requests


def save_token(token):
    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    with open(token_path, "wb") as fp:
        pickle.dump(token, fp)


def load_token():
    with open(token_path, "rb") as fp:
        return pickle.load(fp)


def req_token(save=False):
    uri = f"{base_url}api?client_id={client_id}&redirect_uri={redirect_uri}"
    webbrowser.open(uri)
    code = input("What is the code= in the URL? ")
    print(code)

    access_token_url = "https://app.clickup.com/api/v2/oauth/token"
    r = requests.post(
        access_token_url,
        data={"client_id": client_id, "client_secret": client_secret, "code": code},
    )
    return r.json()


def get_token():
    try:
        token = load_token()
    except FileNotFoundError:
        token = req_token()
        save_token(token)
    return token


def req(endpoint, token):
    return requests.get(
        f"{base_url}api/v2/{endpoint}",
        headers={
            "Accept": "application/json",
            "x-api-key": client_id,
            "Authorization": token["access_token"],
        },
    ).json()


client_id = "C6XW91KMDU91YE6JGN60N4BV3UYBFEM2"
client_secret = "IIM76BD7NXJAQVWNC1059SBZZLU2K0ZD8DI3T1PIQSXGCLH4Q0J0N5XV11GM2P3C"
redirect_uri = "http://localhost:4000/"

token_path = os.path.join(click.get_app_dir("myday"), "clickup.pkl")
base_url = "https://app.clickup.com/"


token = get_token()

team = 2289609
spaces = {
    "personal": 4274443,
    "work": 4276625,
    "recipes": 4274789,
}

lists = {"personal": {"chores": 16851936}}


def pp(obj):
    print(black.format_str(str(obj), mode=black.FileMode()))


start = int(datetime.combine(date.today(), datetime.min.time()).timestamp() * 1000)
stop = int(datetime.combine(date.today(), datetime.max.time()).timestamp() * 1000)

# pp(req(f"team/{team}/space", token))
# pp(req(f"space/{spaces['personal']}/list", token))
# pp(req(f"list/{lists['personal']['chores']}/task", token))
# pp(req(f"team/{team}/task?page=0&due_date_gt={start}&due_date_lt={stop}", token))

tasks = req(f"team/{team}/task?page=0&due_date_gt={start}&due_date_lt={stop}", token)
tasks = [
    f"{','.join(tag['name'] for tag in task['tags'])}"
    f"{': ' if len(task['tags']) > 0 else ''}"
    f"{task['name']}"
    for task in tasks["tasks"]
]
tasks.sort()
for task in tasks:
    print(task)
