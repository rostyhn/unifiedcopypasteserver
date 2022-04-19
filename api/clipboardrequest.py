from typing import Optional
from pydantic import BaseModel
from fastapi import status, HTTPException

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
                raise HTTPException(status_code=403,
                                    detail="Invalid authentication.")

    def set_passphrase(self,
                       new_passphrase: str,
                       passphrase: str = None) -> status:
        if self.isPassphraseCorrect(passphrase):
            self.passphrase = new_passphrase
            return status.HTTP_200_OK

    def get_contents(self, passphrase: str = None) -> str:
        if self.isPassphraseCorrect(passphrase):
            return self.contents

    def set_contents(self, contents: str, passphrase: str = None) -> status:
        if self.isPassphraseCorrect(passphrase):
            self.contents = contents
