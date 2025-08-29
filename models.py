from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, JSON, DECIMAL, Date, UniqueConstraint, Index, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
import enum

# Enums (si une typage stricte est nécessaire, sinon on peut utiliser String)
class SkillLevelEnum(str, enum.Enum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'
    expert = 'expert'

class UserGameSkillLevelEnum(str, enum.Enum):
    bronze = 'bronze'
    silver = 'silver'
    gold = 'gold'
    platinum = 'platinum'
    diamond = 'diamond'
    master = 'master'
    grandmaster = 'grandmaster'

class RequestTypeEnum(str, enum.Enum):
    quick_match = 'quick_match'
    find_team = 'find_team'
    find_mentor = 'find_mentor'
    find_student = 'find_student'

class MatchStatusEnum(str, enum.Enum):
    pending = 'pending'
    accepted = 'accepted'
    declined = 'declined'
    expired = 'expired'

# --- Modèles ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(100))
    email_verification_expires = Column(DateTime)
    password_reset_token = Column(String(100))
    password_reset_expires = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    ban_reason = Column(Text)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    last_login = Column(TIMESTAMP)

    # Relation
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    games = relationship("UserGame", back_populates="user", cascade="all, delete-orphan")
    match_requests = relationship("MatchRequest", back_populates="user", cascade="all, delete-orphan")
    matches_as_matched_user = relationship("Match", back_populates="matched_user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    avatar_url = Column(String(500))
    bio = Column(Text)
    location = Column(String(100))
    timezone = Column(String(50))
    discord_username = Column(String(100))
    steam_id = Column(String(100))
    twitch_username = Column(String(100))
    preferred_game_modes = Column(JSON)
    preferred_playtime = Column(JSON)
    skill_level = Column(Enum(SkillLevelEnum), default=SkillLevelEnum.beginner)
    looking_for = Column(String(50)) # ENUM dans la BD, mais pour l'instant une chaîne
    availability_schedule = Column(JSON)
    is_available_now = Column(Boolean, default=False)
    profile_visibility = Column(String(20)) # ENUM dans la BD
    show_stats = Column(Boolean, default=True)
    allow_friend_requests = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

    # Relation
    user = relationship("User", back_populates="profile")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    api_identifier = Column(String(100))
    category = Column(String(50)) # ENUM dans la BD
    is_active = Column(Boolean, default=True)
    icon_url = Column(String(500))
    banner_url = Column(String(500))
    description = Column(Text)
    min_players = Column(Integer, default=1)
    max_players = Column(Integer, default=10)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

    # Relation
    user_games = relationship("UserGame", back_populates="game")
    match_requests = relationship("MatchRequest", back_populates="game")
    matches = relationship("Match", back_populates="game")

class UserGame(Base):
    __tablename__ = "user_games"
    __table_args__ = (UniqueConstraint('user_id', 'game_id', name='unique_user_game'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    skill_level = Column(Enum(UserGameSkillLevelEnum), default=UserGameSkillLevelEnum.bronze)
    current_rank = Column(String(100))
    peak_rank = Column(String(100))
    hours_played = Column(Integer, default=0)
    is_main_game = Column(Boolean, default=False)
    game_username = Column(String(100))
    stats = Column(JSON)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

    # Relations
    user = relationship("User", back_populates="games")
    game = relationship("Game", back_populates="user_games")

class MatchRequest(Base):
    __tablename__ = "match_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    request_type = Column(String(20)) # ENUM dans la BD
    preferred_skill_levels = Column(JSON)
    preferred_game_modes = Column(JSON)
    preferred_roles = Column(JSON)
    min_players = Column(Integer, default=1)
    max_players = Column(Integer, default=5)
    available_from = Column(DateTime, nullable=False)
    available_until = Column(DateTime, nullable=False)
    status = Column(String(20)) # ENUM dans la BD, par défaut 'active'
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

    # Relations
    user = relationship("User", back_populates="match_requests")
    game = relationship("Game", back_populates="match_requests")
    matches = relationship("Match", back_populates="match_request") # Supposons qu'une requête puisse avoir plusieurs matches ?

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_request_id = Column(Integer, ForeignKey('match_requests.id'), nullable=False)
    matched_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    compatibility_score = Column(DECIMAL(3,2))
    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    suggested_game_mode = Column(String(50))
    suggested_role = Column(String(50))
    status = Column(Enum(MatchStatusEnum), default=MatchStatusEnum.pending)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

    # Relations
    match_request = relationship("MatchRequest", back_populates="matches")
    matched_user = relationship("User", back_populates="matches_as_matched_user")
    game = relationship("Game", back_populates="matches")

# Ajoutez des index si c'est important pour la performance, mais pour le MVP on peut se contenter de ceux dans la BD.