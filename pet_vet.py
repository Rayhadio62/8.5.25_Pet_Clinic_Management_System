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
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("owners.id"), nullable=True)
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
    email: Mapped[str] = mapped_column(String(360), unique=True)
    
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
    
    
# owner_1 = Owners(first_name='Bill', last_name='Gates', phone='111-111-1111', email='bgates@email.com')
# owner_2 = Owners(first_name='Jeff', last_name='Bezos', phone='222-222-2222', email='jbezos@email.com')
# owner_3 = Owners(first_name='Tim', last_name='Cook', phone='333-333-3333', email='tcook@email.com')

# pet_1 = Pets(owner_id='1', name='Snoopy', species='dog', breed='beagle', age=74)
# pet_2 = Pets(owner_id='2', name='Sandy', species='dog', breed='Heinz57', age=15)
# pet_3 = Pets(owner_id='3', name='Tom', species='cat', breed='domestic shorthair', age=84)
# pet_4 = Pets(owner_id='1', name='Woody', species='bird', breed='woodpecker', age=85)
# pet_5 = Pets(owner_id='2', name='Garfield', species='cat', breed='orange tabby', age='47')
# pet_6 = Pets(owner_id='3', name='Charlotte', species='araneus cavaticus', breed='barn_spider', age='73')

vet_1 = Vets(pet_id='2', first_name='Dr. Captain', last_name='Kangaroo', specialization='stuffed animals', email='capkangaroo@email.com')
vet_2 = Vets(pet_id='1', first_name='Dr. Jan', last_name='Pol', specialization='large farm animals', email='jpol@email.com')

# session.add_all([owner_1, owner_2, owner_3])

# session.add_all([pet_1, pet_2, pet_3, pet_4, pet_5, pet_6])

session.add_all([vet_1, vet_2]) 

session.commit()





    

        
    
    
Base.metadata.create_all(bind=engine)