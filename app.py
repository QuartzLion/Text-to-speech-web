from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

# Home route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to convert text to speech
@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    input_text = request.form['text']  # Get text from form
    language = request.form['language']  # Get language from form
    slow = request.form.get('slow', 'false') == 'true'  # Check for slow speed option

    if not input_text.strip():
        return jsonify({"error": "Text cannot be empty"}), 400

    try:
        # Generate speech using gTTS
        tts = gTTS(text=input_text, lang=language, slow=slow)
        audio_file = "output.mp3"
        tts.save(audio_file)

        # Send the audio file to the client
        return send_file(audio_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
