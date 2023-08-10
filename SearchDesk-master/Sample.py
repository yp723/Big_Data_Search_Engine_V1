import time
import os
import cv2
import pytesseract
import re
import fitz
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def searchtext(keyword):
    time1 = time.time()
    root = 'D:\\db'
    links = {}
    filenames = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            filenames.append(os.path.join(path, name))
    for file_name in filenames:
        if ".txt" in file_name:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = f.read().casefold()
                words = keyword.casefold().split()
                for w in words:
                    if w in data:
                        Count = data.count(w)
                        links[file_name] = Count
    for file_name in filenames:
        if (".doc" in file_name or ".docx" in file_name):
            with open(file_name, 'r', encoding='ISO-8859-1') as f:
                data = f.read().casefold()
                words = keyword.casefold().split()
                for w in words:
                    if w in data:
                        Count = data.count(w)
                        links[file_name] = Count
    for file_name in filenames:
        if ".png" in file_name or ".jfif" in file_name:
            img = cv2.imread(file_name)
            custom_config = r'--oem 3 --psm 6'
            data = pytesseract.image_to_string(img, config=custom_config).casefold()
            words = keyword.casefold().split()
            for w in words:
                if w in data:
                    Count = data.count(w)
                    links[file_name] = Count
    for file_name in filenames:
        if (".pdf" in file_name):
            pdfDoc = fitz.open(file_name)
            Count = 0
            for pg in range(pdfDoc.page_count):
                page = pdfDoc[pg]
                lines = page.get_text("text").split('\n')
                words = keyword.split()
                for w in words:
                    for line in lines:
                        w1 = w.casefold()
                        line1 = line.casefold()
                        if re.findall(w1, line1):
                            Count += line1.count(w1)
            if Count != 0:
                links[file_name] = Count
    time2 = time.time()
    print("Total Time Taken: ", time2 - time1)
    return links