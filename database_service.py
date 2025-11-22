from models import db, Movie, MovieList, MovieOverview, MovieData, SimilarityMatrix
from flask import current_app
import numpy as np

class DatabaseService:
    
    @staticmethod
    def get_movie_overview(movie_id):
        """Get movie overview by movie_id"""
        try:
            overview = MovieOverview.query.filter_by(movie_id=movie_id).first()
            return overview.overview if overview and overview.overview else "nothing"
        except:
            return "nothing"
    
    @staticmethod
    def search_movies(query, limit=6):
        """Search movies by title"""
        try:
            movies = MovieData.query.filter(
                MovieData.title.ilike(f'{query}%')
            ).limit(limit).all()
            return [movie.title for movie in movies]
        except:
            return []
    
    @staticmethod
    def get_random_movies(count=12):
        """Get random movies"""
        try:
            import random
            movies = Movie.query.all()
            return random.sample(movies, min(count, len(movies)))
        except:
            return []
    
    @staticmethod
    def get_movie_by_title(title):
        """Get movie by title"""
        try:
            return Movie.query.filter(Movie.title.ilike(title)).first()
        except:
            return None
    
    @staticmethod
    def get_all_movies():
        """Get all movies"""
        try:
            movies = Movie.query.all()
            return movies if movies else []
        except Exception as e:
            print(f"Error getting movies: {e}")
            return []
    
    @staticmethod
    def get_similarity_matrix():
        """Get similarity matrix from database or calculate if not exists"""
        try:
            movies = Movie.query.all()
            movie_count = len(movies)
            
            if movie_count == 0:
                return np.array([[]])
            
            # Check if similarity matrix exists in database
            similarity_count = SimilarityMatrix.query.count()
            
            if similarity_count == 0:
                # Calculate similarity matrix on the fly
                print("Calculating similarity matrix on the fly...")
                from sklearn.feature_extraction.text import CountVectorizer
                from sklearn.metrics.pairwise import cosine_similarity
                
                movie_tags = [movie.tags or '' for movie in movies]
                cv = CountVectorizer(max_features=5000, stop_words='english')
                vector = cv.fit_transform(movie_tags).toarray()
                similarity_matrix = cosine_similarity(vector)
                return similarity_matrix
            
            # Initialize similarity matrix
            similarity_matrix = np.zeros((movie_count, movie_count))
            
            # Fill diagonal with 1.0 (self-similarity)
            np.fill_diagonal(similarity_matrix, 1.0)
            
            # Get similarity data from database
            similarities = SimilarityMatrix.query.all()
            
            for sim in similarities:
                if (isinstance(sim.movie_index, int) and isinstance(sim.similar_movie_index, int) and 
                    0 <= sim.movie_index < movie_count and 0 <= sim.similar_movie_index < movie_count):
                    similarity_matrix[sim.movie_index][sim.similar_movie_index] = float(sim.similarity_score)
                    # Make matrix symmetric
                    similarity_matrix[sim.similar_movie_index][sim.movie_index] = float(sim.similarity_score)
            
            return similarity_matrix
        except Exception as e:
            print(f"Error getting similarity matrix: {e}")
            # Fallback: return identity matrix
            movies = Movie.query.all()
            if len(movies) > 0:
                matrix = np.eye(len(movies))
                return matrix
            return np.array([[1.0]])