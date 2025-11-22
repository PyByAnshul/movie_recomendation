import requests
from concurrent.futures import ThreadPoolExecutor
import asyncio

class PosterService:
    API_KEY = "a27a49bf043d4a93c59dccc8ffde1312"
    BASE_URL = "https://api.themoviedb.org/3/movie"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    @staticmethod
    def get_poster_url_sync(movie_id):
        """Get poster URL synchronously (for single requests)"""
        try:
            url = f"{PosterService.BASE_URL}/{movie_id}?api_key={PosterService.API_KEY}&language=en-US"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if 'poster_path' in data and data['poster_path']:
                return f"{PosterService.IMAGE_BASE_URL}{data['poster_path']}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"
        except:
            return "https://via.placeholder.com/500x750?text=Error"
    
    @staticmethod
    def get_multiple_posters(movie_ids):
        """Get multiple poster URLs using threading for better performance"""
        def fetch_single_poster(movie_id):
            return {
                'movie_id': movie_id,
                'poster_url': PosterService.get_poster_url_sync(movie_id)
            }
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(fetch_single_poster, movie_ids))
        
        return {result['movie_id']: result['poster_url'] for result in results}