from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine('sqlite:///new.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

##FEITO UTILIZANDO SQLALCHEMY

Base = declarative_base()

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    value = Column(String)
    ong_id = Column(Integer, ForeignKey('ongs.id'))
    ong = relationship('Ong')

    def __repr__(self):
        return f'Incident(id={self.id}, title={self.title})'

class Ong(Base):
    __tablename__ = "ongs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    whatsapp = Column(String)
    location = Column(String)
    incidents = relationship(Incident, backref='ongs')

    def __repr__(self):
        return f'Ong(id={self.id}, name={self.name}, email={self.email}, incidents={self.incidents})'

Base.metadata.create_all(engine)

ong1 = Ong(name='ze', email='ze@gmail.com', whatsapp='1234', location='Brazil')
incident1 = Incident(title='atropelamento cachorro', description='atropelado', value='15', ong=ong1)
#ong2 = Ong(name='ong maria', email='maria@gmail.com', whatsapp='1234', location='Brazil')

session.add(ong1)
session.add(incident1)
#session.add_all([ong1, incident1])
#session.add(ong2)
session.commit()

#print(session.query(Ong).all())
print(session.query(Incident).filter(Ong.name=='ze').first())
