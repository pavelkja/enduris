from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.dashboard_service import get_dashboard_months, get_dashboard_ytd

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/ytd")
def dashboard_ytd(
    user_id: str = Query(..., description="User UUID"),
    sport: str = Query(..., description="ride | run | cycling_overall"),
    db: Session = Depends(get_db),
):
    try:
        return get_dashboard_ytd(db=db, user_id=user_id, sport=sport)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/months")
def dashboard_months(
    user_id: str = Query(..., description="User UUID"),
    sport: str = Query(..., description="ride | run | cycling_overall"),
    db: Session = Depends(get_db),
):
    try:
        return get_dashboard_months(db=db, user_id=user_id, sport=sport)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
