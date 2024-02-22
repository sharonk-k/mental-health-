from flask import Flask, request
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'koech'

facebook_bearer_token = 'EAAI7KQfphY0BOZC4T0cy9eyv2Wa1ADCO5UX2gqypsNJYzumX9yQEreLVqxCCMhWBF2u3u80EbBDBz4flXZA1xWyIZBBcZBJPZB1BtF9y9dJdOfoOA36YzCwkRDBon9UqZBqB4ZCEW3ytpLtLADdRyGaEJuNlNQNBs0ZBrZBc8hZAQkrFnsDWtCZBvrua0oNzFBYLKCMtTzNwmHl8gHjzXhG2KioEFi3QNO9DGpa5ngZD'

data = {
    "intents": [
        {"tag": "definition",
         "patterns": ["What does it mean to have a mental illness?", "What is mental health illness", "Describe mental health illness"],
         "responses": ["Mental illnesses are health conditions that disrupt a person's thoughts, emotions, relationships, and daily functioning."],
         "context": [""]
         },

        {"tag": "affects_whom",
         "patterns": ["Who does mental illness affect?", "Who is affected by mental illness"],
         "responses": ["It is estimated that mental illness affects 1 in 5 adults in America, and that 1 in 24 adults have a serious mental illness."],
         "context": [""]
         },
        {"tag": "what_causes",
         "patterns": ["What causes mental illness?", "What leads to mental illness?", "How does one get mentally ill?"],
         "responses": ["Symptoms of mental health disorders vary depending on the type and severity of the condition."],
         "context": [""]
         },

        {"tag": "recover",
         "patterns": ["Can people with mental illness recover?", "Is it possible to recover from mental illness"],
         "responses": ["When healing from mental illness, early identification and treatment are of vital importance. Based on the nature of the illness, there are a range of effective treatments available. For any type of treatment, it is essential that the person affected is proactive and fully engaged in their own recovery process. Many people with mental illnesses who are diagnosed and treated respond well, although some might experience a return of symptoms. Even in such cases, with careful monitoring and management of the disorder, it is still quite possible to live a fulfilled and productive life."],
         "context": [""]
         },
        {"tag": "steps",
         "patterns": ["I know someone who appears to have such symptoms?", "What are the steps to be followed in case of symptoms"],
         "responses": ["Although this website cannot substitute for professional advice, we encourage those with symptoms to talk to their friends and family members and seek the counsel of a mental health professional. The sooner the mental health condition is identified and treated, the sooner they can get on the path to recovery. If you know someone who is having problems, don't assume that the issue will resolve itself. Let them know that you care about them, and that there are treatment options available that will help them heal. Speak with a mental health professional or counselor if you think your friend or family member is experiencing the symptoms of a mental health condition. If the affected loved one knows that you support them, they will be more likely to seek out help."],
         "context": [""]
         },
        {"tag": "find_help",
         "patterns": ["How to find mental health professional for myself", "How to find mental health professional?"],
         "responses": ["Feeling comfortable with the professional you or your child is working with is critical to the success of the treatment. Finding the professional who best fits your needs may require research. Start by searching for providers in your area."],
         "context": [""]
         },
        {"tag": "treatment_options",
         "patterns": ["What treatment options are available?", "How can one recover?"],
         "responses": ["Just as there are different types of medications for physical illness, different treatment options are available for individuals with mental illness. Treatment works differently for different people. It is important to find what works best for you or your child."],
         "context": [""]
         },
        {"tag": "treatment_tips",
         "patterns": ["How to become involved in treatment?", "What should I keep in mind if I begin treatment?"],
         "responses": ["Since beginning treatment is a big step for individuals and families, it can be very overwhelming."],
         "context": [""]
         },
        {"tag": "professional_types",
         "patterns": ["What is the difference between mental health professionals?", "What are the different types of mental health professionals present?"],
         "responses": ["There are many types of mental health professionals. The variety of providers and their services may be confusing. Each has various levels of education, training, and may have different areas of expertise. Finding the professional who best fits your needs may require some research."],
         "context": [""]
         },
        {"tag": "right_professional",
         "patterns": ["How can I find a mental health professional right myself?", "How to find the right mental health professional?"],
         "responses": ["Feeling comfortable with the professional you or your child is working with is critical to the success of your treatment. Finding the professional who best fits your needs may require some research."],
         "context": [""]
         }
    ]
}


def send_msg(msg, wa_id):
    headers = {
        'Authorization': f'Bearer {facebook_bearer_token}',
    }
    json_data = {
        'messaging_product': 'whatsapp',
        'to': wa_id,
        'type': 'text',
        "text": {
            "body": msg
        }
    }
    response = requests.post('https://graph.facebook.com/v13.0/PhoneID/messages', headers=headers,
                             json=json_data)
    print(response.text)


def get_response(user_query):
    for intent in data['intents']:
        for pattern in intent['patterns']:
            if user_query.lower() in pattern.lower():
                return intent['responses'][0]
    return "I'm sorry, I couldn't understand that."


@app.route('/receive_msg', methods=['POST', 'GET'])
def webhook():
    try:
        if request.method == 'GET':
            if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
                if not request.args.get("hub.verify_token") == "koechbot":
                    return "Verification token mismatch", 403
                return request.args['hub.challenge'], 200

        res = request.get_json()

        if 'entry' in res and 'changes' in res['entry'][0] and 'value' in res['entry'][0]['changes'][0] and 'messages' in res['entry'][0]['changes'][0]['value']:
            user_query = res['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

            # Check if 'contacts' key is present
            if 'contacts' in res['entry'][0]['changes'][0]['value']['messages'][0]:
                wa_id = res['entry'][0]['changes'][0]['value']['messages'][0]['contacts'][0]['wa_id']
            else:
                wa_id = res['entry'][0]['changes'][0]['value']['messages'][0]['from']

            if user_query.lower() == 'hi':
                send_msg("Hello, how can I assist you today?", wa_id)
            else:
                response = get_response(user_query)
                send_msg(response, wa_id)

    except Exception as e:
        print(f"Error: {e}")

    return '200 OK HTTPS.'


if __name__ == "__main__":
    app.run(debug=True)
