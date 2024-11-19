import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration       
cloudinary.config( 
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key =    os.getenv('CLOUD_API_KEY'),
    api_secret = os.getenv('CLOUD_API_SECRET'),
    secure=True
)


def upload_img_to_cloudinary(image_path, folder):
    try:
        # Upload the image to Cloudinary
        response = cloudinary.uploader.upload(image_path, folder=folder)

        # Get the URL of the uploaded image
        image_url = response.get("secure_url")
        return image_url

    except Exception as e:
        return str(e)