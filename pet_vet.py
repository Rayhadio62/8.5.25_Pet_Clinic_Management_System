from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker
from datetime import datetime, timezone

Base = declarative_base()

engine = create_engine('sqlite:///vet.db')

Session = sessionmaker(bind=engine)
session = Session()


class Owners(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[int] = mapped_column(String(12), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False)
       
    vets: Mapped[list['Vets']] = relationship('Vets', back_populates='owner')
    pets: Mapped[list['Pets']] = relationship('Pets', secondary='vets', back_populates='owners')
    

class Pets(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    species: Mapped[str] = mapped_column(String(10), nullable=False)
    breed: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(String(3), nullable=False)
    
    vets: Mapped[list['Vets']] = relationship('Vets', back_populates='pet')
    owners: Mapped[list['Owners']] = relationship('Owners', secondary='vets', back_populates='pets')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', secondary='pet', back_populates='vets')


class Vets(Base):
    __tablename__ = "vets"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    specialization: Mapped[str] = mapped_column(String(80), nullable=False)
    
    pets: Mapped[list['Pets']] = relationship('Pets', back_populates='vet')
    owners: Mapped[list['Owners']] = relationship('Owners', secondary='vets', back_populates='owners')
    
class Apointments(Base): #Association Model
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"))
    vet_id: Mapped[int] = mapped_column(Integer, ForeignKey("vets.id"))
    appointment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    notes: Mapped[str] =mapped_column(String(500))
    status: Mapped[str] =mapped_column(String(20))
    
    pets: Mapped[list['Pets']] = relationship('Pets', back_populates='appointment')
    vets: Mapped[list['Vets']] = relationship('Vets', secondary='appointments', back_populates='pet') 





    

        
    
    
    Base.metadata.create_all(bind=engine)