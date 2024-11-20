from PIL import Image
import pytesseract

# Load the QR code image
image_path = "qr_code.png"  # Replace with your file path
image = Image.open(image_path)

# Perform OCR
decoded_text = pytesseract.image_to_string(image)

# Output
print("Decoded Text:", decoded_text)


# 

import cv2
from pyzbar.pyzbar import decode

# Load the image containing the QR code
image_path = "qr_code.png"  # Replace with the path to your image
image = cv2.imread(image_path)

# Decode the QR code
qr_codes = decode(image)

# Process and display the decoded data
for qr_code in qr_codes:
    print("Decoded Data:", qr_code.data.decode('utf-8'))
    print("Type:", qr_code.type)

if not qr_codes:
    print("No QR code found in the image.")
