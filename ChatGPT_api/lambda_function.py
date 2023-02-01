import json
import openai
import base64
import io
import os
from openai import api_key,Image
from PIL import Image as im


api_key = os.environ.get("OPENAI_API_KEY")
responseformat = "b64_json"
width, height = 256, 256

def preprocess_image(basestring):
    imgdata = base64.b64decode(str(basestring))
    img = im.open(io.BytesIO(imgdata))
    or_width, or_height = img.size
    if or_height!=or_width:
        s= max(or_height, or_width)
        area = (0, 0, s, s)
        img = img.crop(area)
    image = img.resize((width, height))
    byte_stream = io.BytesIO()
    img.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()
    return byte_array
    
def opai_imagefromprompt(txt, n = 1, size = "1024x1024"):
    response = openai.Image.create(
      prompt= txt,
      n=n,
      size=size,
      response_format = responseformat,
    )
    print(response["data"])
    return response
    
def opai_imagefromimage(basestring, n = 1, size = "1024x1024"):
    
    byte_array = preprocess_image(basestring)
    response = openai.Image.create_variation(
      image=byte_array,
      n=n,
      size=size,
      response_format = responseformat,
    )
    return response

modelDict = {
    "opai_imagefromprompt": opai_imagefromprompt,
    "opai_imagefromimage": opai_imagefromimage,
    }

def lambda_handler(event, context):
     # Call functions to select dalle models
    context = json.loads(json.dumps(event))
    result = modelDict.get(context["target_model"], lambda: 'Invalid')(context["prompt"],context["counts"],context["size"])
    return result
    
