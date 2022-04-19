from aiocache import Cache
from fastapi import status, HTTPException, APIRouter, WebSocket, WebSocketDisconnect
from api.clipboardrequest import ClipboardRequest
from api.authrequest import AuthRequest
from api.connectionmanager import ConnectionManager

cache = Cache(Cache.MEMORY)

router = APIRouter(prefix="/api")

clipboards_manager = ConnectionManager()
clipboard_managers = {}

@router.on_event("startup")
async def start():
    await cache.set("hostnames", ["Server Clipboard"])
    await cache.add("Server Clipboard", ClipboardRequest(contents="Initial Contents"))
    clipboard_managers["Server Clipboard"] = ConnectionManager()



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
        await clipboards_manager.broadcast(hostnames)

async def __removeHostname(hostname: str):
    hostnames = await cache.get("hostnames")
    if hostnames is None:
        raise HTTPException(404, "Clipboard does not exist")
    if hostname in hostnames:
        hostnames.remove(hostname)
        await clipboards_manager.broadcast(hostnames)
    else:
        raise HTTPException(404, "Clipboard does not exist")


@router.post('/kill_clipboard/{hostname}')
async def kill_clipboard(hostname: str, auth: AuthRequest):
    clipboard = await __getClipboard(hostname)
    if clipboard.isPassphraseCorrect(auth.passphrase):
        await __removeHostname(hostname)
        deleted = await cache.delete(hostname)        
        await clipboard_managers[hostname].disconnectAll()
        del clipboard_managers[hostname]
        return {
            "detail":
            "{deleted} clipboard{s} deleted.".format(
                deleted=deleted, s="s" if deleted > 1 else "")
        }


@router.post('/get_clipboard/{hostname}')
async def get_clipboard(hostname: str, auth: AuthRequest):
    clipboard = await __getClipboard(hostname)
    return clipboard.get_contents(auth.passphrase)


@router.get('/get_clipboards')
async def get_clipboards():
    hostnames = await cache.get("hostnames")
    if hostnames is not None:
        return hostnames
    else:
        raise HTTPException(404, "No clipboards found.")


@router.post('/set_clipboard/{hostname}')
async def set_clipboard(hostname: str, clip: ClipboardRequest):
    clipboard = await __getClipboard(hostname)
    clipboard.set_contents(clip.contents, clip.passphrase)
    await clipboard_managers[hostname].broadcast(clip.contents)
    return {
        "detail": "Set contents to {contents}".format(contents=clip.contents)
    }


@router.post('/create_clipboard/{hostname}',
             status_code=status.HTTP_201_CREATED)
async def create_clipboard(hostname: str, new_clip: ClipboardRequest):
    """
    Create a clipboard with the given hostname, contents and passphrase.
    """

    try:
        await cache.add(hostname, new_clip)
        await __addHostname(hostname)
        clipboard_managers[hostname] = ConnectionManager()
        return {
            "detail": "Created clipboard {hostname}.".format(hostname=hostname)
        }
    except ValueError:
        raise HTTPException(403, "Clipboard already exists.")


@router.websocket("/clipboards_websocket")
async def clipboards_websocket(websocket: WebSocket):
    await clipboards_manager.connect(websocket)
    hostnames = await cache.get("hostnames")
    await websocket.send_json(hostnames)
    await websocket.receive()


@router.websocket("/clipboard_websocket/{hostname}")
async def clipboard_websocket(hostname: str, websocket: WebSocket, passphrase: str = ""):
    await clipboard_managers[hostname].connect(websocket)
    clip = await cache.get(hostname)
    if clip.isPassphraseCorrect(passphrase):
        while True:
            await websocket.send_json(clip.get_contents(passphrase))
            data = await websocket.receive_text()
            await set_clipboard(hostname, ClipboardRequest(contents=data, passphrase=passphrase))
