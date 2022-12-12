import os
import io
import sys, base64
import subprocess
import openai
import urllib.request
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

with open("file.txt", "r") as file:
    text_img = file.readline()


openai.api_key = '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'

response = openai.Image.create(
  prompt=text_img,
  n=1,
  size="512x512"
)

image_url = response['data'][0]['url']

urllib.request.urlretrieve(image_url, f'./Image/Dalle/{text_img}.png')


# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

os.environ['STABILITY_KEY'] = 'sk-dLAEOaxENFYruvfhxx7rLVsOUVRfTaRMR0kJKQ3SjRDoAk52'

# Set up our connection to the API.
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    verbose=True, # Print debug messages.
)

# Set up our initial generation parameters.
answers = stability_api.generate(
    prompt=text_img, # If a seed is provided, the resulting generated image will be deterministic.
                    # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                    # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
    steps=50, # Step Count defaults to 50 if not specified here.
    cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                   # Setting this value higher increases the strength in which it tries to match your prompt.
                   # Defaults to 7.0 if not specified.
    width=512, # Generation width, defaults to 512 if not included.
    height=512, # Generation height, defaults to 512 if not included.
    samples=1, # Number of images to generate, defaults to 1 if not included.
    sampler=generation.SAMPLER_K_DPM_2_ANCESTRAL # Choose which sampler we want to denoise our generation with.
                                                 # Defaults to k_lms if not specified. Clip Guidance only supports ancestral samplers.
                                                 # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_lms)
)

# # Set up our warning to print to the console if the adult content classifier is tripped.
# # If adult content classifier is not tripped, save generated images.
            
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            img.save(f'./Image/SD/{text_img}.png') # Save our generated images with their seed number as the filename.
