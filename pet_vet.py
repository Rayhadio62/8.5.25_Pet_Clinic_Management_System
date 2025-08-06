from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker
from datetime import datetime, timezone

Base = declarative_base()

engine = create_engine('sqlite:///vet.db')

Session = sessionmaker(bind=engine)
session = Session()


class Pets(Base):
    __tablename__ = "pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("owners.id"))
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    species: Mapped[str] = mapped_column(String(10), nullable=False)
    breed: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    
    vets: Mapped[list['Vets']] = relationship('Vets', back_populates='pets')
    owner: Mapped['Owners'] = relationship('Owners', back_populates='pets')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='pet')
    

class Owners(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str] = mapped_column(String(12), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False)
       
    pets: Mapped[list['Pets']] = relationship('Pets', back_populates='owner')


class Vets(Base):
    __tablename__ = "vets"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"))
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    specialization: Mapped[str] = mapped_column(String(80), nullable=False)
    
    pets: Mapped[list['Pets']] = relationship('Pets', back_populates='vets')
    appointments: Mapped[list['Appointments']] = relationship('Appointments', back_populates='vet')
    
    
class Appointments(Base):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(Integer, ForeignKey("pets.id"))
    vet_id: Mapped[int] = mapped_column(Integer, ForeignKey("vets.id"))
    appointment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    notes: Mapped[str] =mapped_column(String(500))
    status: Mapped[str] =mapped_column(String(20))
    
    pet: Mapped['Pets'] = relationship('Pets', back_populates='appointments')
    vet: Mapped['Vets'] = relationship('Vets', back_populates='appointments')
    
owner_1 = Owners(first_name='Bill', last_name='Gates', phone='111-111-1111', email='bgates@email.com')
owner_2 = Owners(first_name='Jeff', last_name='Bezos', phone='222-222-2222', email='jbezos@email.com')
owner_3 = Owners(first_name='Tim', last_name='Cook', phone='333-333-3333', email='tcook@email.com')


session.add_all([owner_1, owner_2, owner_3]) 
session.commit()





    

        
    
    
Base.metadata.create_all(bind=engine)