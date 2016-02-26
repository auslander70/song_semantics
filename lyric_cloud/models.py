import os.path
from flask import url_for
from sqlalchemy import Column, Date, ForeignKey, Integer, Sequence, String, Table, Text
from sqlalchemy.orm import relationship
from lyric_cloud import app
from .database import Base, engine

class Song(Base):
  __tablename__ = 'song'
  id = Column(Integer, primary_key=True)
  title = Column(String(256))
  artist = Column(String(256))
  lyrics = relationship('Lyrics', uselist=False, backref='song')
  charts = relationship('ChartSongs', backref='song')
  def as_dictionary(self):
    return {
      'id': self.id,
      'title': self.title,
      'artist': self.artist
    }
  

class Chart(Base):
  __tablename__ = 'chart'
  id = Column(Integer, primary_key=True)
  date = Column(Date)
  songs = relationship('ChartSongs', backref='chart')
  def as_dictionary(self):
    return {
      'id': self.id, 
      'date': self.date
    }
    

class ChartSongs(Base):
  __tablename__ = 'chartsongs'
  id = Column(Integer, primary_key=True)
  rank = Column(Integer)
  song_id = Column(Integer, ForeignKey('song.id'), nullable=False)
  chart_id = Column(Integer, ForeignKey('chart.id'), nullable=False)
  def as_dictionary(self):
    return {
      'id': self.id,
      'rank': self.ranks
    }
    
class Lyrics(Base):
  __tablename__ = 'lyrics'
  id = Column(Integer, primary_key=True)
  lyrics = Column(Text)
  song_id = Column(Integer, ForeignKey('song.id'), nullable=False)
  def as_dictionary(self):
    return {
    'id': self.id,
    'lyrics': self.lyrics
    }
  
Base.metadata.create_all(engine)