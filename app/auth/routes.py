from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.auth.models import User, Module, UserModule
from app.auth.schemas import UserCreate, Token, ModuleCreate, ModuleAssign
from app.auth.main import get_password_hash, verify_password, authenticate_user, create_access_token
from app.database import get_db
from uuid import uuid4
import os

router = APIRouter()

# Endpoints
@router.get("/ping")
def read_root():
    return {"message": "pong! :)"}

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/{module_name}/login", response_model=Token)
def module_login(
    user_data: UserCreate,
    module_name: str = Path(..., title="Module name (e.g. 'moneyfy')"),
    db: Session = Depends(get_db)
):
    # 1. Verificar credenciales del usuario
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print(f"User {user.email} authenticated successfully")
    # 2. Buscar el módulo
    module = db.query(Module).filter(Module.name == module_name).first()
    if not module:
        raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found")

    # 3. Verificar si el usuario tiene acceso al módulo
    user_module = db.query(UserModule).filter_by(user_id=user.id, module_id=module.id).first()
    if not user_module:
        raise HTTPException(
            status_code=403,
            detail=f"User does not have access to module '{module_name}'"
        )

    # 4. Crear token con info del módulo
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "module": module.name
    }
    token = create_access_token(token_data)

    return {"access_token": token, "token_type": "bearer"}

@router.post("/modules", response_model=dict)
def create_module(module_data: ModuleCreate, db: Session = Depends(get_db)):
    existing = db.query(Module).filter(Module.name == module_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Module already exists")

    module = Module(id=str(uuid4()), name=module_data.name)
    db.add(module)
    db.commit()
    db.refresh(module)
    return {"message": f"Module '{module.name}' created successfully", "id": module.id}

@router.post("/modules/assign", response_model=dict)
def assign_user_to_module(
    assignment_data: ModuleAssign,
    db: Session = Depends(get_db)
):
    # Buscar módulo
    module = db.query(Module).filter(Module.name == assignment_data.module).first()
    if not module:
        raise HTTPException(status_code=404, detail=f"Module '{assignment_data.module}' not found")

    # Verificar usuario
    user = db.query(User).filter(User.email == assignment_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar si ya está asociado
    existing = db.query(UserModule).filter_by(user_id=user.id, module_id=module.id).first()
    if existing:
        return {"message": f"User already assigned to module '{assignment_data.module}'"}

    # Asociar
    user_module = UserModule(user_id=user.id, module_id=module.id)
    db.add(user_module)
    db.commit()
    return {"message": f"User '{assignment_data.email}' assigned to module '{assignment_data.module}'"}


@router.get("/check-token", response_model=dict)
def check_token(
    token: str,
    db: Session = Depends(get_db)
):
    try:
        # Decodificar el token
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id = payload.get("sub")
        module_name = payload.get("module")

        if not user_id or not module_name:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Verificar si el usuario existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verificar si el módulo existe
        module = db.query(Module).filter(Module.name == module_name).first()
        if not module:
            raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found")

        # Verificar si el usuario tiene acceso al módulo
        user_module = db.query(UserModule).filter_by(user_id=user.id, module_id=module.id).first()
        if not user_module:
            raise HTTPException(
                status_code=403,
                detail=f"User does not have access to module '{module_name}'"
            )

        return {"message": "Token is valid and user has access to the module"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/refresh-token", response_model=Token)
def refresh_token(
    token: str,
    db: Session = Depends(get_db)
):
    try:
        # Intentar decodificar el token para verificar su validez
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"], options={"verify_exp": False})
        user_id = payload.get("sub")
        module_name = payload.get("module")

        if not user_id or not module_name:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Verificar si el usuario existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verificar si el módulo existe
        module = db.query(Module).filter(Module.name == module_name).first()
        if not module:
            raise HTTPException(status_code=404, detail=f"Module '{module_name}' not found")

        # Verificar si el usuario tiene acceso al módulo
        user_module = db.query(UserModule).filter_by(user_id=user.id, module_id=module.id).first()
        if not user_module:
            raise HTTPException(
                status_code=403,
                detail=f"User does not have access to module '{module_name}'"
            )

        # Crear un nuevo token
        new_token = create_access_token(data={"sub": str(user.id), "module": module_name})
        return {"access_token": new_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

