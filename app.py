import os
from flask import Flask, request, jsonify
from chat import prompt_to_predict
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from flask_cors import CORS

cors = CORS()

Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Create an engine and a session
engine = create_engine('sqlite:///tu-vi.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
cors.init_app(app)

@app.route('/api/reply', methods=['POST'])
def reply():
    params = request.get_json()
    print('reply:data:', params)
    message = params['message']
    year_to_check = 2024
    
    response = prompt_to_predict(message)
    return jsonify({'message': response})

def parse_tu_vi(query):
    print('parse_tu_vi', query)
    
    response = requests.get('https://api.phuongdonghuyenbi.vn/api/GetHoroscope?' + query)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    #  remove logo from api
    for div in soup.find_all("div", {'class': 'advertising-text'}):
        div.decompose()
    
    for div in soup.find_all("div", {'class': 'mark-image'}):
        div.decompose()
    
    for div in soup.find_all("div", {'class': 'advisor-section'}):
        div.decompose()
        
    for div in soup.find_all("div", {'class': 'capture-button-container'}):
        div.decompose()
    
    for div in soup.find_all("form", {'class': 'hiddenForm'}):
        div.decompose()
        
    for div in soup.find_all("a", {'class': 'redirect-button'}):
        div.decompose()
    
    soup_htm = str(soup)
    soup_html = soup_htm.replace('/backend', '..')
    soup_html = soup_html.replace('background-image: url(/backend/assets/images/ly-so/bglasotuvi2-03.jpg)', '')

    user_id = 1  # Replace with actual user_id
    new_request = Request(user_id=user_id, content=soup_html)
    session.add(new_request)
    session.commit()
    
    return jsonify(new_request)


# DEFINE query string
# sex=1|2 (1: nam, 2: nữ)
# birthday=dd/mm/yyyy+h:m (duơng lịch)
#
# EXAMPLE: /export-tu-vi?fullname=PHAM+VAN+MINH&sex=1&year=2024&birthday=2/10/2024+0:0
@app.route('/api/export-tu-vi', methods=['GET'])
def export_tu_vi():
    query = request.query_string.decode('utf-8')
    print(query)
    
    response = requests.get('https://api.phuongdonghuyenbi.vn/api/GetHoroscope?' + query)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    #  remove logo from api
    for div in soup.find_all("div", {'class': 'advertising-text'}):
        div.decompose()
    
    for div in soup.find_all("div", {'class': 'mark-image'}):
        div.decompose()
    
    for div in soup.find_all("div", {'class': 'advisor-section'}):
        div.decompose()
        
    for div in soup.find_all("div", {'class': 'capture-button-container'}):
        div.decompose()
    
    for div in soup.find_all("form", {'class': 'hiddenForm'}):
        div.decompose()
        
    for div in soup.find_all("a", {'class': 'redirect-button'}):
        div.decompose()
    
    soup_htm = str(soup)
    soup_html = soup_htm.replace('/backend', '..')
    soup_html = soup_html.replace('background-image: url(/backend/assets/images/ly-so/bglasotuvi2-03.jpg)', '')

    user_id = 1  # Replace with actual user_id
    new_request = Request(user_id=user_id, content=soup_html)
    session.add(new_request)
    session.commit()

    # TODO write to file for test open in browser
    # with open('./la-tu-vi/templates/la-tu-vi.html', 'w', encoding='utf-8') as f:
    #     f.write(soup_html)

    # TODO return html for client render
    # os_path_html = os.path.abspath('./la-tu-vi/templates/la-tu-vi.html') # for test
    
    return jsonify({'message': 'success', 'request_id': new_request.id})


if __name__ == '__main__':
    app.run(debug=True)