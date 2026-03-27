from app.services.daily_metrics import compute_daily_metrics
from app.core.database import SessionLocal
from app.models.user import User

import app.models.activity
import app.models.activity_stream
import app.models.activity_metric
import app.models.user

def main():
    db = SessionLocal()

    # vezmeme prvního usera (pro test)
    user = db.query(User).first()

    if not user:
        print("No users found")
        return

    print(f"Computing daily metrics for user: {user.id}")

    compute_daily_metrics(str(user.id))

    print("Done")


if __name__ == "__main__":
    main()