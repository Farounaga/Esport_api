from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
import enum

# Enums pour Pydantic (si nécessaire)
# Vous pouvez utiliser les mêmes que dans models.py, ou simplement String

# --- Schémas Utilisateur ---
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username_or_email: str # Peut être un email ou un nom d'utilisateur
    password: str

class User(UserBase):
    id: int
    uuid: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # Pour la compatibilité avec l'ORM

# --- Schémas ProfilUtilisateur ---
class UserProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    timezone: Optional[str] = None
    discord_username: Optional[str] = None
    steam_id: Optional[str] = None
    twitch_username: Optional[str] = None
    skill_level: Optional[str] = None # On utilise str pour la simplicité
    looking_for: Optional[str] = None
    is_available_now: Optional[bool] = None
    profile_visibility: Optional[str] = "public"
    show_stats: Optional[bool] = True
    allow_friend_requests: Optional[bool] = True

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Schémas Jeu ---
class GameBase(BaseModel):
    name: str
    slug: str
    category: str

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Schémas DemandeDeMatch ---
class MatchRequestBase(BaseModel):
    game_id: int
    request_type: str
    available_from: datetime
    available_until: datetime
    min_players: Optional[int] = 1
    max_players: Optional[int] = 5

class MatchRequestCreate(MatchRequestBase):
    # Vous pouvez ajouter une validation des champs JSON si nécessaire
    preferred_skill_levels: Optional[List[str]] = Field(default_factory=list)
    preferred_game_modes: Optional[List[str]] = Field(default_factory=list)
    preferred_roles: Optional[List[str]] = Field(default_factory=list)

class MatchRequest(MatchRequestBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Schémas Match ---
class MatchBase(BaseModel):
    match_request_id: int
    matched_user_id: int
    game_id: int
    suggested_game_mode: Optional[str] = None
    suggested_role: Optional[str] = None
    expires_at: datetime

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    compatibility_score: Optional[float] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Schémas Token ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    