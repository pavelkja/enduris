import time

from app.core.database import SessionLocal
from app.models.activity import Activity
from app.models.user import User
from app.services.stream_importer import import_streams


BATCH_SIZE = 100
SLEEP_SECONDS = 0.3


def main():

    db = SessionLocal()

    try:
        user = db.query(User).first()

        if not user:
            print("❌ No user found")
            return

        activities = (
            db.query(Activity)
            .filter(Activity.streams_imported == False)
            .order_by(Activity.start_date.desc())
            .limit(BATCH_SIZE)
            .all()
        )

        print(f"👉 Activities to process: {len(activities)}")

        if not activities:
            print("✅ Nothing to process")
            return

        success = 0
        failed = 0

        for i, activity in enumerate(activities, start=1):

            print(f"⬇️ [{i}/{len(activities)}] Activity {activity.id}")

            try:
                result = import_streams(db, user, activity)

                if result == "STOP":
                    print("🛑 Batch stopped (rate limit)")
                    break

                # označ jako hotové
                activity.streams_imported = True
                db.commit()

                success += 1
                print(f"✅ Done {activity.id}")

            except Exception as e:
                db.rollback()
                failed += 1

                print(f"❌ Error for {activity.id}: {e}")

            # ochrana proti rate limitu
            time.sleep(SLEEP_SECONDS)

        print("------")
        print(f"✅ Success: {success}")
        print(f"❌ Failed: {failed}")
        print("------")

    finally:
        db.close()


if __name__ == "__main__":
    main()