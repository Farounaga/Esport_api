from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, auth

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/me", response_model=schemas.UserProfile)
def read_my_profile(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()
    if not db_profile:
         # On peut créer automatiquement un profil vide ou retourner 404
         raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.put("/me", response_model=schemas.UserProfile)
def update_my_profile(profile_update: schemas.UserProfileUpdate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    db_profile = db.query(models.UserProfile).filter(models.UserProfile.user_id == current_user.id).first()
    if not db_profile:
        # Créer un nouveau profil
        db_profile = models.UserProfile(user_id=current_user.id, **profile_update.dict(exclude_unset=True))
        db.add(db_profile)
    else:
        # Mettre à jour l'existant
        update_data = profile_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile