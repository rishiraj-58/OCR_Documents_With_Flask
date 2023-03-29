import pytesseract
from PIL import Image, ImageEnhance
import re

# img = Image.open('dataset/form b/Screenshot 2023-03-20 at 7.19.03 PM.png')
custom_config = r'--oem 3 --psm 11 -l eng'

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
    # img.show()

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
    details_regex = r'\bdetails\b'
    cit_regex = r'\bCIT\b'

    lines = re.split(r'\n+', text)
    # img.show(img)

    idx=0
    while idx<len(lines):
        # print(lines[idx])
        if re.search(pan_regex, lines[idx], flags=re.IGNORECASE):
            # while idx<len(lines) and len(lines[idx])!=10:
            idx +=3
            form_details["pan_deductor"] = lines[idx]
            idx+=1
            form_details["tan_deductor"] = lines[idx]
            # idx+=1
            # form_details["pan_employee"] = lines[idx]
            break
        idx += 1
    text = pytesseract.image_to_string(img2, config=custom_config)
    text = cleanup_text(text)
    lines = re.split(r'\n+', text)
    idx=0
    while idx<len(lines):
        if re.search(cit_regex, lines[idx]):
            idx+=1
            while idx < len(lines) and not re.search(details_regex, lines[idx], flags=re.IGNORECASE):
                form_details["cit_tds"] = form_details["cit_tds"] + " " + lines[idx]
                idx += 1
            
        if idx<len(lines) and re.search(details_regex, lines[idx], flags=re.IGNORECASE):
            break
        idx+=1
    