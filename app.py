import os
from flask import Flask, request, jsonify
from chat import prompt_to_predict, get_chat_history, check_database_integrity, recreate_database
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from models import Request, Zodiac, Star, CanChi, MasterData, User, Session as DBSession
from contextlib import contextmanager

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

cors = CORS()

app = Flask(__name__)
cors.init_app(app)

@app.route('/api/reply', methods=['POST'])
def reply():
    params = request.get_json()
    print('reply:data:', params)
    message = params['message']
    user_uuid = params.get('uuid', 'default_user')

    try:
        response = prompt_to_predict(message, user_uuid)
        
        # Log interaction
        with get_db_session() as db_session:
            new_request = Request(content=f"User: {message}\nBot: {response}", uuid=user_uuid)
            db_session.add(new_request)
            db_session.commit()
        
        return jsonify({
            'message': response,
            'status': 'success'
        })
    except Exception as e:
        print(f'Error in reply: {str(e)}')
        return jsonify({
            'message': 'Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.',
            'status': 'error'
        }), 500

@app.route('/api/chat-history', methods=['GET'])
def get_user_chat_history():
    """Get chat history for a specific user"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({
            'message': 'user_id is required',
            'status': 'error'
        }), 400

    try:
        # Check database integrity first
        if not check_database_integrity():
            print("Database integrity check failed, attempting to recreate...")
            recreate_database()
        
        history = get_chat_history(user_id, limit=100)
        
        # Convert to frontend format
        messages = []
        for h in reversed(history):  # Reverse to show oldest first
            messages.append({
                'type': 'bot' if h['role'] == 'assistant' else 'human',
                'content': h['message'],
                'stage': h.get('step', 'greeting')
            })
        
        return jsonify({
            'messages': messages,
            'status': 'success'
        })
    except Exception as e:
        print(f'Error fetching chat history: {str(e)}')
        # Try to recreate database if it's a corruption error
        if "malformed" in str(e).lower() or "corrupted" in str(e).lower():
            print("Database corruption detected, attempting to recreate...")
            try:
                recreate_database()
                return jsonify({
                    'message': 'Database đã được khôi phục, vui lòng thử lại',
                    'status': 'error'
                }), 500
            except Exception as recreate_error:
                print(f"Failed to recreate database: {recreate_error}")
        
        return jsonify({
            'message': 'Lỗi khi tải lịch sử chat',
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tu Vi Bot API'
    })



if __name__ == '__main__':
    app.run(debug=True)