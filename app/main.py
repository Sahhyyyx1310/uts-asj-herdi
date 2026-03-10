import os
import io
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

# --- DATABASE CONFIG ---
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    photo_url = Column(String)

Base.metadata.create_all(bind=engine)

# --- MINIO CONFIG ---
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

bucket_name = os.getenv("MINIO_BUCKET")

# Buat Bucket jika belum ada
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# OTOMATIS SET PUBLIC POLICY (Agar Gambar Muncul)
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Resource": [f"arn:aws:s3:::{bucket_name}"]
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
        }
    ]
}
minio_client.set_bucket_policy(bucket_name, json.dumps(policy))

app = FastAPI()

# --- CORS MIDDLEWARE (Izin Akses Browser) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.post("/users")
async def create_user(name: str = Form(...), email: str = Form(...), file: UploadFile = File(...)):
    # Validasi Ukuran File (Max 5MB) [cite: 44]
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File terlalu besar (Maks 5MB)")

    file_name = f"{email}_{file.filename}".replace(" ", "_")
    minio_client.put_object(
        bucket_name, file_name, io.BytesIO(content), len(content), content_type=file.content_type
    )
    
    db = SessionLocal()
    new_user = User(name=name, email=email, photo_url=f"/{bucket_name}/{file_name}")
    db.add(new_user)
    db.commit()
    db.close()
    return {"message": "Data berhasil disimpan"}

@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@app.put("/users/{user_id}")
async def update_user(user_id: int, name: str = Form(...), email: str = Form(...), file: UploadFile = File(None)):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    user.name = name
    user.email = email

    if file:
        # Hapus foto lama di MinIO [cite: 28]
        old_file = user.photo_url.split("/")[-1]
        try:
            minio_client.remove_object(bucket_name, old_file)
        except:
            pass
        
        # Upload foto baru
        content = await file.read()
        file_name = f"{email}_{file.filename}".replace(" ", "_")
        minio_client.put_object(
            bucket_name, file_name, io.BytesIO(content), len(content), content_type=file.content_type
        )
        user.photo_url = f"/{bucket_name}/{file_name}"

    db.commit()
    db.close()
    return {"message": "Data diperbarui"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # Hapus file dari MinIO [cite: 28]
        file_name = user.photo_url.split("/")[-1]
        try:
            minio_client.remove_object(bucket_name, file_name)
        except:
            pass
        db.delete(user)
        db.commit()
        db.close()
        return {"message": "Data dihapus"}
    db.close()
    raise HTTPException(status_code=404, detail="Gagal hapus")
