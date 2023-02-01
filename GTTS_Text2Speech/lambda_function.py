import json
from gtts import gTTS
import base64
import io

def lambda_handler(event, context):
    data = json.loads(json.dumps(event))
    mytext = data["payload"]
    audio = gTTS(text=mytext, lang="en", slow=False)
    audiobytes = io.BytesIO()
    audio.write_to_fp(audiobytes)
    audiobytes.seek(0)
    audiob64 = base64.b64encode(audiobytes.read())
    return {"b64":audiob64}
