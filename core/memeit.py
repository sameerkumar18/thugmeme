import os
import uuid

from PIL import Image, ImageFont, ImageDraw, ImageOps
# from cv2 import CascadeClassifier, imread, cvtColor, COLOR_BGR2GRAY, rectangle
import cv2

from thugmeme.settings import OBJECT_STORAGE_PROVIDER, OBJECT_STORAGE_CREDENTIALS
from core.upload import Upload

from thugmeme.settings import STATICFILES_DIRS, BASE_DIR


class ThugLifeMeme:
    """Adds the standard ThugLife Cigar and glasses over the detected faces in the image"""

    def __init__(self):
        pass

    def meme(self, image_path):
        # base_dir = BASE_DIR

        # base_dir += '/' if not base_dir == '/' else ''
        image_path = image_path
        # thug life meme mask image path
        mask_path = STATICFILES_DIRS[0] + "/images/mask.png"
        # haarcascade path
        casc_path = STATICFILES_DIRS[0] + "/xml/haarcascade_frontalface_default.xml"

        # cascade classifier object
        face_cascade = cv2.CascadeClassifier(casc_path)

        # read input image
        image = cv2.imread(image_path)
        print(os.listdir())
        print(image, image_path)
        # convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect faces in grayscale image
        faces = face_cascade.detectMultiScale(gray, 1.15)

        # open input image as PIL image
        background = Image.open(image_path)

        # paste mask on each detected face in input image
        for (x, y, w, h) in faces:
            # just to show detected faces
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # imshow('face detected', image)
            # waitKey(50)

            # open mask as PIL image
            mask = Image.open(mask_path)
            # resize mask according to detected face
            mask = mask.resize((w, h), Image.ANTIALIAS)

            # define o
            # ffset for mask
            offset = (x, y)
            # paste mask on background
            background.paste(mask, offset, mask=mask)

        # paste final thug life meme
        output_path = "thug_" + str(image_path.split(".")[0]) + ".png"
        background.save(output_path)
        obj = Upload(provider=OBJECT_STORAGE_PROVIDER, credentials=OBJECT_STORAGE_CREDENTIALS, file=output_path)
        cloud_url = obj.upload_file()
        os.remove(os.getcwd() + '/' + output_path)
        return cloud_url


class TextMeme:
    """Adds text and adds white space around the image for a meme like look"""

    def __init__(self):
        pass

    def meme(self, top_text=" ", bottom_text=" ", filename=""):
        if len(top_text) < 2:
            top_text = " "
        if len(bottom_text) < 2:
            bottom_text = " "

        img = ImageOps.expand(Image.open(filename), border=80, fill='white')
        image_size = img.size

        # find biggest font size that works
        font_size = int(image_size[1] / 10)
        font = ImageFont.truetype(STATICFILES_DIRS[0] + "/fonts/impact-opt.ttf", font_size)
        top_text_size = font.getsize(top_text)
        bottom_text_size = font.getsize(bottom_text)
        while top_text_size[0] > image_size[0] - 20 or bottom_text_size[0] > image_size[0] - 20:
            font_size = font_size - 1
            font = ImageFont.truetype(STATICFILES_DIRS[0] + "/fonts/Impact.ttf", font_size)
            top_text_size = font.getsize(top_text)
            bottom_text_size = font.getsize(bottom_text)

        # find top centered position for top text
        top_text_x = (image_size[0] / 2) - (top_text_size[0] / 2)
        top_text_y = 0
        top_text_position = (top_text_x, top_text_y)

        # find bottom centered position for bottom text
        bottom_text_x = (image_size[0] / 2) - (bottom_text_size[0] / 2)
        bottom_text_y = image_size[1] - bottom_text_size[1]
        bottom_text_position = (bottom_text_x, bottom_text_y)

        draw = ImageDraw.Draw(img)

        # draw outlines
        # there may be a better way
        # outline_range = int(font_size / 10)
        outline_range = 0
        for x in range(-outline_range, outline_range + 1):
            for y in range(-outline_range, outline_range + 1):
                draw.text((top_text_position[0] + x, top_text_position[1] + y), top_text, (0, 0, 0), font=font)
                draw.text((bottom_text_position[0] + x, bottom_text_position[1] + y), bottom_text, (0, 0, 0), font=font)

        draw.text(top_text_position, top_text, (0, 0, 0), font=font)
        draw.text(bottom_text_position, bottom_text, (0, 0, 0), font=font)
        output_path = str(uuid.uuid4().hex) + ".png"
        img.save(output_path)
        obj = Upload(provider=OBJECT_STORAGE_PROVIDER, credentials=OBJECT_STORAGE_CREDENTIALS, file=output_path)
        cloud_url = obj.upload_file()
        os.remove(os.getcwd() + '/' + output_path)
        return cloud_url
