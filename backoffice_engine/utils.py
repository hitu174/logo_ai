from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from django.core.files.base import ContentFile
from backoffice_engine.models import Logo


def text2vision(user_prompt,creativity, user_object):
    client=genai.Client(api_key="AIzaSyDX-pSfut3_tHQEog99OKPY4AwKuNgI2GY")
    user=user_prompt
    system_prompt = "i will pass your system generated text in a image model,so give me output as logo input prompt."
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=1000, # set max tokens here
            
            temperature=int(int(creativity)/100)
    
    ),
    contents=user
)

    contents = (response.text,)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )

    for part in response.candidates[0].content.parts:
        
        if part.inline_data is not None:
            # Convert bytes to image
            image = Image.open(BytesIO(part.inline_data.data))
            image_io = BytesIO()
            image.save(image_io, format='PNG')
            image_io.seek(0)

            # Create Django-compatible file

            # Step 3: Save to Generated_image model
            generated_image = Logo.objects.create(
                user=user_object,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temprature=int(creativity)/100
            )
            
            generated_image.save()
            
            image_file = ContentFile(image_io.read(), name=f"{generated_image.id}.png")
            generated_image.image = image_file
            generated_image.save()
            
            return generated_image
            
    


