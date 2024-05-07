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
    # add a text of how you want the bot to behave
    static_txt = "..."
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
