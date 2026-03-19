from app.core.database import SessionLocal
from app.models.user import User
from app.services.activity_importer import import_activities


def main():

    db = SessionLocal()

    try:

        # zatím vezmeme prvního uživatele
        user = db.query(User).first()

        if not user:
            print("No users found in database.")
            return

        print(f"Starting activity sync for user {user.id}")

        imported = import_activities(
            db=db,
            user_id=user.id,
            access_token=user.access_token
        )

        print(f"Import finished. Imported {imported} activities.")

    finally:
        db.close()


if __name__ == "__main__":
    main()