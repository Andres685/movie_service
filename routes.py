from flask_cors import cross_origin
from flask import Blueprint, jsonify, request
import requests
from config import Config


routes = Blueprint('routes', __name__)

@routes.route('/api/listar/todo', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_movies_batch():
    """
    Obtiene información de múltiples películas por título
    """
    print("Raw data:", request.data)
    print("JSON:", request.get_json(force=True, silent=True))
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.get_json()
    titles = data.get('titles')
    
    if not titles or not isinstance(titles, list):
        return jsonify({'message': 'Se requiere una lista de títulos', 'movies': []}), 400
    
    omdb_key = Config.OMDB_API_KEY
    omdb_url = Config.OMDB_API_URL
    results = []
    
    for title in titles:
        try:
            response = requests.get(f"{omdb_url}?apikey={omdb_key}&t={title}")
            movie_data = response.json()
            
            if movie_data.get('Response') == 'True':
                results.append(movie_data)
        except Exception as e:
            print(f"Error al buscar la película '{title}': {str(e)}")
    
    return jsonify({'movies': results}), 200

@routes.route('/api/movie/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')  # Ej: /api/movie/search?query=batman
    
    if not query:
        return jsonify({"error": "Se requiere un término de búsqueda"}), 400
    
    omdb_key = Config.OMDB_API_KEY
    omdb_url = Config.OMDB_API_URL
    try:
        response = requests.get(
            f"{omdb_url}?apikey={omdb_key}&s={query}&type=movie"
        )
        data = response.json()
        
        if data.get('Response') == 'True':
            return jsonify(data['Search'])  # Devuelve resultados de búsqueda
        else:
            return jsonify({"error": "No se encontraron películas"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
