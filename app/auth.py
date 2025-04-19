from fastapi import APIRouter  ,Depends ,HTTPException, status 
from fastapi.security import OAuth2PasswordBearer 
from passlib.context import CryptContext
from jose import jwt , JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from pathlib import Path
from dotenv import load_dotenv
from app.settings import get_settings

env_path = Path('.')/'.env'
load_dotenv(env_path,override=True)
print(env_path)


sett = get_settings()

SECRET_KEY = sett.SECRET_KEY
ALGORITHM = sett.ALGORITHM

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
username = sett.username
password = sett.password
hashed_password = bcrypt_context.hash(password)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/token")


def authenticate_user(usrname,password_raw):
    if ((usrname == username) and (bcrypt_context.verify(password_raw,hashed_password))) :
        return True
    return False

def create_access_token(username):
    encode = {'username':username}
    tokn = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    print(f"Token = {tokn}")
    return tokn

async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('username')
        if username is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate User .........")
        return {'username':username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate User .........")

app_auth = APIRouter()



@app_auth.post("/token")
async def login(username: Annotated[str, Form(...)], password: Annotated[str, Form(...)]):
    print(f"""{Form(...)} ===> {Form(...)}""")
    is_user_authorised = authenticate_user(username,password)
    if not is_user_authorised:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    TKN = create_access_token(username)
    return {"access_token": TKN, "token_type": "bearer"}


@app_auth.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app_auth.get("/check_token_validation/")
async def check_token_validation(token: Annotated[str, Depends(oauth2_scheme)]):
    usr = await get_current_user(token)
    return usr
