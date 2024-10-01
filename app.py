import openai
import os
from flask import Flask, request, jsonify
from chat import prompt_to_predict
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    birthday = data['birthday']
    year_to_check = int(data['yearToCheck'])

    # Extract year from birthday
    birth_year = int(birthday.split('-')[0])
    message = f"Năm {year_to_check} là năm tốt để xông đất không, nếu chủ nhà sinh năm {birth_year}?"
    response = prompt_to_predict(message)
    return jsonify({'message': response})


# DEFINE query string
# sex=1|2 (1: nam, 2: nữ)
# birthday=dd/mm/yyyy+h:m (duơng lịch)
#
# EXAMPLE: /export-tu-vi?fullname=PHAM+VAN+MINH&sex=1&year=2024&birthday=2/10/2024+0:0
@app.route('/export-tu-vi', methods=['GET'])
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
    
    # TODO write to file for test open in browser
    with open('./la-tu-vi/templates/la-tu-vi.html', 'w', encoding='utf-8') as f:
        f.write(soup_html)

    # TODO return html for client render
    os_path_html = os.path.abspath('./la-tu-vi/templates/la-tu-vi.html') # for test
    
    return jsonify({'message': 'success', 'os_path_html': os_path_html})


if __name__ == '__main__':
    app.run(debug=True)