import json, subprocess, ffmpeg

from openai import OpenAI
from flask import Blueprint, jsonify, request, render_template, send_file
from io import BytesIO
from base64 import b64decode, b64encode

ai = OpenAI()
bp = Blueprint("chat", __name__)

@bp.route('/')
def chat():
    return "<h1> Chat </h1>"

@bp.route('/v1/convo', methods=['POST'])
def convo():
    audio_input = request.files['audio'].read()

    wav_bytes, _ = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='wav')
        .run(input=audio_input, capture_stdout=True, capture_stderr=True)
    )

    response = ai.chat.completions.create(
        model="gpt-4o-audio-preview",
        modalities=["text","audio"],
        audio={"voice":"alloy","format":"wav"},
        messages=[
            {
                "role":"user",
                "content": [
                    {
                        "type":"input_audio",
                        "input_audio": {
                            "data": b64encode(wav_bytes).decode(),
                            "format": "wav"
                        }
                    }
                ]
            }
        ]
    )
    

    reply_wav = b64decode(response.choices[0].message.audio.data)
    return send_file(BytesIO(reply_wav), mimetype='audio/wav')
