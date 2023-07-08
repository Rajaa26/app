from datetime import datetime, timedelta
import bcrypt
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Form, HTTPException, UploadFile
from pydantic import BaseModel, validator

from .. import constants
from ..utils.types import File,Result
from ..utils import fs

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


class FileUploadRequest(BaseModel):
    password: Optional[str] = None
    expires: Optional[float] = None
    filename: Optional[str] = None

    @validator("expires")
    def expires_length(cls, v):
        if v is not None and v > constants.MAX_FILE_DURATION:
            raise ValueError(f"File duration must be less than {constants.MAX_FILE_DURATION} secounds")
        return int(v)

    @validator("expires", pre=True)
    def default_expires(cls, v):
        if v is None:
            return constants.DEFAULT_FILE_DURATION
        if str(v).isnumeric() is False:
            raise ValueError(f"Invlaid input type: Expected: Numeric")
        return v


class FileUploadResponse(BaseModel):
    id: str
    expires: int


async def create_meta_file(id: str, data: FileUploadRequest):
    if data.password is not None:
        data.password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())

    fileData = File(
        id=id,
        name=data.filename,
        expires=data.expires,
        password=data.password
    )
    return await fs.save_file(fileData.json().encode(), id + ".meta")


async def create_file(id: str, data: UploadFile):
    return await fs.save_file(data.file.read(), id)


async def generate_file_id() -> Result[str, Exception]:
    id = str(uuid4())
    path = await fs.file_path(id)
    if path.is_ok() is False:
        id = str(uuid4())  # try again

    return Result.ok(id)


async def handle_upload(file: UploadFile, data: FileUploadRequest):
    id = (await generate_file_id()).unwrap()

    if data.expires is not None:
        data.expires = (datetime.now() + timedelta(seconds=data.expires)).timestamp()

    meta = await create_meta_file(id, data)
    meta.ok_else_raise(HTTPException(status_code=500, detail=str(meta.error)))
    
    file_saved = await create_file(id, file)
    file_saved.ok_else_raise(HTTPException(status_code=500, detail=str(file_saved.error)))
        

    return FileUploadResponse(id=id, expires=data.expires)


@router.post("/upload", response_model=FileUploadResponse)
async def upload(
    file: UploadFile,
    password: Optional[str] = Form(None),
    expires: Optional[int] = Form(None)
):
    try:
        data = FileUploadRequest(
            password=password, expires=expires, filename=file.filename
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return await handle_upload(file, data)
