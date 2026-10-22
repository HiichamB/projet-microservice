from fastapi import APIRouter, HTTPException
from app.schemas import PersonneCreate, PersonneRead
router = APIRouter(prefix="/personnes", tags=["personnes"])
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.db import SessionLocal
from app.models import Personne



@router.get("", response_model=list[PersonneRead])
async def lister():
 async with SessionLocal() as session:
   result = await session.execute(select(Personne))
 return result.scalars().all()


# @router.get("", response_model=list[PersonneRead])
# async def lister():
#     return list(_db.values())

@router.get("/{personne_id}", response_model=PersonneRead)
async def consulter(personne_id: int):
    async with SessionLocal() as session:
        personne = await session.get(Personne, personne_id)
    if personne is None:
        raise HTTPException(status_code=404, detail="Personne non existe")
    return personne

@router.get("/{personne_nom}", response_model=PersonneRead)
async def consulter_par_nom(personne_nom: str):
    async with SessionLocal() as session:
        result = await session.execute(select(Personne).where(Personne.nom == personne_nom))
        personne = result.scalar_one_or_none()
    if personne is None:
        raise HTTPException(status_code=404, detail="Personne non existe")
    return personne



@router.post("", response_model=PersonneRead, status_code=201)
async def creer(personne: PersonneCreate):
    async with SessionLocal() as session:
        nouveau = Personne(**personne.model_dump())
        session.add(nouveau)
        await session.commit()
        await session.refresh(nouveau)
    return nouveau



# @router.post("", response_model=PersonneRead, status_code=201)
# async def creer(personne: PersonneCreate):
#     global _next_id
#     nouveau = PersonneRead(id=_next_id, **personne.model_dump())
#     _db[_next_id] = nouveau
#     _next_id += 1
#     return nouveau

@router.put("/{personne_id}", response_model=PersonneRead)
async def modifier(personne_id: int, personne: PersonneCreate):
    async with SessionLocal() as session:
        modifie = await session.get(Personne, personne_id)
        if modifie is None:
            raise HTTPException(status_code=404, detail="Personne introuvable")
        for champ, valeur in personne.model_dump().items():
            setattr(modifie, champ, valeur)
        await session.commit()
        await session.refresh(modifie)
    return modifie

@router.delete("/{personne_id}", status_code=204)
async def supprimer(personne_id: int):
    async with SessionLocal() as session:
        personne = await session.get(Personne, personne_id)

        #  if personne is None:
        #             raise HTTPException(status_code=404, detail="Personne introuvable")
        await session.delete(personne)
        await session.commit()

