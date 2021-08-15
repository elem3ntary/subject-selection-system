from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from ..core.dependencies import get_db

router = APIRouter(prefix=["user"], tags=["user"], dependencies=[Depends()])


@router.get("/subjects")
def subjects(db: Session = Depends(get_db)):
    ...
