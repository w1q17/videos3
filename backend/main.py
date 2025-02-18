from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from s3_manager import MinioManager

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Хардкодим учетные данные (в реальном приложении использовать базу данных)
VALID_CREDENTIALS = {
    "email": "rumden@tpu.ru",
    "password": "password123"
}

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
async def read_root():
    return FileResponse("../frontend/index.html")

@app.post("/api/login")
async def login(login_request: LoginRequest):
    if (login_request.email == VALID_CREDENTIALS["email"] and 
        login_request.password == VALID_CREDENTIALS["password"]):
        
        # Создаем имя бакета из email (убираем @tpu.ru)
        bucket_name = login_request.email.split('@')[0]
        
        # Инициализируем MinIO клиент
        minio = MinioManager()
        
        # Проверяем существование бакета
        if not minio.bucket_exists(bucket_name):
            if not minio.create_bucket(bucket_name):
                raise HTTPException(status_code=500, detail="Ошибка создания бакета")
        
        # Получаем список видео
        videos = minio.list_objects(bucket_name)
        
        return {
            "success": True,
            "bucket_name": bucket_name,
            "videos": videos or []
        }
    
    raise HTTPException(status_code=401, detail="Неверные учетные данные") 