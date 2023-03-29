import pytesseract
from PIL import Image, ImageEnhance
import re

# img = Image.open('dataset/form b/Screenshot 2023-03-20 at 7.20.03 PM.png')
form_details = {}

def add_decimal(num):
    if len(num) > 2:
        if '.' not in num:
            return num[:-2] + '.' + num[-2:]
        else:
            return num
    else:
        return 0.00

def b_3(img, form_details):
    width, height = img.size

    # Crop the bottom half of the image
    img = img.crop((width/1.5, height/14, width, height))

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    rs_regex = r'\bRs\b'
    amt_regex = r'\bamount\b'

    # Run OCR using Tesseract
    text = pytesseract.image_to_string(img)
    lines = re.split(r'\n+', text)
    i=0
    values = []
    while i<len(lines):
        if lines[i].split():
            words = re.findall(r'\b\d+(?:\.\d{2})?\b', lines[i])
            if len(words)!=0:
                # print(words)
                values.extend(words)  
        i+=1
    form_details["10f"] = {}
    form_details["10g"] = {}
    form_details["10h"] = {}
    form_details["10i"] = {}
    form_details["10j"] = {}
    form_details["10k"] = {}
    form_details["10l"] = {}
    form_details["10f"]["gross"] = float(values[0])
    form_details["10f"]["ded"] = float(values[1])
    form_details["10g"]["gross"] = float(values[2])
    form_details["10g"]["ded"] = float(values[3])
    form_details["10h"]["gross"] = float(values[4])
    form_details["10h"]["ded"] = float(values[5])
    form_details["10i"]["gross"] = float(values[6])
    form_details["10i"]["qualify"] = float(values[7])
    form_details["10i"]["ded"] = float(values[8])
    form_details["10j"]["gross"] = float(values[9])
    form_details["10j"]["qualify"] = float(values[10])
    form_details["10j"]["ded"] = float(values[11])
    form_details["10l"]["gross"] = float(values[12])
    form_details["10l"]["qualify"] = float(values[13])
    form_details["10l"]["ded"] = float(values[14])
    form_details["11"] = float(values[15])
    form_details["12"] = float(values[16])
    form_details["13"] = float(values[17])
    form_details["14"] = float(values[18])
    form_details["15"] = float(values[19])
    form_details["16"] = float(values[20])
    form_details["17"] = float(values[21])
    form_details["18"] = float(values[22])
    form_details["19"] = float(values[23])
    # print(form_details)
    # img.show()

# b_3(img,form_details)
