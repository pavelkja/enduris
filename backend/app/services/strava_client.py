import requests
import os

STRAVA_API_BASE = "https://www.strava.com/api/v3"
STRAVA_OAUTH_TOKEN_URL = "https://www.strava.com/oauth/token"

def refresh_access_token(db, user):
        """
        Obnoví Strava access token přes refresh token a uloží nové tokeny do DB.
        """
        if not user or not user.refresh_token:
            return None

        data = {
            "client_id": os.getenv("STRAVA_CLIENT_ID"),
            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
            "grant_type": "refresh_token",
            "refresh_token": user.refresh_token
        }

        response = requests.post(STRAVA_OAUTH_TOKEN_URL, data=data, timeout=(5, 30))

        if response.status_code != 200:
            print(f"❌ Token refresh failed: {response.status_code} {response.text}")
            return None

        tokens = response.json()
        user.access_token = tokens["access_token"]
        user.refresh_token = tokens["refresh_token"]
        db.commit()
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

    # pokud token expiroval, zkusíme refresh + 1 retry
    if response.status_code == 401 and db is not None and user is not None:
        print("🔑 Access token expired while fetching activities, trying refresh...")
        new_token = refresh_access_token(db=db, user=user)

        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.get(url, headers=headers, params=params, timeout=(5, 30))

    
    response.raise_for_status()

    return response.json()
