import io
import os
import sys
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="apikey.json"

def ocr_book (book_directory):
    client = vision.ImageAnnotatorClient()
    directory = book_directory
    book_name = os.path.basename(os.path.normpath(directory))
    textfile_name = book_name + ".txt"

    list = os.listdir(directory)
    number_of_files = len(list)

    for i in range(number_of_files):
        filename_with_path = os.path.join(directory, book_name) + "_" + str(i + 1) + ".png"

        with io.open(filename_with_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)
        image_context = types.ImageContext(language_hints =["ur"])
        resp = client.document_text_detection(image=image, image_context=image_context)
        if len(resp.text_annotations) > 0:
            page = resp.text_annotations[0].description
            
            with open(textfile_name, mode='a', encoding='UTF-8', errors='strict', buffering=1) as file:
                file.write("Page " + str(i + 1) + " of " + str(number_of_files) + "\r")
                file.write(page + "\r\n")
            
if len(sys.argv) > 1:
    input_book_directory = sys.argv[1]
    ocr_book (input_book_directory)
else:
    exit()