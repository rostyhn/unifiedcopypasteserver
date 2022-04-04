from aiocache import Cache
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel

#aiocache to store data
app = FastAPI()
cache = Cache(Cache.MEMORY)

class ClipboardRequest(BaseModel):
    contents: str
    passphrase: Optional[str] = None
                        
    def isPassphraseCorrect(self, passphrase: str = None) -> bool:
        if self.passphrase is None:
            return True
        else:
            if self.passphrase == passphrase:
                return True
            else:
                raise HTTPException(status_code=403, detail="Invalid authentication.")

    def set_passphrase(self, new_passphrase: str, passphrase: str = None) -> status:
        if self.isPassphraseCorrect(passphrase):
            self.passphrase = new_passphrase
            return status.HTTP_200_OK
            
    def get_contents(self, passphrase: str = None) -> str:
        if self.isPassphraseCorrect(passphrase):
            return self.contents

    def set_contents(self, contents: str, passphrase: str = None) -> status:
        if self.isPassphraseCorrect(passphrase):
            self.contents = contents

class AuthRequest(BaseModel):
    passphrase: Optional[str] = None
            
async def __getClipboard(hostname: str) -> ClipboardRequest:
    clipboard = await cache.get(hostname)
    if clipboard is not None:
        return clipboard
    else:
        raise HTTPException(404, "Clipboard not found.")

async def __addHostname(hostname: str):
    hostnames = await cache.get("hostnames")
    if hostnames is None:
        hostnames = []
    if hostname in hostnames:
        raise HTTPException(403, "Clipboard already exists.")
    else:
        hostnames.append(hostname)
        await cache.set("hostnames", hostnames)


@app.post('/kill_clipboard/{hostname}')
async def kill_clipboard(hostname: str, auth: AuthRequest):
    clipboard = await cache.get(hostname)
    if clipboard.isPassphraseCorrect(auth.passphrase):
        deleted = await cache.delete(hostname)
        return {"detail": "{deleted} clipboard{s} deleted.".format(deleted=deleted,s="s" if deleted > 1 else "")}

    
@app.post('/get_clipboard/{hostname}')
async def get_clipboard(hostname: str, auth: AuthRequest):
    clipboard = await __getClipboard(hostname)
    return clipboard.get_contents(auth.passphrase)


@app.get('/get_clipboards')
async def get_clipboards():
    hostnames = await cache.get("hostnames")
    return hostnames


@app.post('/set_clipboard/{hostname}')
async def set_clipboard(hostname: str, clip: ClipboardRequest):
    clipboard = await __getClipboard(hostname)
    clipboard.set_contents(clip.contents, clip.passphrase)
    return {"detail": "Set contents to {contents}".format(contents=clip.contents)}

@app.post('/create_clipboard/{hostname}', status_code=status.HTTP_201_CREATED)
async def create_clipboard(hostname: str, new_clip: ClipboardRequest):
    """
    Creates a clipboard with the given hostname, contents and passphrase.
    """
    
    try:
        await cache.add(hostname, new_clip)
        await __addHostname(hostname)
        return {"detail": "Created clipboard {hostname}.".format(hostname=hostname)}
    except ValueError:
        raise HTTPException(403, "Clipboard already exists.")
