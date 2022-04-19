from typing import Optional
from pydantic import BaseModel
from fastapi import status, HTTPException

class AuthRequest(BaseModel):
    passphrase: Optional[str] = None
