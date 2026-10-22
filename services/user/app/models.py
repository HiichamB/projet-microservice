from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
 pass
class Personne(Base):
 __tablename__ = "personnes"
 id: Mapped[int] = mapped_column(primary_key=True)
 nom: Mapped[str] = mapped_column()
 prenom: Mapped[str] = mapped_column()
 age: Mapped[int] = mapped_column()
 email: Mapped[str]= mapped_column(unique=True)
 telephone: Mapped[str]= mapped_column()
 password: Mapped[str]= mapped_column()

