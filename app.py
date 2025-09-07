import os
from flask import Flask, request, jsonify
from chat_refactored import prompt_to_predict, get_user_from_database, list_all_users
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
        # Import database manager from chat_refactored
        from chat_refactored import get_database_manager
        
        # Get database manager and fetch chat history
        db_manager = get_database_manager()
        history = db_manager.get_chat_history(user_id, limit=100)
        
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
        
        return jsonify({
            'message': 'Lỗi khi tải lịch sử chat',
            'status': 'error'
        }), 500

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users from database"""
    try:
        users = list_all_users()
        return jsonify({
            'users': users,
            'count': len(users),
            'status': 'success'
        })
    except Exception as e:
        print(f'Error fetching users: {str(e)}')
        return jsonify({
            'message': 'Lỗi khi tải danh sách users',
            'status': 'error'
        }), 500

@app.route('/api/users/<name>', methods=['GET'])
def get_user_by_name(name):
    """Get user by name"""
    try:
        user = get_user_from_database(name)
        if user:
            return jsonify({
                'user': user,
                'status': 'success'
            })
        else:
            return jsonify({
                'message': f'Không tìm thấy user với tên: {name}',
                'status': 'not_found'
            }), 404
    except Exception as e:
        print(f'Error fetching user {name}: {str(e)}')
        return jsonify({
            'message': 'Lỗi khi tải thông tin user',
            'status': 'error'
        }), 500

@app.route('/api/components', methods=['GET'])
def get_component_info():
    """Get information about current components"""
    try:
        from chat_refactored import get_component_info
        info = get_component_info()
        return jsonify({
            'components': info,
            'status': 'success'
        })
    except Exception as e:
        print(f'Error getting component info: {str(e)}')
        return jsonify({
            'message': 'Lỗi khi lấy thông tin components',
            'status': 'error'
        }), 500

@app.route('/api/test', methods=['POST'])
def test_components():
    """Test component functionality"""
    try:
        from chat_refactored import test_components
        success = test_components()
        return jsonify({
            'test_result': 'PASSED' if success else 'FAILED',
            'status': 'success' if success else 'error'
        })
    except Exception as e:
        print(f'Error testing components: {str(e)}')
        return jsonify({
            'message': f'Lỗi khi test components: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tu Vi Bot API (Refactored)',
        'version': '2.0.0'
    })



if __name__ == '__main__':
    app.run(debug=True)