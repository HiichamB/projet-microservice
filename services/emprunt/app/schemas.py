from datetime import date
from typing import Literal
from pydantic import BaseModel
class EmpruntCreate(BaseModel):
 personne_id: int
 livre_id: int
 dateEmprunt: date
 datePrevuRetour: date
 dateRetourReelle: date | None = None
 statut: Literal["en cours", "rendu", "retard"] = "en cours"

class EmpruntRead(EmpruntCreate):
 id: int
