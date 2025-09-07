import os
from flask import Flask, request, jsonify
from chat import prompt_to_predict
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from models import Request, Zodiac, Star, CanChi, MasterData, User, session

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
        response = prompt_to_predict(message)
        
        # Log interaction
        new_request = Request(content=f"User: {message}\nBot: {response}", uuid=user_uuid)
        session.add(new_request)
        session.commit()
        
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tu Vi Bot API'
    })



if __name__ == '__main__':
    app.run(debug=True)