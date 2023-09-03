from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

english_api_key = "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"
english_model_name = "davinci:ft-personal-2023-09-01-13-31-52"

korean_api_key = "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"
korean_model_name = "davinci:ft-personal-2023-09-02-15-55-41"

conversation_history = []

@app.route('/gpt', methods=['POST'])
def get_answer():
    data = request.get_json()
    prompt = data.get('prompt')
    language = data.get('language')

    if language == 'en':
        openai.api_key = english_api_key
        model_name = english_model_name
        tokens = 40
        
    elif language == 'ko':
        openai.api_key = korean_api_key
        model_name = korean_model_name
        tokens = 240
        
    else:
        return jsonify({"error": "Unsupported language"}), 400

    conversation_history.append(prompt)
    conversation = "\n".join(conversation_history)

    response = openai.Completion.create(
        engine=model_name,
        prompt=conversation,
        max_tokens=tokens,
        temperature=0.3,
        n=100
    )

    return jsonify({"answer": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
