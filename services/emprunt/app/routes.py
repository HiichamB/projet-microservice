import httpx
import pybreaker
from fastapi import APIRouter, HTTPException
from app.schemas import EmpruntCreate, EmpruntRead
router = APIRouter(prefix="/emprunts", tags=["emprunts"])
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Emprunt
from app.clients.user import get_personne



@router.get("", response_model=list[EmpruntRead])
async def lister():
 async with SessionLocal() as session:
   result = await session.execute(select(Emprunt))
 return result.scalars().all()


@router.get("/{emprunt_id}", response_model=EmpruntRead)
async def consulter(emprunt_id: int):
    async with SessionLocal() as session:
        emprunt = await session.get(Emprunt, emprunt_id)
    if emprunt is None:
        raise HTTPException(status_code=404, detail="Emprunt introuvable")
    return emprunt


@router.post("", response_model=EmpruntRead, status_code=201)
async def creer(emprunt: EmpruntCreate):
    try:
        personne = await get_personne(emprunt.personne_id)
    except (httpx.HTTPError, pybreaker.CircuitBreakerError):
        raise HTTPException(503, "service user momentanément indisponible")
    if personne is None:
        raise HTTPException(
            status_code=422,
            detail=f"La personne {emprunt.personne_id} n'existe pas",
        )
    async with SessionLocal() as session:
        nouveau = Emprunt(**emprunt.model_dump())
        session.add(nouveau)
        await session.commit()
        await session.refresh(nouveau)
    return nouveau


@router.put("/{emprunt_id}", response_model=EmpruntRead)
async def modifier(emprunt_id: int, emprunt: EmpruntCreate):
    async with SessionLocal() as session:
        modifie = await session.get(Emprunt, emprunt_id)
        if modifie is None:
            raise HTTPException(status_code=404, detail="Emprunt introuvable")
        for champ, valeur in emprunt.model_dump().items():
            setattr(modifie, champ, valeur)
        await session.commit()
        await session.refresh(modifie)
    return modifie

@router.delete("/{emprunt_id}", status_code=204)
async def supprimer(emprunt_id: int):
    async with SessionLocal() as session:
        emprunt = await session.get(Emprunt, emprunt_id)
        if emprunt is None:
            raise HTTPException(status_code=404, detail="Emprunt introuvable")
        await session.delete(emprunt)
        await session.commit()
