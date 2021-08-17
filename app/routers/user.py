from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from ..core.dependencies import get_db, get_current_user
from ..models import User
from app.crud.user import get_available_subjects, update_subjects

from typing import List

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/subjects")
def subjects(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_available_subjects(db, current_user)


@router.post("/subjects/choose", status_code=200)
def subjects_select(
    subject_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    update_subjects(db, subject_ids, current_user)
