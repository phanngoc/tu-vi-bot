import openai

# Thêm API key của OpenAI
openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    birthday = data['birthday']
    year_to_check = int(data['year_to_check'])

    # Giả sử spec.txt chứa một danh sách các năm tốt
    if year_to_check in good_years:
        message = f"Năm {year_to_check} là năm tốt để xông đất."
        # Gọi OpenAI để tạo lời thoại
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Viết một lời thoại cho năm {year_to_check} là năm tốt để xông đất.",
            max_tokens=50
        )
        message += "\n" + response.choices[0].text.strip()
    else:
        message = f"Năm {year_to_check} không phải là năm tốt để xông đất."

    return jsonify({'message': message})