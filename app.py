from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)
CORS(app)

# TMDB API配置（请替换为你自己的API Key）
TMDB_API_KEY = os.environ.get('TMDB_API_KEY', 'YOUR_TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# 电影类型映射
GENRE_MAP = {
    '动作': [28],
    '冒险': [12],
    '喜剧': [35],
    '犯罪': [80],
    '纪录片': [99],
    '剧情': [18],
    '家庭': [10751],
    '奇幻': [14],
    '历史': [36],
    '恐怖': [27],
    '音乐': [10402],
    '悬疑': [9648],
    '爱情': [10749],
    '科幻': [878],
    '惊悚': [53],
    '战争': [10752],
    '西部': [37]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/movies/hot', methods=['GET'])
def get_hot_movies():
    """获取热门电影"""
    try:
        # 从TMDB获取热门电影
        tmdb_movies = fetch_tmdb_popular()

        # 从豆瓣获取热门电影（模拟数据，因为豆瓣API需要授权）
        douban_movies = fetch_douban_hot()

        # 合并并排序
        all_movies = tmdb_movies + douban_movies
        all_movies.sort(key=lambda x: x['rating'], reverse=True)

        return jsonify({
            'success': True,
            'movies': all_movies[:20]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/movies/upcoming', methods=['GET'])
def get_upcoming_movies():
    """获取即将上映的电影"""
    try:
        url = f'{TMDB_BASE_URL}/movie/upcoming'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'zh-CN',
            'region': 'CN',
            'page': 1
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        movies = []
        for movie in data.get('results', [])[:15]:
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'rating': movie.get('vote_average', 0),
                'release_date': movie.get('release_date', ''),
                'overview': movie.get('overview', ''),
                'source': 'TMDB'
            })

        return jsonify({
            'success': True,
            'movies': movies
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/movies/recommend', methods=['POST'])
def recommend_movies():
    """根据类型偏好推荐电影"""
    try:
        data = request.json
        genres = data.get('genres', [])

        # 获取类型ID
        genre_ids = []
        for genre in genres:
            if genre in GENRE_MAP:
                genre_ids.extend(GENRE_MAP[genre])

        if not genre_ids:
            # 如果没有指定类型，返回高分电影
            return get_top_rated_movies()

        # 从TMDB获取推荐
        url = f'{TMDB_BASE_URL}/discover/movie'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'zh-CN',
            'sort_by': 'vote_average.desc',
            'with_genres': '|'.join(map(str, genre_ids)),
            'vote_count.gte': 100,
            'page': 1
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        movies = []
        for movie in data.get('results', [])[:15]:
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'rating': movie.get('vote_average', 0),
                'release_date': movie.get('release_date', ''),
                'overview': movie.get('overview', ''),
                'source': 'TMDB'
            })

        return jsonify({
            'success': True,
            'movies': movies
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/movies/daily', methods=['GET'])
def get_daily_recommendation():
    """每日推荐电影"""
    try:
        # 基于日期生成随机种子，确保同一天推荐相同
        today = datetime.now().strftime('%Y-%m-%d')
        random.seed(today)

        # 获取高分电影
        url = f'{TMDB_BASE_URL}/movie/top_rated'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'zh-CN',
            'page': random.randint(1, 5)
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        all_movies = data.get('results', [])
        # 随机选择3部电影作为今日推荐
        daily_movies = random.sample(all_movies, min(3, len(all_movies)))

        movies = []
        for movie in daily_movies:
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'rating': movie.get('vote_average', 0),
                'release_date': movie.get('release_date', ''),
                'overview': movie.get('overview', ''),
                'source': 'TMDB'
            })

        return jsonify({
            'success': True,
            'date': today,
            'movies': movies
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def fetch_tmdb_popular():
    """从TMDB获取热门电影"""
    movies = []
    try:
        url = f'{TMDB_BASE_URL}/movie/popular'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'zh-CN',
            'page': 1
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        for movie in data.get('results', [])[:10]:
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'rating': movie.get('vote_average', 0),
                'release_date': movie.get('release_date', ''),
                'overview': movie.get('overview', ''),
                'source': 'TMDB'
            })
    except Exception as e:
        print(f"TMDB获取失败: {e}")

    return movies

def fetch_douban_hot():
    """从豆瓣获取热门电影（模拟数据）"""
    # 注意：豆瓣API现在需要授权，这里提供模拟数据
    # 实际使用时建议申请豆瓣API key或使用其他方法
    movies = []

    # 这里可以添加爬虫逻辑，但要注意遵守网站robots.txt
    # 示例：返回空列表或使用备用数据源

    return movies

def get_top_rated_movies():
    """获取高分电影"""
    try:
        url = f'{TMDB_BASE_URL}/movie/top_rated'
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'zh-CN',
            'page': 1
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        movies = []
        for movie in data.get('results', [])[:15]:
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'rating': movie.get('vote_average', 0),
                'release_date': movie.get('release_date', ''),
                'overview': movie.get('overview', ''),
                'source': 'TMDB'
            })

        return jsonify({
            'success': True,
            'movies': movies
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
