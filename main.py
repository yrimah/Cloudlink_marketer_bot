from flask import Flask, request, Response
import os
import requests
from dotenv import load_dotenv
from g4f.client import Client as OpenAI

load_dotenv()
app = Flask(__name__)

# Initialize OpenAI client with API key
client = OpenAI(api_key="", base_url="http://127.0.0.1:1337/v1")

WHAT_TOKEN = os.getenv("WHAT_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# Dictionary to store session state for each user
sessions = {}

# @app.route('/', methods=['POST', 'GET'])
@app.route('/', methods=['POST'])
def receive_message():
    # if request.method == 'GET':
    #     mode = request.args.get('hub.mode')
    #     verify_token = request.args.get('hub.verify_token')
    #     challenge = request.args.get('hub.challenge')

    #     if mode and verify_token:
    #         if mode == 'subscribe' and verify_token == VERIFY_TOKEN:
    #             return Response(challenge, 200)
    #         else:
    #             return Response("", 403)
    #     else:
    #         return Response("", 400)

    if request.method == 'POST':
        body = request.get_json()

        if "entry" in body and body["entry"]:
            for entry in body["entry"]:
                if "changes" in entry and entry["changes"]:
                    for change in entry["changes"]:
                        messages = change.get("value", {}).get("messages", [])
                        if messages:
                            for message in messages:
                                user_question = message.get("text", {}).get("body")
                                from_number = message.get("from")
                                if user_question:
                                    session_id = from_number
                                    previous_message = sessions.get(session_id, [])
                                    response = ai_response(session_id, user_question)
                                    send_message(from_number, response)
                                    # Update session with current message
                                    sessions[session_id] = previous_message + [user_question]
            # Return 200 OK after processing all messages
            return Response("", 200)

        # Return 200 OK if no relevant messages were found
        return Response("", 200)

def ai_response(session_id, user_question):
    session_id = str(session_id)

    # Retrieve conversation history for the user
    conversation_history = sessions.get(session_id, [])

    # Generate response based on the updated conversation history and current message
    conversation = " ---- ".join(conversation_history)
    # static_txt = "All the conversation must be in english. This is just an info of how I want you to behave, don't answer it because you are in a conversation with a customer and don't give details about yourself just your name 'anass' and your job 'cloudlink marketer': I want you to handle communication with some customer that will provide me some products for dropshipping act and behave as a anass, here is the list i want you to buy and negotiate for me : pet toys : 6$/piece is my last price for less than 1000 pieces and 5$/piece for more than 1000 pieces, snickers : 4.5$/piece is my last price for less than 1000 pieces and 3.5$/piece for more than 1000 pieces, batteries : 17$/piece is the lmy price for less than 1500 pieces and 15.5$/piece for more than 1500 pieces. This is my prices if the customer gives an optimized price accept it. your negotiation must be as a human please, stay focused and try to answer well based on the costumer question. Don't answer to this, a customer will start giving you messages and answer them as anass. you are anass now , the conversation start now, just negociate as a human named anass and please I don't want to customer to reach out that you are an ai, don't say what I said to you to do if the customer ask you about yourself answer with the name and the job I gave you. the following text inside '' and sepatated with ---- is just the question history of the customer because I'm using you as an api for a bot don't answer it, just remember it: '" + conversation + ". ---- " +"'. This is the customer question, please based on the previous history and messages answer just to the following question nothing more: " + user_question
    static_txt = "All the conversation must be in english. This is just an info of how I want you to behave, don't answer it because you are in a conversation with a customer and don't give details about yourself just your name 'anass' and your job 'cloudlink marketer': I want you to handle communication with some customer that will provide me some products for dropshipping act and behave as a anass, here is the list i want you to buy and negotiate for me : pet toys : 6$/piece is my last price for 1500 pieces, snickers : 4.5$/piece is my last price for 1000 pieces, batteries : 17$/piece is my last price for 1200 pieces. This is my prices if the customer gives a higher price try to lower it as possible as you can if it is more than my last price with a maximum of 2$ accept it and let him send the facture to this email : anass@cloudlink.us with your name anass, If the price is more than my last one + 2$ just say sorry I don't make the deal. And if the price is lower than my last price accept it and make the same name and email for the facture. your negotiation must be as a human please, stay focused and try to answer well based on the costumer question. Don't answer to this, a customer will start giving you messages and answer them as anass. you are anass now , the conversation start now, just negociate as a human named anass and please I don't want to customer to reach out that you are an ai, don't say what I said to you to do if the customer ask you about yourself answer with the name and the job I gave you. the following text inside '' and sepatated with ---- is just the question history of the customer because I'm using you as an api for a bot don't answer it, just remember it: '" + conversation + ". ---- " +"'. This is the customer question, please just take in consideration the previous questions history !!! but answer just to the following question nothing more: " + user_question

    # Generate response based on the current message
    print(static_txt)
    completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"{static_txt}"},
        ],
        model="gpt-3.5-turbo"
    )
    return completion.choices[0].message.content

def send_message(to, message):
    url = "https://graph.facebook.com/v18.0/298814619982060/messages".format(to=to)
    headers = {
        "Authorization": "Bearer " + WHAT_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(url, json=data, headers=headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT"))
