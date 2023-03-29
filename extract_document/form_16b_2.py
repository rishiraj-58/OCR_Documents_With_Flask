import pytesseract
from PIL import Image, ImageEnhance
import re

# img = Image.open('dataset/form b/Screenshot 2023-03-20 at 7.19.42 PM.png')
form_details = {}

def add_decimal(num):
    if len(num) > 2:
        if '.' not in num:
            return num[:-2] + '.' + num[-2:]
        else:
            return num
    else:
        return 0.00

def b_2(img, form_details):
    width, height = img.size

    img = img.crop((width/1.5, height/8, width, height))

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    rs_regex = r'\bRs\b'
    amt_regex = r'\bamount\b'

    # Run OCR using Tesseract
    text = pytesseract.image_to_string(img)
    lines = re.split(r'\n+', text)
    i=0
    values = []
    while i<len(lines) and not re.search(amt_regex, lines[i], flags=re.IGNORECASE):
        if lines[i].split():
            # print(lines[i])
            num = add_decimal(re.sub(r"[^\d.-]", "", lines[i]))
            # print(num)
            values.extend([num])
        i+=1
    form_details["2g"] = float(values[0])
    form_details["2h"] = float(values[1])
    form_details["3"] = float(values[2])
    form_details["4a"] = float(values[3])
    form_details["4b"] = float(values[4])
    form_details["4c"] = float(values[5])
    form_details["5"] = float(values[6])
    form_details["6"] = float(values[7])
    form_details["7a"] = float(values[8])
    form_details["7b"] = float(values[9])
    form_details["8"] = float(values[10])
    form_details["9"] = float(values[11])
    i+=1
    values = []
    while i<len(lines):
        if lines[i].split():
            # print(lines[i])
            words = re.findall(r'\b\d+(?:\.\d{2})?\b', lines[i])
            values.extend(words)
        i+=1
    form_details["10a"]={}
    form_details["10b"]={}
    form_details["10c"]={}
    form_details["10d"]={}
    form_details["10e"]={}
    form_details["10a"]["gross"] = float(values[0])
    form_details["10a"]["ded"] = float(values[1])
    form_details["10b"]["gross"] = float(values[2])
    form_details["10b"]["ded"] = float(values[3])
    form_details["10c"]["gross"] = float(values[4])
    form_details["10c"]["ded"] = float(values[5])
    form_details["10d"]["gross"] = float(values[6])
    form_details["10d"]["ded"] = float(values[7])
    form_details["10e"]["gross"] = float(values[8])
    form_details["10e"]["ded"] = float(values[9])
 
    # print(form_details)
    # img.show()

# b_2(img,form_details)