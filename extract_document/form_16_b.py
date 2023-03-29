import pytesseract
from PIL import Image, ImageEnhance
from wand.image import Image as WandImage
from wand.color import Color
import os
import re
from extract_document.form_16b_2 import b_2
from extract_document.form_16b_3 import b_3
from extract_document.form_16b_1st_half import get_name_address_employer, get_name_address_employee, get_pan_details

form_details = {}
def add_decimal(num):
    if len(num) > 2:
        if '.' not in num:
            return num[:-2] + '.' + num[-2:]
        else:
            return num
    else:
        return 0.00

# img = Image.open('dataset/form b/Screenshot 2023-03-21 at 6.58.17 PM.png')
# img2 = Image.open('dataset/form b/Screenshot 2023-03-21 at 6.58.36 PM.png')
# img3 = Image.open("dataset/form b/Screenshot 2023-03-21 at 6.58.40 PM.png")
form_path = '../uploads/Form-16B/111374Y_2021.pdf'

def f16b(form_path):
    form_details = {}
    form_details["name_and_add_of_employer"] = ""
    form_details["name_and_add_of_employee"] = ""
    form_details["pan_deductor"] = ""
    form_details["tan_deductor"] = ""
    form_details["pan_employee"] = ""
    form_details["cit_tds"] = ""
    form_details["assessment_year"] = ""
    form_details["emp_period_from"] = ""
    form_details["emp_period_to"] = ""

    pdf_folder = os.path.splitext(os.path.basename(form_path))[0]
    output_folder = '../uploads/Form-16B'
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
    img3_path = os.path.join(output_path, 'page3.png')
    img = Image.open(img_path)
    img2 = Image.open(img2_path)
    img3 = Image.open(img3_path)
    width, height = img.size

    get_name_address_employer(img,form_details)
    get_name_address_employee(img,form_details)
    get_pan_details(img,form_details)
    
    # Crop the bottom half of the image
    img = img.crop((width/1.5, height/2, width, height))
    # img.show()

    # enhancer = ImageEnhance.Contrast(img)
    # img = enhancer.enhance(2)

    rs_regex = r'\bRs\b'

    # Run OCR using Tesseract
    text = pytesseract.image_to_string(img)
    lines = re.split(r'\n+', text)
    i=0
    # while i<len(lines):
    #     if lines[i].split():
    #         if re.search(rs_regex, lines[i], flags=re.IGNORECASE):
    #             i+=1
    #             break
    #     i+=1
    values = []
    while i<len(lines):
        if lines[i].split():
            words = re.findall(r'\b\d+(?:\.\d{2})?\b', lines[i])
            values.extend(words)
        i+=1
    form_details["1a"] = float(values[0])
    form_details["1b"] = float(values[1])
    form_details["1c"] = float(values[2])
    form_details["1d"] = float(values[3])
    form_details["1e"] = float(values[4])
    form_details["2a"] = float(values[5])
    form_details["2b"] = float(values[6])
    form_details["2c"] = float(values[7])
    form_details["2d"] = float(values[8])
    form_details["2e"] = float(values[9])
    b_2(img2,form_details)
    b_3(img3, form_details)
    # print(form_details)
    return form_details
    


# f16b(form_path)
