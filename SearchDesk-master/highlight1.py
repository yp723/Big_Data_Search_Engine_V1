import time
import os
import cv2
import pytesseract
import re
import fitz
from ConvertDOCX2PDF import Converter
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def highlight(keyword, link):
    time1 = time.time()
    if ".txt" in link:
        with open(link, 'r', encoding='utf-8') as f:
            data = f.read().casefold()
            words = keyword.casefold().split()
            for w in words:
                if w in data:
                    with open("D:/Dataset/Cache/" + link[11:] + '.html', mode='wt', encoding='utf-8') as file:
                        file.write(data.replace(w, '<span><mark>{}</mark></span>'.format(w)))
    elif ".png" in link or ".jfif" in link:
        img = cv2.imread(link)
        custom_config = r'--oem 3 --psm 6'
        data = pytesseract.image_to_string(img, config=custom_config).casefold()
        words = keyword.casefold().split()
        for w in words:
            if w in data:
                with open("D:/Dataset/Cache/" + link[11:] + '.html', mode='wt', encoding='utf-8') as file:
                    file.write(data.replace(w, '<span><mark>{}</mark></span>'.format(w)))
    elif ".pdf" in link:
        with open("D:/Dataset/Cache/" + link[11:] + '.html', mode='wt', encoding='utf-8') as f:
            Count = 0
            pdfDoc = fitz.open(link)
            for pg in range(pdfDoc.page_count):
                page = pdfDoc[pg]
                lines = page.get_text("text").split('\n')
                words = keyword.split()
                for w in words:
                    for line in lines:
                        w1 = w.casefold()
                        line1 = line.casefold()
                        long = 'created with an evaluation copy of aspose.words.'
                        if long in line1 or line1 == 'please visit: https://products.aspose.com/words/' or line1 == 'evaluation only. created with aspose.words. copyright 2003-2022 aspose pty ltd.':
                            continue
                        elif re.findall(w1, line1):
                            Count += line1.count(w1)
                        f.write(line1.replace(w, '<span><mark>{}</mark></span>'.format(w)))
    elif ".doc" in link or ".docx" in link:
        Converter(link)
        link = link + ".pdf"
        highlight(keyword, link)
        if ".docx.pdf" in link or ".doc.pdf" in link:
            os.remove(link)
        pass
    time2 = time.time()
    print("Total Time Taken: ", time2 - time1)
    htmllink = link+'.html'
    return htmllink