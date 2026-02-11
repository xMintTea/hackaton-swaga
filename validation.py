from utils.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session, Query


from auth import utils_jwt
from schemas.users import User as UserSchema
from models import User
from utils.db_helpher import get_db
from routers.users import get_users

oath2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/",)


def validate_token_type(
    payload: dict,
    token_type: str
) -> bool:
    
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type  == token_type:
        return True
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {current_token_type!r} expected {token_type!r}"
        )


def get_current_token_payload(
    token: str = Depends(oath2_scheme)
    ) -> dict:
    try:
        payload = utils_jwt.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Token Error: {e}")

    return payload
    

def get_user_by_token_sub(payload: dict, users: Query) -> UserSchema:
    user_id: str | None = payload.get("sub")

    if user:=users.where(User.id == user_id).first():
        
        return user
    

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid username or password")


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
        users: Query = Depends(get_users)
    ) -> UserSchema:
        validate_token_type(payload,token_type)
        return get_user_by_token_sub(payload, users)
    
    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)
