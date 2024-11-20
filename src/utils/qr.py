# import qrcode

# # Data for the QR Code
# data = "https://cloud.mongodb.com/v2/6739866ffa60cf7dc3fad441#/metrics/replicaSet/6739875cc622b63fe6a88b5d/explorer/edu_tech/profile_teachers/find"

# # Create a QR Code object
# qr = qrcode.QRCode(
#     version=1,  # Controls the size of the QR Code (1 = smallest)
#     error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
#     box_size=10,  # Size of each box in the QR code grid
#     border=4,  # Thickness of the border (minimum is 4)
# )

# # Add data to the QR Code
# qr.add_data(data)
# qr.make(fit=True)

# # Generate an image of the QR Code
# img = qr.make_image(fill_color="black", back_color="white")
# img.save("qrcode.png")  # Save the QR code as an image

# print("QR Code generated and saved as qrcode.png!")


# scan code 

import cv2

# Load the image
image = cv2.imread("qrcode.png")

# Initialize the QRCodeDetector
qr_detector = cv2.QRCodeDetector()

# Detect and decode the QR code
data, points, straight_qrcode = qr_detector(image)

# Check if QR code is detected
if data:
    print(f"QR Code Data: {data}")
else:
    print("No QR Code detected")
