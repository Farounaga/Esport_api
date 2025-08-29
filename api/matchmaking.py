from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/matchmaking", tags=["matchmaking"])

@router.post("/requests/", response_model=schemas.MatchRequest)
def create_match_request(request: schemas.MatchRequestCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # On peut ajouter des vérifications, par exemple, si le jeu existe
    db_game = db.query(models.Game).filter(models.Game.id == request.game_id).first()
    if not db_game:
         raise HTTPException(status_code=400, detail="Game not found")

    db_request = models.MatchRequest(user_id=current_user.id, **request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/requests/me", response_model=list[schemas.MatchRequest])
def read_my_match_requests(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    requests = db.query(models.MatchRequest).filter(models.MatchRequest.user_id == current_user.id).all()
    return requests

@router.get("/matches/me", response_model=list[schemas.Match])
def read_my_matches(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
     # On suppose que l'utilisateur voit les matchs où il était "matched_user"
    matches = db.query(models.Match).filter(models.Match.matched_user_id == current_user.id).all()
    return matches