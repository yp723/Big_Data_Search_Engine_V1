import aspose.words as aw
def Converter(link):
    if ".docx" in link or ".doc" in link:
        doc = aw.Document(link)
        doc.save(link+".pdf")