import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
from wand.image import Image as WandImage
from wand.color import Color
import os
from io import BytesIO
import re
import numpy as np
# from utils.utils import *
# from config import *
import logging
from extract_document.amt_and_tax_paid import quarters
from extract_document.challan_det import challan
from extract_document.chellan_data_2 import challan2
logger = logging.getLogger("main")

# NOTE: # If you don't have tesseract executable in your PATH, include the following:
# FOR WINDOWS
# pyt.pytesseract.tesseract_cmd = TESSRACT_PATH

# Set the language to English
custom_config = r'--oem 3 --psm 11 -l eng'
# img_path = 'dataset/Screenshot 2023-03-17 at 11.09.49 AM.png'
form_path = '../uploads/Form-16A/111374Y_2021.pdf'
# image2_path = "dataset/Screenshot 2023-03-18 at 12.08.00 PM.png"

 

def cleanup_text(text):
    # Define a regular expression to match lines containing only special characters
    regex = r'[^[.,?()`~\'[-_+=*&^%$#@!{}\|:";><\]]'

    # Split the text into lines and filter out lines that match the regular expression
    lines = [line for line in text.split('\n') if re.match(regex, line) and len(line)>2]

    # Join the remaining lines back into text
    text = '\n'.join(lines)

    return text

def get_name_address_employer(img,form_details):
    width, height = img.size
    img = img.crop((0, 0, width//2, height//2))
    text = pytesseract.image_to_string(img, config=custom_config)
    text = cleanup_text(text)
    name_regex = r"\bname\b"
    pan_regex = r'\bpan\b'
    img.show()

    lines = re.split(r'\n+', text)

    idx=0
    while idx<len(lines):
        # print(lines[idx])
        if re.search(name_regex, lines[idx], flags=re.IGNORECASE):
            idx=idx+1
            while idx < len(lines) and not re.search(pan_regex, lines[idx], flags=re.IGNORECASE):
                form_details["name_and_add_of_employer"] = form_details["name_and_add_of_employer"] + " " + lines[idx]
                idx += 1
        if re.search(pan_regex, lines[idx], flags=re.IGNORECASE):
            break

        idx += 1
    return form_details

def get_name_address_employee(img,form_details):
    width, height = img.size
    img = img.crop((width//2, 0, width, height//2))
    text = pytesseract.image_to_string(img, config=custom_config)
    text = cleanup_text(text)
    name_regex = r"\bname\b"
    pan_regex = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    date_regex = r'\d{2}-[A-Za-z]{3}-\d{4}'
    year_regex = r'^\d{4}-\d{2}$'

    lines = re.split(r'\n+', text)

    idx=0
    while idx<len(lines):
        # print(lines[idx])
        if re.search(name_regex, lines[idx], flags=re.IGNORECASE):
            idx=idx+1
            for y in range(2):
                form_details["name_and_add_of_employee"] = form_details["name_and_add_of_employee"] + " " + lines[idx]
                idx += 1
        if re.search(pan_regex, lines[idx]):
            form_details["pan_employee"]=lines[idx]
        if re.search(date_regex, lines[idx]):
            if form_details["emp_period_from"]=="" and form_details["name_and_add_of_employee"]!="":
                form_details["emp_period_from"] = lines[idx]
            elif form_details["name_and_add_of_employee"]!="" and form_details["emp_period_from"]!="":
                form_details["emp_period_to"] = lines[idx]
        if re.search(year_regex, lines[idx]):
            form_details["assessment_year"] = lines[idx]

        idx += 1

def get_pan_details(img,form_details):
    width, height = img.size
    img2 = img.crop((0, 0, int(width*0.6), int(height/2)))
    img = img.crop((0, 0, int(width), int(height/2)))
    text = pytesseract.image_to_string(img, config=custom_config)
    text = cleanup_text(text)
    name_regex = r"\bname\b"
    pan_regex = r'\bpan\b'
    summary_regex = r'\bsummary\b'
    cit_regex = r'\bCIT\b'

    lines = re.split(r'\n+', text)
    # img.show(img)

    idx=0
    while idx<len(lines):
        # print(lines[idx])
        if re.search(pan_regex, lines[idx], flags=re.IGNORECASE):
            while idx<len(lines) and len(lines[idx])!=10:
                idx +=1
            form_details["pan_deductor"] = lines[idx]
            idx+=1
            form_details["tan_deductor"] = lines[idx]
            idx+=1
            form_details["pan_employee"] = lines[idx]
            break
        idx += 1
    text = pytesseract.image_to_string(img2, config=custom_config)
    text = cleanup_text(text)
    lines = re.split(r'\n+', text)
    idx=0
    while idx<len(lines):
        if re.search(cit_regex, lines[idx]):
            idx+=1
            while idx < len(lines) and not re.search(summary_regex, lines[idx], flags=re.IGNORECASE):
                form_details["cit_tds"] = form_details["cit_tds"] + " " + lines[idx]
                idx += 1
            
        if idx<len(lines) and re.search(summary_regex, lines[idx], flags=re.IGNORECASE):
            break
        idx+=1
    return form_details

def get_form16(form_path):
    form_details = {}
    form_details["name_and_add_of_employer"] = ""
    form_details["name_and_add_of_employee"] = ""
    form_details["pan_deductor"] = ""
    form_details["pan_employee"] = ""
    form_details["tan_deductor"] = ""
    form_details["cit_tds"] = ""
    form_details["assessment_year"] = ""
    form_details["emp_period_from"] = ""
    form_details["emp_period_to"] = ""
    form_details["quarters"] = {}
    form_details["challan_det"] = {}
    pdf_folder = os.path.splitext(os.path.basename(form_path))[0]
    output_folder = '../uploads/Form-16A'
    output_path = os.path.join(output_folder, pdf_folder)
    os.makedirs(output_path, exist_ok=True)

    with WandImage(filename=form_path, resolution=300) as pdf:
        for page_num in range(len(pdf.sequence)):
            with WandImage(pdf.sequence[page_num]) as page:
                page.format = 'png'
                page.background_color = Color('white')
                page.alpha_channel = 'remove'
                page_path = os.path.join(output_path, f'page{page_num+1}.png')
                page.save(filename=page_path)
    # Get the file paths of the first and second image files
    img_path = os.path.join(output_path, 'page1.png')
    img2_path = os.path.join(output_path, 'page2.png')
        
    img = Image.open(img_path) 

   # Get the size of the image
    width, height = img.size

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.5)
    bottom_half = img.crop((0, height//2, width, height))
    challan_bottom = img.crop((0, height*0.75, width, height))
 
    get_name_address_employer(img,form_details)
    get_name_address_employee(img,form_details)
    get_pan_details(img,form_details)
    form_details["quarters"] = quarters(bottom_half)
    form_details["challan_det"] = challan(challan_bottom)
    form_details["challan_det"].update(challan2(img2_path))

    # print(form_details)
    
    return form_details

# get_form16(form_path)
