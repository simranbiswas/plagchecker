import cv2
import os
import pytesseract
from pytesseract import Output
import matplotlib.pyplot as plt

def highlight_text(sent,filename):
    tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = cv2.imread(os.path.join("static/uploads", filename))
    d = pytesseract.image_to_data(img, output_type=Output.DICT, lang='eng', config=tessdata_dir_config)
    n_boxes = len(d['level'])

    overlay = img.copy()

    for word in sent:
        i = 0
        while i < n_boxes:
            text = d['text'][i]
            # print(text)
            if text == word:
                flag = True
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 255), -1)
                i += 1
                while flag == True and i < n_boxes:
                    text = d['text'][i]
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 255), -1)
                    if '.' in str(text):
                        flag = False
                    i += 1
            else:
                i += 1

    alpha = 0.4  # Transparency factor.
    # Following line overlays transparent rectangle over the image
    img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    r = 1000.0 / img_new.shape[1]  # resizing image without loosing aspect ratio
    dim = (1000, int(img_new.shape[0] * r))
    # perform the actual resizing of the image and show it
    resized = cv2.resize(img_new, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('img', resized)
    cv2.imwrite(os.path.join("static/uploads", filename), resized)
    cv2.waitKey(0)

# # read the image and get the dimensions
# img = cv2.imread(filename)
# h, w, _ = img.shape # assumes color image
#
# # run tesseract, returning the bounding boxes
# boxes = pytesseract.image_to_boxes(img)
# print(pytesseract.image_to_string(img)) #print identified text
#
# # draw the bounding boxes on the image
# for b in boxes.splitlines():
#     b = b.split()
#     print(b)
#     cv2.rectangle(img, ((int(b[1]), h - int(b[2]))), ((int(b[3]), h - int(b[4]))), (0, 255, 0), 2)
#
# plt.imshow(img)
# plt.show()


# for i in range(n_boxes):
#     text = d['text'][i]
#     if text == 'agent' or text == 'environment':
#
#         (x1, y1, w1, h1) = (d['left'][i + 1], d['top'][i + 1], d['width'][i + 1], d['height'][i + 1])
#         # (x2, y2, w2, h2) = (d['left'][i + 2], d['top'][i + 2], d['width'][i + 2], d['height'][i + 2])
#         # cv2.rectangle(img, (x, y), (x1 + w1, y1 + h1), (0, 255, 0), 2)
#         cv2.rectangle(overlay, (x, y), (x1 + w1, y1 + h1), (0, 0, 255), -1)
#         # cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)
#         # cv2.rectangle(overlay, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), -1)
#         # print(text)


    # if '.' in str(text):
    #     print(str(text))
    #     print('***contains full stop***')

        # if(str(text).find('.')):
        #     print('***contains full stop***')
    # else:
    #     i+=1


