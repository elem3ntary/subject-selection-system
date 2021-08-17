from fastapi import APIRouter, HTTPException
from fastapi.openapi.models import HTTPBase
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from ..schemas import SubjectBase
from ..schemas import Subject as SubjectScheme
from ..core.dependencies import get_admin_user, get_db
from ..crud.subject import create_subject, update_subject, delete_subject
from app.crud.user import update_config
from ..models import Subject

router = APIRouter(
    prefix="/admin", tags=["admin"], dependencies=[Depends(get_admin_user)]
)


@router.post("/subject/create", response_model=SubjectScheme, status_code=201)
def subject_create(subject: SubjectBase, db: Session = Depends(get_db)):
    db_subject: Subject = create_subject(db, subject)
    return db_subject


@router.put("/subject/{subject_id}", status_code=200)
def subject_update(
    subject_id: int, new_subject: SubjectBase, db: Session = Depends(get_db)
):
    result = update_subject(db, subject_id, new_subject)
    if not result:
        raise HTTPException(400, "Error updating subject")


@router.delete("/subject/{subject_id}", status_code=200)
def subject_delete(subject_id: int, db: Session = Depends(get_db)):
    result = delete_subject(db, subject_id)
    if not result:
        raise HTTPException(400, "Error deleting subject")


@router.patch("/config", status_code=200)
def config_update(props: dict, db: Session = Depends(get_db)):
    result = update_config(db, props)
    if not result:
        raise HTTPException(400, "Error updating config")
