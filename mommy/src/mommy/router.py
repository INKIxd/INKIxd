import json
import os

from fastapi import APIRouter, HTTPException

from mommy.schemas import StatusResponse, User, UserResponse

router = APIRouter()

DB_FILE = os.path.join(os.path.dirname(__file__), "users_db.json")

# 1. Инициализируем словарь
User_database = {}

# 2. Загружаем данные, если файл существует
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if content:
                User_database = json.loads(content)
    except json.JSONDecodeError:
        print("Файл базы данных пуст или поврежден. Создаем новую базу.")

# 3. Функция сохранения
def save_db():
    global User_database  # Обязательно указываем, что меняем глобальную переменную  # noqa: PLW0602
    with open(DB_FILE, "w", encoding="utf-8") as f:
        dict_to_save = {}
        for login, user in User_database.items():
            # Проверяем: если user - это объект Pydantic (при первой регистрации)
            if hasattr(user, "model_dump"):
                dict_to_save[login] = user.model_dump()
            else:
                # Если user - это уже словарь (загружен из файла)
                dict_to_save[login] = user
        
        json.dump(dict_to_save, f, ensure_ascii=False, indent=4)


@router.get("/status")
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")


@router.post("/signup", status_code=201, response_model=UserResponse)
def signup(user: User):
    global User_database  # noqa: PLW0602

    if user.login in User_database:
        raise HTTPException(409)
    User_database[user.login] = user
    save_db()
    return user


@router.post("/login", response_model=UserResponse)
def login(user : User):
    stored_user = User_database.get(user.login)
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(status_code=401)
    return stored_user
