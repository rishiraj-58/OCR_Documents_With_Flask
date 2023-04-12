import re
import pytesseract as pyt
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import cv2
import logging
logger = logging.getLogger("main")


# image_path = "../uploads/Aadhar_Card/Screenshot_2023-03-13_at_10.45.33_PM.png"

aadhaar_details = {}
       
def get_aadhar_text(image_path):
    # Load the image using PIL
    img = Image.open(image_path)
    aadhaar_details['Aadhar No']=''
    aadhaar_details["Name"]=''
    aadhaar_details["Date of Birth"]=''
    aadhaar_details["Gender"]=''

    # increase the brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.25)
    text = pyt.image_to_string(img, lang="eng+hin+mar", config=('--oem 1 --psm 11'))
    enrol_regex = r"\bEnrolment\b"
    ident_regex = r"\bproof of identity\b"
    through_regex = r"/bthroughout/b"

     # Split the text into lines using regular expressions
    lines = re.split(r'\n+', text)
    flag=0
    width, height = img.size
    idx=0
    while idx<len(lines):
        if re.search(enrol_regex, lines[idx]):
            flag=1
        if re.search(ident_regex, lines[idx]) or re.search(through_regex, lines[idx]):
            flag=2
            break
        idx+=1
    if flag==1:
        img = img.crop((0, int(height/2), int(width), int(height)))
    if flag==2:
        img = img.crop((0, int(height/2), int(width/2), int(height)))
    text = pyt.image_to_string(img, lang="eng", config=('--oem 1 --psm 11'))
    lines = re.split(r'\n+', text)
    idx=0
    while idx<len(lines):
        line=lines[idx]
        # Extract words that match the regex pattern
        matching_words = re.findall(r'[A-Za-z0-9/:]+', line)

        # Join the matching words into a string
        line = ' '.join(matching_words)
        if re.match(r'India', line) or re.search(r'Government', line):
            idx+=1
            continue
        elif re.search(r'\d{2}/\d{2}/\d{4}', line):
            if len(lines[idx-1])>3:
                aadhaar_details["Name"]=lines[idx-1]
            date=re.search(r'\d{2}/\d{2}/\d{4}', line)
            date = date.group(0)
            aadhaar_details["Date of Birth"]=date
        elif re.search(r'MALE', line) or re.search(r'FEMALE', line):
            gender=re.search(r'MALE', line)
            if gender:
                gender = gender.group(0)
                aadhaar_details["Gender"]="MALE"
            else:
                aadhaar_details["Gender"]="FEMALE"
        elif re.match(r"[0-9]{4}\s[0-9]{4}\s[0-9]{4}", line):
            aadhaar_details['Aadhar No']=line
        idx+=1

    return aadhaar_details
# get_aadhar_text(image_path)