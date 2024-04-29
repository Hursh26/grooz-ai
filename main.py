import hd
from flask import Flask, render_template, redirect, url_for, request, send_file
import speech_recognition as sr
from gtts import gTTS
import tempfile
import io
from flask_socketio import send, SocketIO

app= Flask(__name__)
app.config['SECRET']="Secret!123"
socketio= SocketIO(app, cors_allowed_origins='*')

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/chat', methods=['GET','POST'])
def chat():
    return render_template("chat.html")

@socketio.on('message')
def message_handler(message):
    if message == 'Start':
        print(message)
        send(message,broadcast=True)

@app.route('/upload', methods=['POST','GET'])
def speech_to_text():
    text = request.json.get('text')

    print(text)

    audio_text= hd.assistent(text)

    # Create a temporary file to store the synthesized speech
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    tts = gTTS(text=audio_text, lang='en')
    speech_bytes = io.BytesIO()
    tts.write_to_fp(speech_bytes)
    speech_bytes.seek(0)
    
    return send_file(
        speech_bytes,
        mimetype='audio/mpeg',
        as_attachment=False,
        download_name='speech.mp3'
    )

if __name__ == "__main__":
    socketio.run(app, debug=True)