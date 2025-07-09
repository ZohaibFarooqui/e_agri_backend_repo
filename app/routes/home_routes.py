from flask import Blueprint, jsonify
from app.utils.decorators import token_required
import datetime

home_bp = Blueprint('home', __name__)

advisors = [
    {"id": "1", "text": "Use drip irrigation", "image_url": "https://example.com/images/advisor1.png"},
    {"id": "2", "text": "Apply compost", "image_url": "https://example.com/images/advisor2.png"}
]

news_items = [
    {"id": "1", "title": "Subsidy on Fertilizers", "content": "Govt announces subsidy",
     "image_url": "https://example.com/images/news1.jpg",
     "published_at": datetime.datetime(2025, 6, 30, 12, 0).isoformat() + 'Z'},
    {"id": "2", "title": "Rain Expected", "content": "Heavy rain in Punjab",
     "image_url": "https://example.com/images/news2.jpg",
     "published_at": datetime.datetime(2025, 6, 29, 10, 0).isoformat() + 'Z'}
]

@home_bp.route('/home', methods=['GET'])
@token_required
def get_home_data():
    return jsonify({"advisors": advisors, "newsItems": news_items})

@home_bp.route('/advisors', methods=['GET'])
@token_required
def get_advisors():
    return jsonify(advisors)

@home_bp.route('/news', methods=['GET'])
@token_required
def get_news():
    return jsonify(news_items)

@home_bp.route('/advisors/<advisor_id>/read', methods=['POST'])
@token_required
def mark_advisor_read(advisor_id):
    print(f"Advisor {advisor_id} marked as read")
    return '', 204

@home_bp.route('/news/<news_id>/read', methods=['POST'])
@token_required
def mark_news_read(news_id):
    print(f"News {news_id} marked as read")
    return '', 204
