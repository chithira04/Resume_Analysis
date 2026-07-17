import PyPDF2


def extract_text(pdf_path):

    text = ""

    reader = PyPDF2.PdfReader(pdf_path)

    for page in reader.pages:
        text += page.extract_text()

    return text