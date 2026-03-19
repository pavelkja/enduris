import requests


STRAVA_API_BASE = "https://www.strava.com/api/v3"


def get_athlete_activities(access_token, page=1, per_page=30, after=None):
    """
    Stáhne aktivity uživatele ze Strava API.

    Parametry:
    access_token : str
    page : int
    per_page : int
    after : unix timestamp (optional)

    Pokud je after nastavený, Strava vrátí pouze aktivity po tomto čase.
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

    response = requests.get(url, headers=headers, params=params, timeout=(5, 30))

    response.raise_for_status()

    return response.json()