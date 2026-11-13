from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    email: str

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True