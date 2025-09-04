import cv2
import pytesseract
import os
from pdf2image import convert_from_path

# Poppler path (bin folder ka exact path yaha dalna)
TEMP_FILE_PATH = "temp/temp_upload.pdf"
POPPLER_PATH = r"C:\Users\amank\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin" 

if not os.path.exists(TEMP_FILE_PATH):
    print(" No uploaded file found! Please upload first.")
else:
    file_ext = os.path.splitext(TEMP_FILE_PATH)[1].lower()

    extracted_text = ""

    if file_ext == ".pdf":
        #  Poppler path pass karna zaroori hai
        pages = convert_from_path(TEMP_FILE_PATH, dpi=300, poppler_path=POPPLER_PATH)
        for i, page in enumerate(pages):
            temp_img_path = os.path.join("temp", f"page_{i+1}.png")
            page.save(temp_img_path, "PNG")

            # Image read for OCR
            image = cv2.imread(temp_img_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            text = pytesseract.image_to_string(gray, lang="eng")
            extracted_text += f"\n--- Page {i+1} ---\n\n{text}"

    elif file_ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        # Direct image read
        image = cv2.imread(TEMP_FILE_PATH)
        if image is None:
            print(" Could not load the image. Check path or format.")
            exit()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        extracted_text = pytesseract.image_to_string(gray, lang="eng")

    else:
        print(" Unsupported file type! Please upload PDF or image.")
        exit()

    # Output
    print(" Extracted Text:")
    print(extracted_text)





