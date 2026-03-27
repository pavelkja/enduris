import os

import requests

STRAVA_API_BASE = "https://www.strava.com/api/v3"
STRAVA_OAUTH_TOKEN_URL = "https://www.strava.com/oauth/token"


def refresh_access_token(user, db):
    if not user or not user.refresh_token:
        print("❌ Cannot refresh token: missing user or refresh_token")
        return None

    payload = {
        "client_id": os.getenv("STRAVA_CLIENT_ID"),
        "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": user.refresh_token,
    }

    response = requests.post(
        STRAVA_OAUTH_TOKEN_URL,
        data=payload,
        timeout=(5, 30)
    )

    if response.status_code != 200:
        print(f"❌ Token refresh failed: {response.status_code} {response.text}")
        return None

    tokens = response.json()

    user.access_token = tokens.get("access_token")
    user.refresh_token = tokens.get("refresh_token")

    db.commit()

    print("✅ Token refreshed successfully")

    return user.access_token


def get_athlete_activities(
    access_token,
    page=1,
    per_page=30,
    after=None,
    db=None,
    user=None
):
    """
    Stáhne aktivity uživatele ze Strava API.
    """

    url = f"{STRAVA_API_BASE}/athlete/activities"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "page": page,
        "per_page": per_page
    }

    if after:
        params["after"] = after

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=(5, 30)
    )

    # 🔥 pokud token expiroval → refresh + 1 retry
    if response.status_code == 401 and db is not None and user is not None:
        print("🔑 Access token expired, refreshing...")

        new_token = refresh_access_token(user=user, db=db)

        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=(5, 30)
            )
        else:
            print("❌ Token refresh failed, aborting request")

    response.raise_for_status()

    return response.json()



def get_activity_streams(activity_id, access_token, db=None, user=None):
    url = f"{STRAVA_API_BASE}/activities/{activity_id}/streams"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "keys": "heartrate,speed,altitude,cadence",
        "key_by_type": "true",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=(5, 30),
    )

    if response.status_code == 401 and db is not None and user is not None:
        print("🔑 Access token expired, refreshing...")

        new_token = refresh_access_token(user=user, db=db)

        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=(5, 30),
            )

    if response.status_code != 200:
        print(f"❌ Stream fetch failed: {activity_id} {response.status_code}")
        return {}

    payload = response.json()
    parsed_streams = {}

    for stream_type, stream_payload in payload.items():
        data = stream_payload.get("data")
        if data:
            parsed_streams[stream_type] = data

    return parsed_streams
