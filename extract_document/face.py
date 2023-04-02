# import cv2
# from config import *
# import face_recognition
# import os
# import logging
# logger = logging.getLogger("main")

# def detect_faces(image_path):
#     """

#     :param image_path: input image path for detecting the faces in document
#     :return: bool for face detection and documnet image
#     """
#     # load the jpg file into a numpy aary
#     image = face_recognition.load_image_file(image_path)

#     # Find all the faces in the image using the default HOG-based model.
#     # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
#     # See also: find_faces_in_picture_cnn.py
#     face_locations = face_recognition.face_locations(image)
#     logger.debug("[INFO] found {} face(s) In this document.".format(len(face_locations)))

#     if len(face_locations) >= 1:
#         # extract only first face cord.
#         top, right, bottom, left = face_locations[0]

#         # expand the face location
#         top -= 25
#         bottom += 25
#         left -= 25
#         right += 25

#         # You can access the actual face itself like this:
#         crop_face = image[top:bottom, left:right]
#         crop_face = cv2.cvtColor(crop_face, cv2.COLOR_RGB2BGR)

#         # write the face
#         face_path = os.path.split(image_path)
#         face_path = os.path.join(face_path[0], "Faces", "face" + " " + face_path[1])

#         # write the crop face to folder
#         cv2.imwrite(face_path,  crop_face)

#         logger.debug("[INFO] Saving crop face to face folder...")
#         # convert the color
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         # draw the rectangle
#         cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)

#         # if face found return the True result
#         return True, image

#     else:
#         return False, None
# import cv2
# import os
# import logging

# logger = logging.getLogger("main")

# # Load the pre-trained Haar Cascade classifier
# face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# def detect_faces(image_path):
#     """

#     :param image_path: input image path for detecting the faces in document
#     :return: bool for face detection and document image
#     """
#     # load the image into a numpy array
#     image = cv2.imread(image_path)

#     # convert the color
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # detect faces in the image
#     face_rects = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#     logger.debug("[INFO] found {} face(s) In this document.".format(len(face_rects)))

#     if len(face_rects) >= 1:
#         # extract only first face coords.
#         x, y, w, h = face_rects[0]

#         # expand the face location
#         x -= 25
#         y -= 25
#         w += 50
#         h += 50

#         # crop the face from the image
#         crop_face = image[y:y+h, x:x+w]

#         # write the face
#         face_path = os.path.split(image_path)
#         face_path = os.path.join(face_path[0], "Faces", "face" + " " + face_path[1])

#         # write the cropped face to folder
#         cv2.imwrite(face_path,  crop_face)

#         logger.debug("[INFO] Saving crop face to face folder...")

#         # draw the rectangle
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

#         # if face found return the True result
#         return True, image

#     else:
#         return False, None


from PIL import Image
import numpy as np



def detect_faces(image_path):
    
    return False, None


