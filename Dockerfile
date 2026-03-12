FROM python:3.11.12

WORKDIR /app

COPY requirements.txt .
RUN pip3.11 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "if [ \"$SERVICE_TYPE\" = \"qq-bot\" ]; then python qq_bot.py; else python server.py; fi"]
