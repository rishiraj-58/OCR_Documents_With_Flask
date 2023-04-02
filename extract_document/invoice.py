import pytesseract
from PIL import Image, ImageEnhance
import os
import os.path
import re
import numpy as np
import logging
logger = logging.getLogger("main")

img_path="uploads/Others/Screenshot_2023-03-15_at_12.48.27_PM.png"
taxDetails = {}
taxDetails["name"]=""
taxDetails["shipTo"]=""
taxDetails["billTo"]=""
taxDetails["goods"]=[]
taxDetails["total"]={}


# Set the language to English
custom_config = r'--oem 3 --psm 11 -l eng'

def add_decimal(num):
    if len(num) > 2:
        if '.' not in num:
            return num[:-2] + '.' + num[-2:]
        else:
            return num
    # else:
    #     return 0.00
def remove_dec(decimal_num):
    return int(decimal_num) + 0.00
def remove_for(sentence):
    words = sentence.split()
    if words[0].lower() == 'for':
        return ' '.join(words[1:])
    else:
        return sentence

def top_det(image_path):
    img = Image.open(image_path) 
    width, height = img.size
    img = img.crop((0, 0, width/3, height/2))
    text = pytesseract.image_to_string(img, config=custom_config)
    # text = text.replace("|", "")
    lines = re.split(r'\n+', text)
    buyer_regex=r"\bBuyer\b"
    consignee_regex=r"\bConsignee\b"
    gst_regex=r'\bGSTIN'
    i=0
    
    while i<len(lines):
        if lines[i].strip():
            if re.search(consignee_regex, lines[i]):
                i+=1
                while not re.search(gst_regex, lines[i]):
                    taxDetails["shipTo"]+=lines[i]
                    i+=1
            if re.search(buyer_regex, lines[i]):
                i+=1
                while not re.search(gst_regex, lines[i]):
                    taxDetails["billTo"]+=lines[i]
                    i+=1           
        i+=1


def invoice_details(image_path):
    top_det(image_path)
    # Load the image
    img = Image.open(image_path) 
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    width, height = img.size
    img = img.crop((0, height//2, width, height))

    # the following command uses the tesseract directory path to get the trained data in the config option
    text = pytesseract.image_to_string(img, config=custom_config)
    text = text.replace("|", "")
    # text = text.replace(' ', '\n')

    tax_amt_regex = r"\bTax Amount"
    percent_regex=r"[%]"
    total_regex=r"\bTotal\b"
    for_regex=r"\bfor\b"


    # Split the text into lines using regular expressions
    lines = re.split(r'\n+', text)
    flag=0
    i=0
    # Print each line individually
    temp={}
    arr=[]
    tot=0
    while i<len(lines):
        if lines[i].strip():  # Skip empty lines
            if flag==2:
                break
            if flag==1:
                while i<len(lines):
                    if re.search(tax_amt_regex, lines[i]):
                        i+=1
                        flag=2
                        break
                    if re.search(percent_regex, lines[i]):
                        i+=1
                    if re.search(total_regex, lines[i]):
                        tot=1
                    words = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', lines[i])
                    for word in words:
                        word=add_decimal(word)
                        arr.append(word)
                    arr = list(filter(lambda x: x is not None, arr))
                    
                    if len(arr)==4:
                        if tot==0:
                            temp["taxable_val"]=float(arr[0].replace(',',''))
                            temp["cgst"]=float(arr[1].replace(',',''))
                            temp["sgst"]=float(arr[2].replace(',',''))
                            temp["tot_tax"]=float(arr[3].replace(',',''))
                            taxDetails["goods"].append(temp)
                            arr=[]
                        else:
                            taxDetails["total"]["taxable_val"]=float(arr[0].replace(',',''))
                            taxDetails["total"]["cgst"]=float(arr[1].replace(',',''))
                            taxDetails["total"]["sgst"]=float(arr[2].replace(',',''))
                            taxDetails["total"]["tot_tax"]=float(arr[3].replace(',',''))
                            taxDetails["total"]["subtotal"]=remove_dec(taxDetails["total"]["taxable_val"]+taxDetails["total"]["tot_tax"])
                    i+=1
                    # if i<len(lines) and len(arr)==0 and tot==0:
                    #     print(lines[i])
                    #     temp["HSN/SAC"]=lines[i]
                    #     i+=1

                
            if i<len(lines) and re.search(tax_amt_regex, lines[i]):
                if flag==0:
                    flag=1
                    i+=1
                    temp["HSN/SAC"]=lines[i]
                    

        i+=1
    while i<len(lines):
        if lines[i].strip():
            if re.search(for_regex, lines[i]):
                sentance=remove_for(lines[i])
                taxDetails["name"]=sentance
        i+=1
    # print(taxDetails)
    return taxDetails
               
# top_det(img_path)
# invoice_details(img_path)