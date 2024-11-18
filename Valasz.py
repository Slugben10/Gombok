from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# OpenAI API key konfigurálása
openai.api_key = ""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    step = request.json.get('step')

    if step == 1:
        if user_input == 'Chatbot':
            return jsonify({
                'response': "Szeretne időpontot foglalni, vagy egy egészségügyi problémáról beszélni?",
                'options': ['Időpont', 'Egészségügyi probléma'],
                'step': 2
            })
        elif user_input == 'Ember':
            return jsonify({'redirect': '/human-support'})
        elif user_input == 'Kutya':
            return jsonify({'redirect': '/dog-support'})
        else:
            return jsonify({
                'response': "Kérjük, válasszon a következők közül: Chatbot, Ember, Kutya.",
                'options': ['Chatbot', 'Ember', 'Kutya'],
                'step': 1
            })

    elif step == 2:
        if user_input == 'Időpont':
            return jsonify({'redirect': '/appointment'})
        elif user_input == 'Egészségügyi probléma':
            return jsonify({
                'response': "Milyen panaszról szeretne beszélni?",
                'options': ['Tüdő', 'Bőr', 'Szív'],
                'step': 3
            })
        else:
            return jsonify({
                'response': "Kérjük, válasszon: Időpont vagy Egészségügyi probléma.",
                'options': ['Időpont', 'Egészségügyi probléma'],
                'step': 2
            })

    elif step == 3:
        if user_input in ['Tüdő', 'Bőr', 'Szív']:
            return jsonify({
                'response': f"A(z) {user_input} problémájával kapcsolatos kérdéseit most felteheti a chatbotnak.",
                'options': [],
                'step': 4
            })
        else:
            return jsonify({
                'response': "Kérjük, válasszon a következők közül: Tüdő, Bőr, Szív.",
                'options': ['Tüdő', 'Bőr', 'Szív'],
                'step': 3
            })

    elif step == 4:
        # OpenAI API hívás
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant chatbot."},
                    {"role": "user", "content": user_input}
                ]
            )
            bot_response = response['choices'][0]['message']['content']
            return jsonify({
                'response': bot_response,
                'options': [],
                'step': 4
            })
        except Exception as e:
            return jsonify({'response': f"Hiba történt: {str(e)}", 'options': [], 'step': 4})
    else:
        return jsonify({
            'response': "Ismeretlen lépés. Kérjük, kezdje újra.",
            'options': ['Chatbot', 'Ember', 'Kutya'],
            'step': 1
        })

if __name__ == "__main__":
    app.run(debug=True)
