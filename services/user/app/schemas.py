from pydantic import BaseModel, Field
class PersonneCreate(BaseModel):
 nom: str = Field(min_length=1, max_length=100)
 prenom: str = Field(min_length=1, max_length=100)
 age: int = Field(ge=0)
 email: str = Field(min_length=5, max_length=100)
 telephone: str = Field(min_length=10, max_length=15)
 password: str = Field(min_length=6, max_length=100)

class PersonneRead(PersonneCreate):
 id: int