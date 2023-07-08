from datetime import datetime
from fastapi.responses import FileResponse
from ..utils.types import File
import bcrypt
from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException,  Form
from ..utils import fs
from ..utils.types import Result
router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)
ERRORS = {
    "not_found": HTTPException(status_code=404, detail="File not found"),
    "invalid_cred":HTTPException(status_code=401, detail="Invliad Password"),
    "cred_requierd": HTTPException(status_code=401, detail="Password required")
}

async def get_meta(id: str) -> Result[File,None]:
    rawMeta = await fs.get_file(id + ".meta")
    if rawMeta.is_err():
        return Result.err()
    meta = File.parse_raw(rawMeta.unwrap())
    return Result.ok(meta)


async def verify_password(saved_password: str, password: str)-> Result[None,None]:
    if bcrypt.checkpw(password.encode(), saved_password.encode()) is False:
        return Result.err()
    return Result.ok()

async def verify_file(file:File) -> Result[None,None]:

    if file.expires < int(datetime.now().timestamp()):
        return Result.err()

    return Result.ok()

async def handle_download(id: str, password: Optional[str] = None):
    meta = await get_meta(id)
    meta = meta.ok_or_raise(ERRORS["not_found"])
    if meta.password is not None:
        if password is None:
            raise ERRORS["cred_requierd"]
        (await verify_password(meta.password, password)).ok_else_raise(ERRORS["invalid_cred"])
        
    (await verify_file(meta)).ok_else_raise(ERRORS["not_found"])
    filePath = await fs.file_path(id)
    filePath.ok_else_raise(ERRORS["not_found"])
    
    return FileResponse(filePath.unwrap(), filename=meta.name)


@router.get("/download/{id}")
async def upload(
        id: Annotated[str, Form],
        password: Optional[Annotated[str, Form]] = None
):
    return await handle_download(id, password)
