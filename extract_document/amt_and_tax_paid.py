import pytesseract
from PIL import Image, ImageDraw
import re

# Load the image and get its size
# img = Image.open('dataset/Screenshot 2023-03-17 at 11.09.49 AM.png')
# Get the size of the image
# width, height = img.size

# Crop the bottom half of the image
# img = img.crop((0, height/2, width, height))

def quarters(img):

    # Run OCR using Tesseract
    text = pytesseract.image_to_string(img)
    lines = re.split(r'\n+', text)
    section_regex = r"section\s*200"
    amt_regex = r"\d+\.\d{2}\b"

    form_index = {}
    i=0
    while i<len(lines):
        if lines[i].split():
            line=lines[i]
            if re.search(section_regex, line, re.IGNORECASE):
                i+=1
                line=lines[i]
                # check if the line contains the specific text pattern
                for y in range(4):
                    line=lines[i]
                    if re.search(r'\b[A-Z]{8}\b', line):
                        form_index[y] = {}
                        # store the word in the line with the specific pattern in "receipt"
                        form_index[y]["receipt"] = re.findall(r'\b[A-Z]{8}\b', line)[0]
                        # store the next 3 words after the pattern as amt_paid, amt_tax_ded, amt_tax_dep
                        words = re.findall(r'\b\d+(?:\.\d{2})?\b', line)
                        if re.search(amt_regex, words[0]):
                            form_index[y]["amt_paid"] = float(words[0])
                        else:
                            words[0] = words[0][:-2] + "." + words[0][-2:]
                            form_index[y]["amt_paid"] = float(words[0])
                        if re.search(amt_regex, words[1]):
                            form_index[y]["tax_ded"] = float(words[1])
                        else:
                            words[1] = words[1][:-2] + "." + words[1][-2:]
                            form_index[y]["tax_ded"] = float(words[1])
                        if re.search(amt_regex, words[2]):
                            form_index[y]["tax_dep"] = float(words[2])
                        else:
                            words[2] = words[2][:-2] + "." + words[2][-2:]
                            form_index[y]["tax_dep"] = float(words[2])
                    i+=1
                total = re.findall(r'\b\d+(?:\.\d{2})?\b', lines[i])
                form_index[4] = {}
                if re.search(amt_regex, words[0]):
                    form_index[4]["tot_amt_paid"] = float(words[0])
                else:
                    words[0] = words[0][:-2] + "." + words[0][-2:]
                    form_index[4]["tot_amt_paid"] = float(words[0])
                if re.search(amt_regex, words[1]):
                    form_index[4]["tot_tax_ded"] = float(words[1])
                else:
                    words[1] = words[1][:-2] + "." + words[1][-2:]
                    form_index[4]["tot_tax_ded"]  = float(words[1])
                if re.search(amt_regex, words[2]):
                    form_index[4]["tot_tax_dep"]  = float(words[2])
                else:
                    words[2] = words[2][:-2] + "." + words[2][-2:]
                    form_index[4]["tot_tax_dep"] = float(words[2])     
        i+=1
    # print(form_index)
    return form_index

