from database_service import DatabaseService

def similar():
    """Get similarity matrix from database"""
    return DatabaseService.get_similarity_matrix()

def get_movie_by_index(index):
    """Get movie by index"""
    try:
        movies = DatabaseService.get_all_movies()
        if not movies or not isinstance(index, int):
            return None
        
        if 0 <= index < len(movies):
            return movies[index]
        return None
    except Exception as e:
        print(f"Error getting movie by index: {e}")
        return None

def get_movie_index_by_title(title):
    """Get movie index by title"""
    try:
        movies = DatabaseService.get_all_movies()
        if not movies:
            return None
        
        for i, movie in enumerate(movies):
            if movie.title and movie.title.lower().strip() == title.lower().strip():
                return i
        return None
    except Exception as e:
        print(f"Error getting movie index: {e}")
        return None