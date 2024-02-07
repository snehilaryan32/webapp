from pydantic import BaseModel
from pydantic import ValidationError

class CreateUserPayload(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

class UpdateUserPayload(BaseModel):
    first_name: str
    last_name: str
    password: str

#Fuction to validate the payload against given model
def is_valid_payload(payload, model):
    try:
        model(**payload)
        return True
    except ValidationError as e:
        print(e)    
        return False

