from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
 pass
class Emprunt(Base):
 __tablename__ = "emprunts"
 id: Mapped[int] = mapped_column(primary_key=True)
 # identifiants dans les services user et livre : pas de ForeignKey, ces tables sont dans d'autres bases
 personne_id: Mapped[int] = mapped_column()
 livre_id: Mapped[int] = mapped_column()
 dateEmprunt: Mapped[date] = mapped_column()
 datePrevuRetour: Mapped[date] = mapped_column()
 dateRetourReelle: Mapped[date | None] = mapped_column()  # vide tant que le livre n'est pas rendu
 statut: Mapped[str] = mapped_column(default="en cours")  # "en cours", "rendu" ou "retard"
