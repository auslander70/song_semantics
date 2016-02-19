import os.path
from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from tuneful import app
from .database import Base, engine

class Song(Base):
  __tablename__ = 'songs'
  id = Column(Integer, primary_key=True)
  title = Column(String(256))
  artist = Column(String(256))
  def as_dictionary(self):
    return {
      'id': self.id,
      'title': self.title,
      'artist': self.artist
    }
  

class Chart(Base):
  __tablename__ = 'charts'
  id = Column(Integer, primary_key=True)
  date = Column(Date)
  def as_dictionary(self):
    return {
      'id': self.id, 
      'date': self.date
    }
    

class ChartSongs(Base):
  __tablename__ = 'chartsongs'
  id = Column(Integer, primary_key=True)
  rank = Column(Integer)
  def as_dictionary(self):
    return {
      'id': self.id,
      'rank': self.ranks
    }
    
    