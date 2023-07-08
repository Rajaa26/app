from datetime import datetime

from ..utils.types import File
from ..constants import VAULT_DIR
from os import listdir, path, mkdir, remove
import aiofiles
from .types import Result


async def save_file(file: bytes, filename: str) -> Result[str, Exception]:
    if not path.exists(VAULT_DIR):
        mkdir(VAULT_DIR)

    if path.exists(path.join(VAULT_DIR, filename)):
        return Result.err("File already exists")
    try:
        async with aiofiles.open(path.join(VAULT_DIR, filename), "wb") as f:
            await f.write(file)
    except Exception as e:
        return Result.err(e)
    return Result.ok(filename)


def delete_file(filename: str) -> Result[str, Exception]:
    try:
        remove(path.join(VAULT_DIR, filename))
    except Exception as e:
        return Result.err(e)
    return Result.ok(filename)


async def get_file(filename: str) -> Result[bytes, Exception]:
    try:
        file = await aiofiles.open(path.join(VAULT_DIR, filename), "rb")
        content = await file.read()
        file.close()
        return Result.ok(content)
    except Exception as e:
        return Result.err(e)


async def file_path(filename: str) -> Result[str, Exception]:
    pat = path.exists(path.join(VAULT_DIR, filename))
    if pat is False:
        return Result.err("File does not exist")
    return Result.ok(path.join(VAULT_DIR, filename))


def delete_expired_files():
    filesMeta = listdir(VAULT_DIR)
    files = [file for file in filesMeta if file.endswith(".meta")]
    for file in files:
        try:
            with open(path.join(VAULT_DIR, file), "r") as f:
                data = File.parse_raw(f.read())
                f.close()
                expires = int(data.expires)
                if expires < int(datetime.now().timestamp()):
                    remove(path.join(VAULT_DIR, file))
                    remove(path.join(VAULT_DIR, file.replace(".meta", "")))
        except Exception as e:
            print("Error deleting file: ", e)
