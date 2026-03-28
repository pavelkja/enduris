import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.services.dashboard_service import get_efficiency_trend

# ⚠️ sem dej reálné user_id z DB
USER_ID = "b506b832-76f2-48f2-b1a1-e00ccef8b988"


def main():
    db = SessionLocal()

    try:
        data = get_efficiency_trend(db, USER_ID, limit=10)

        print("=== RESULT ===")
        for row in data:
            print(row)

    finally:
        db.close()


if __name__ == "__main__":
    main()
