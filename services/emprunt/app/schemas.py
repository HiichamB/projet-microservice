from datetime import date
from typing import Literal
from pydantic import BaseModel, Field
class EmpruntCreate(BaseModel):
 personne_id: int
 livre_id: int
 dateEmprunt: date
 datePrevuRetour: date
 dateRetourReelle: date | None = None
 statut: Literal["en cours", "rendu", "retard"] = "en cours"
 email: str = Field(min_length=5, max_length=100)

class EmpruntRead(EmpruntCreate):
 id: int
