from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Float

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False, index=True)
    tags = Column(Text, nullable=True)
    
    def __repr__(self):
        return f'<Movie {self.title}>'

class MovieList(db.Model):
    __tablename__ = 'movie_list'
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False, index=True)
    
    def __repr__(self):
        return f'<MovieList {self.title}>'

class MovieOverview(db.Model):
    __tablename__ = 'movie_overview'
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, unique=True, nullable=False, index=True)  # Changed from 'id' to 'movie_id'
    overview = Column(Text, nullable=True)
    
    def __repr__(self):
        return f'<MovieOverview {self.movie_id}>'

class MovieData(db.Model):
    __tablename__ = 'movie_data'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False, index=True)
    
    def __repr__(self):
        return f'<MovieData {self.title}>'

class SimilarityMatrix(db.Model):
    __tablename__ = 'similarity_matrix'
    
    id = Column(Integer, primary_key=True)
    movie_index = Column(Integer, nullable=False, index=True)
    similar_movie_index = Column(Integer, nullable=False, index=True)
    similarity_score = Column(Float, nullable=False)
    
    def __repr__(self):
        return f'<SimilarityMatrix {self.movie_index}-{self.similar_movie_index}>'