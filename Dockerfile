FROM python:3.11.2

WORKDIR /app

COPY . .

RUN python3 -m venv chat_bot_env

RUN . chat_bot_env/bin/activate && pip install --no-cache-dir -r requirements.txt

EXPOSE 80
