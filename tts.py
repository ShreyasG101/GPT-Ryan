import requests
import curl
from apikey import elevenlabskey


jimmy_voice_id= 'cD0F69rQB08cHYnFFX9F'
CHUNK_SIZE = 1024
url = f"https://api.elevenlabs.io/v1/text-to-speech/{jimmy_voice_id}"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": elevenlabskey
}







def output_speech(text, output_path):
    data = {
        "text": text,
        "voice_settings": {
            "stability": 1,
            "similarity_boost": .75
        }
        }
    response = requests.post(url, json=data, headers=headers)
    c = curl.parse(response, return_it=True)
    print(c)

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:   
                f.write(chunk)