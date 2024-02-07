from pydantic import BaseModel, EmailStr
from pydantic import ValidationError

class CreateUserPayload(BaseModel):
    username: EmailStr
    first_name: str
    last_name: str
    password: str
    # class Config:
    #     extra = 'forbid'

class UpdateUserPayload(BaseModel):
    first_name: str
    last_name: str
    password: str
    class Config:
        extra = 'forbid'

#Fuction to validate the payload against given model
def is_valid_payload(payload, model):
    try:
        model(**payload)
        return True
    except ValidationError as e:
        print(e)    
        return False

