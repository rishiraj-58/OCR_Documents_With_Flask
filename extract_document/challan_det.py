import pytesseract
from PIL import Image, ImageEnhance
import re

# Load the image and get its size
# img = Image.open('dataset/Screenshot 2023-03-17 at 11.09.49 AM.png')
# Get the size of the image
# width, height = img.size

# Crop the bottom half of the image
# image = img.crop((0, height*0.75, width, height))
# Adjust brightness, contrast, and sharpness
# enhancer = ImageEnhance.Brightness(image)
# image = enhancer.enhance(1)

# enhancer = ImageEnhance.Contrast(image)
# image = enhancer.enhance(2.5)

def challan(image):
    # Run OCR using Tesseract
    text = pytesseract.image_to_string(image)
    lines = re.split(r'\n+', text)
    amt_regex = r"\d+\.\d{2}\b"

    i=0
    idx=1
    chellan_data = {}
    while i<len(lines):
        if lines[i].split():
            words = re.findall(r'\b\d+(?:\.\d{2})?\b', lines[i])
            if len(words)>=4:
                chellan_data[idx] = {}
                words = [word for word in words if len(word) > 1]
                if re.search(amt_regex, words[0]):
                    chellan_data[idx]["tax_dep"] = float(words[0])
                else:
                    words[0] = words[0][:-2] + "." + words[0][-2:]
                    chellan_data[idx]["tax_dep"] = float(words[0])
                chellan_data[idx]["BSR_code"]=words[1]
                if len(words[2])==2:
                    if len(words[3])==2:
                        words[3]=words[3]+words[4]
                        words[2]=words[2]+words[3]
                    else:
                        words[2]=words[2]+words[3]
                elif len(words[2])==4:
                    words[2]=words[2]+words[3]
                if len(words[2])==8:
                    date = '-'.join([words[2][:2], words[2][2:4], words[2][4:]])
                    chellan_data[idx]["date"] = date
                chellan_data[idx]["chellan_sn_no"] = words[-1]
                idx+=1
        i+=1
    # print(chellan_data)
    return chellan_data
