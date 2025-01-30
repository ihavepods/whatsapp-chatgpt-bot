from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# Masukkan API Key OpenAI sebagai environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def chatbot():
    """Webhook untuk menangani pesan WhatsApp dan membalas dengan ChatGPT."""
    incoming_msg = request.values.get("Body", "").strip()

    # Dapatkan balasan dari ChatGPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response['choices'][0]['message']['content']
    except Exception:
        reply = "Maaf, saya mengalami kesalahan. Coba lagi nanti."

    # Kirim balasan ke Twilio
    twilio_resp = MessagingResponse()
    twilio_resp.message(reply)

    return str(twilio_resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
