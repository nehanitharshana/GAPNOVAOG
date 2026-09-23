import pymupdf


def extract_text_from_pdf(uploaded_file):
    pdf_document = pymupdf.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text