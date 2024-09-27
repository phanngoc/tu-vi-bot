import openai
from flask import Flask, request, jsonify
from llama_index.core.node_parser import (
    SemanticDoubleMergingSplitterNodeParser,
    LanguageConfig,
)

from llama_index.core import SimpleDirectoryReader

app = Flask(__name__)

# Thêm API key của OpenAI
openai.api_key = 'YOUR_OPENAI_API_KEY'
# Load and parse spec.txt
def load_spec():
    good_years = []
    with open('spec.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() and 'Tốt' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    year = parts[1].split('-')[-1].strip()
                    good_years.append(int(year))
    return good_years

good_years = load_spec()

# Load documents and create splitter
documents = SimpleDirectoryReader(input_files=["pg_essay.txt"]).load_data()
config = LanguageConfig(language="english", spacy_model="en_core_web_md")
splitter = SemanticDoubleMergingSplitterNodeParser(
    language_config=config,
    initial_threshold=0.4,
    appending_threshold=0.5,
    merging_threshold=0.5,
    max_chunk_size=5000,
)
nodes = splitter.get_nodes_from_documents(documents)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    birthday = data['birthday']
    year_to_check = int(data['yearToCheck'])

    # Extract year from birthday
    birth_year = int(birthday.split('-')[0])

    if birth_year in good_years:
        message = f"Năm {birth_year} là năm tốt để xông đất."
        # Gọi OpenAI để tạo lời thoại
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Viết một lời thoại cho năm {birth_year} là năm tốt để xông đất.",
            max_tokens=50
        )
        message += "\n" + response.choices[0].text.strip()
    else:
        message = f"Năm {birth_year} không phải là năm tốt để xông đất."

    # Use Llama Index to generate additional horoscope prediction
    node_content = nodes[0].get_content()
    llama_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Dựa trên nội dung sau, hãy đưa ra dự đoán tử vi cho năm {year_to_check}:\n{node_content}",
        max_tokens=150
    )
    llama_prediction = llama_response.choices[0].text.strip()
    message += f"\nDự đoán tử vi từ Llama Index: {llama_prediction}"

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)