from datetime import date, datetime, timezone
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


def req_token():
    redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
    uri = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={client_id}"
        "&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
        f"&scope={scope}"
        "&response_type=code"
    )
    print(uri)
    webbrowser.open(uri)
    code = input("What is the code= in the URL? ")
    print(code)

    r = requests.post(
        access_token_url,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    token = r.json()
    save_token(token)
    return token


def refresh_token(token):
    assert "refresh_token" in token
    r = requests.post(
        access_token_url,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": token["refresh_token"],
            "grant_type": "refresh_token",
        },
    )
    token.update(r.json())
    save_token(token)
    return token


def get_token():
    try:
        token = load_token()
    except FileNotFoundError:
        token = req_token()
    return token


def req(endpoint, token):
    uri = f"https://www.googleapis.com/calendar/v3/{endpoint}"
    r = requests.get(uri, headers={"Authorization": f"Bearer {token['access_token']}"},)
    if r.status_code == 401 and r.reason == "Unauthorized":
        token = refresh_token(token)
        r = requests.get(
            uri, headers={"Authorization": f"Bearer {token['access_token']}"},
        )
    return r.json()


client_id = "1043144290628-dkl3gq00tddto38t83g45mn25inl2b9l.apps.googleusercontent.com"
client_secret = "z0X6WT1wWhA3_ZwiKR1k3D3Q"
scope = "https://www.googleapis.com/auth/calendar.readonly"
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
access_token_url = "https://accounts.google.com/o/oauth2/token"


token_path = os.path.join(click.get_app_dir("myday"), "gcal.pkl")
token = get_token()
assert token["token_type"] == "Bearer"


def pp(obj):
    print(black.format_str(str(obj), mode=black.FileMode()))


my_cal = "tbekolay@gmail.com"

# pp(req(f"users/me/calendarList", token))
start = (
    datetime.combine(date(2020, 8, 22), datetime.min.time()).astimezone().isoformat()
)
stop = datetime.combine(date(2020, 8, 22), datetime.max.time()).astimezone().isoformat()

events = req(f"calendars/primary/events?timeMin={start}&timeMax={stop}", token)
events = [
    f"{datetime.fromisoformat(event['start']['dateTime']):%H:%M}: {event['summary']}"
    for event in events["items"]
]
events.sort()
for event in events:
    print(event)
