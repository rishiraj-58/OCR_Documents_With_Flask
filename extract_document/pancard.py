import pytesseract
from PIL import Image
import datetime
import cv2
import sys
import os
import os.path
import re
import numpy as np
from utils.utils import *
from config import *
import logging
logger = logging.getLogger("main")

# NOTE: # If you don't have tesseract executable in your PATH, include the following:
# FOR WINDOWS
pyt.pytesseract.tesseract_cmd = TESSRACT_PATH

# Set the language to English
custom_config = r'--oem 3 --psm 11 -l eng'


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
    text = text.split()
    
    logger.debug("[INFO] Pancard Raw text: `{}` ".format(text))
    # create a list of unwanted word to remove in lower case only
    # remove = ["permanent", "account", "income","tax", "number", "card", "department", "father'", "father's", "father", "of", "signature",
    #           "govt.", "india", "card", "birth", "date", "fathers", "ante", "twat", "Number."]
    remove = ["~","™","-","?","/","<",">","."]

    # remove all the unwanted text with
    text = [t for t in text if len(t) >= 4 and t.lower().strip() not in remove]

    return text


def get_pan_number(image_path):
    img = cv2.imread(image_path)

    # resize the image
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # convert the image to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase the brightness
    img = cv2.addWeighted(img, 1.5, np.zeros(img.shape, img.dtype), 0, 0)

    # Increase the contrast
    # img = cv2.equalizeHist(img)

    # the following command uses the tesseract directory path to get the trained data in the config option
    text = pytesseract.image_to_string(img, config=custom_config)

    clean_text = cleanup_text(text)
    date_regex = "^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-]\d{4}$"
    pan_regex = r'^[a-zA-Z]{5}[0-9]{4}[a-zA-Z]$'
    name_regex = r"\bname\b"

    pan_details = {}
    pan_details["Pan No: "] = ""
    pan_details["Birth Date: "] = ""
    pan_details["Name:"] = ""
    pan_details["Father's Name:"] = ""

    names = []

    flag=0
    # Split the text into lines using regular expressions
    lines = re.split(r'\n+', text)

    # Print each line individually
    for line in lines:
        if line.strip():  # Skip empty lines
            i=line.lower()
            print("text-------", i)
            if re.search(pan_regex, i):
                pan_details["Pan No: "] = line
            elif re.search(date_regex, i):
                pan_details["Birth Date: "] = line
            elif re.search(name_regex, i) and flag==0:
                flag=1
                continue
            if flag==1 and re.match(r'^[a-zA-Z ]+$', i) and len(i)>3:
                pan_details["Name:"] = line
                flag=2
                continue
            if re.search(name_regex, i) and flag==2:
                flag=3
                continue
            if flag==3 and re.match(r'^[a-zA-Z ]+$', i) and len(i)>3:
                pan_details["Father's Name:"] = line
                flag=0
                

    if len(pan_details["Name:"])==0:
        for line in lines:
            if line.strip():
                i=line.lower()
                if i=='govt. of india':
                    flag=1
                    continue
                if flag==1:
                    pan_details["Name:"] = line
                    flag=2
                    continue
                if flag==2:
                    if re.match(r'^[a-zA-Z ]+$', i) and len(i)>3:
                        pan_details["Father's Name:"] = line
                        break

    

    return pan_details
