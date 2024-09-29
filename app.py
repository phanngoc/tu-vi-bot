import openai
import os
from flask import Flask, request, jsonify
from chat import prompt_to_predict

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

if __name__ == '__main__':
    app.run(debug=True)