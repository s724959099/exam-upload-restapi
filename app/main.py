from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

import models
from config import upload_path, DEBUG
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, File, UploadFile
from uuid import uuid4
from models import get_session
from sqlmodel import Session, select
from fastapi.responses import Response
import pathlib

app = FastAPI(title='Exam Upload RestAPI', description='For Quality Agriculture Exam', version='0.1.0')
origins = [
    '*',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
if not os.path.exists(upload_path):
    os.mkdir(upload_path)
app.mount('/uploads', StaticFiles(directory=upload_path), name='uploads')


@app.post('/file/')
def post_file(
        session: Session = Depends(get_session),
        file: UploadFile = File(...),
):
    filename, ext = file.filename.rsplit('.', 1)
    new_file_name = f'{str(uuid4())}.{ext}'
    file_path = os.path.join(upload_path, new_file_name)
    with open(file_path, 'wb') as f:
        f.write(file.file.read())

    file_orm = models.File(
        name=file.filename,
        file_path=file_path,
        content_type=file.content_type,
    )
    session.add(file_orm)
    session.commit()
    session.refresh(file_orm)
    return file_orm


@app.get('/file/{_id}')
def get_file_by_id(
        _id: int,
        session: Session = Depends(get_session),
):
    file_orm = session.exec(select(models.File).filter_by(id=_id)).first()
    if not file_orm:
        return Response(content='Not Found', status_code=404)
    p = pathlib.Path(file_orm.file_path)
    return Response(content=p.read_bytes(), media_type=file_orm.content_type)


if __name__ == '__main__':
    if DEBUG:
        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=5000,
            log_level='info',
            reload=True,
            workers=1,
            debug=True
        )
