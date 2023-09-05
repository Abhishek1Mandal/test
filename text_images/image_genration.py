from huggingface_hub import login
from diffusers import StableDiffusionXLPipeline
import torch

# Initialize the Diffuser pipeline and configuration
login()
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-0.9", torch_dtype=torch.float16, variant="fp32", use_safetensors=True
)
pipe.to("cuda")
config = pipe.unet.config


def process_image(prompt: str):
    if not prompt:
        return {"error": "Prompt is missing"}

    image = pipe(prompt=prompt, num_inference_steps=30).images[0]

    # You can return the image in a desired format, like base64 encoded string or save it to a file
    # For this example, we'll return a dictionary with the image result.
    return {"image": image}

# You can add more functions and code related to image generation here
