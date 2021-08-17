from requests.sessions import session
from ..models import Subject
from ..schemas import SubjectBase
from sqlalchemy.orm import Session


def create_subject(db: Session, subject: SubjectBase) -> Subject:
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    return db_subject


def get_subject_by_id(db: Session, subject_id: int) -> Subject:
    return db.query(Subject).filter_by(id=subject_id).one_or_none()


def update_subject(db: Session, subject_id: int, new_subject: SubjectBase):
    rows_matched = db.query(Subject).filter_by(id=subject_id).update(new_subject.dict())
    db.commit()
    if not rows_matched:
        return False
    return True


def delete_subject(db: Session, subject_id: int):
    rows_matched = db.query(Subject).filter_by(id=subject_id).delete()
    db.commit()
    if not rows_matched:
        return False
    return True
