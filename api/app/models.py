from pydantic import BaseModel

class ContainerBlueprint(BaseModel):
    user_id: str
    key: str
    max_timeout: int
    timeout: int

class UserInput(BaseModel):
    email: str
    password: str