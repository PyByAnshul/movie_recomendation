from flask import Flask, render_template, request, jsonify
import requests
import data as dt
from models import db
from database_service import DatabaseService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()






def fetch_overview(movie_id):
    return DatabaseService.get_movie_overview(movie_id)

def get_poster_url(movie_id):
    """Return the poster URL template for frontend to fetch"""
    return f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a27a49bf043d4a93c59dccc8ffde1312&language=en-US"

def recommend(movie):
    try:
        # Get movie index by title
        movie_index = dt.get_movie_index_by_title(movie)
        if movie_index is None:
            print(f"Movie '{movie}' not found")
            return []
        
        # Get similarity matrix
        similarity = dt.similar()
        
        if similarity.size == 0 or movie_index >= len(similarity):
            print(f"Invalid similarity matrix or movie index: {movie_index}")
            return []
        
        # Get similarity scores for the movie
        try:
            movie_similarities = similarity[movie_index]
            distances = sorted(list(enumerate(movie_similarities)), reverse=True, key=lambda x: x[1])
        except IndexError as e:
            print(f"Index error in similarity matrix: {e}")
            return []
        
        recommended_movie = []
        
        # Limit to available movies and ensure we don't exceed bounds
        max_recommendations = min(6, len(distances))
        
        for i in range(max_recommendations):
            if i < len(distances):
                movie_idx, score = distances[i]
                # Get movie by index
                movie_obj = dt.get_movie_by_index(movie_idx)
                if movie_obj:
                    movie_id = movie_obj.movie_id
                    movie_name = movie_obj.title
                    movies_overviews = fetch_overview(movie_id)
                    
                    # Return movie_id instead of poster URL for frontend to fetch
                    recommended_movie.append({
                        'title': movie_name,
                        'overview': movies_overviews,
                        'movie_id': movie_id
                    })
        
        return recommended_movie
    except Exception as e:
        print(f"Error in recommend function: {e}")
        return []

@app.route("/")
def home():
 
    return render_template("home.html")


@app.route('/gettext', methods=["POST"])
def gettext():
    try:
        movie = request.json['text_data']
        
        # Check if database has movies
        from models import Movie
        movie_count = Movie.query.count()
        
        if movie_count == 0:
            return jsonify([{
                'title': 'Database Empty',
                'overview': 'Please run the database migration first: py migrate_to_db.py',
                'movie_id': 0
            }])
        
        recommended_movie = recommend(movie.lower())
        
        if not recommended_movie:
            return jsonify([{
                'title': 'No Recommendations',
                'overview': f'No similar movies found for "{movie}"',
                'movie_id': 0
            }])
        
        return jsonify(recommended_movie)
    except Exception as e:
        print(f"Error in gettext: {e}")
        return jsonify([{
            'title': 'Error',
            'overview': 'An error occurred while getting recommendations',
            'movie_id': 0
        }])
    

@app.route('/update', methods=['POST'])
def update():
    try:
        update_name = request.json['user_input']
        update_name = update_name.lower()
        
        movies = DatabaseService.search_movies(update_name)
        return jsonify(movies)
    except Exception as e:
        print(f"Error in update function: {e}")
        return jsonify([])


@app.route('/movies_data',methods=['GET'])
def movies_data():
    try:
        # Check if database has movies
        from models import Movie
        movie_count = Movie.query.count()
        
        if movie_count == 0:
            return jsonify([{
                'title': 'Database Empty',
                'tags': 'Please run migration: py migrate_to_db.py',
                'movie_id': 0
            }])
        
        random_movies = DatabaseService.get_random_movies(12)
        
        if not random_movies:
            return jsonify([{
                'title': 'No Movies Found',
                'tags': 'Database appears to be empty',
                'movie_id': 0
            }])
        
        movie_list = []
        for movie in random_movies:
            movie_list.append({
                'title': movie.title,
                'tags': movie.tags or '',
                'movie_id': movie.movie_id
            })
        
        return jsonify(movie_list)
    except Exception as e:
        print(f"Error in movies_data function: {e}")
        return jsonify([{
            'title': 'Error',
            'tags': f'Database error: {str(e)}',
            'movie_id': 0
        }])

@app.route('/get_posters', methods=['POST'])
def get_posters():
    """Batch fetch poster URLs for multiple movies"""
    try:
        from poster_service import PosterService
        movie_ids = request.json.get('movie_ids', [])
        
        if not movie_ids:
            return jsonify({})
        
        posters = PosterService.get_multiple_posters(movie_ids)
        return jsonify(posters)
    except Exception as e:
        print(f"Error in get_posters function: {e}")
        return jsonify({})
    


#invalid url
@app.errorhandler(404)
def page_not_found(e):
    return  "404"

#internal server
@app.errorhandler(500)
def page_not_found(e):
    return "500"




if __name__ == "__main__":
    


    app.run(debug=False)
