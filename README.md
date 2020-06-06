# OCR-To-Get-Data-in-Structured-Format
 Tesseract ocr + OpenCv + PIL + Python
  
# Download the following -:
1. sudo apt-get install tesseract-ocr
2. pip install pytesseract
3. pip install pdf2image
4. pip install opencv-python
5. pip install subprocess.run
6. pip install pandas

# Instruction
  -: This code is specifically for fetching a Text from PDF, All you need to do is to pass path  while executing the Script.
  
  -: As a Result, You will have Images of PDF file and .TXT file.


# For Example
    -> If your PDF has 5 pages, you will get 5 Images(It will tell you which data I am using in my Script) and 5 .TXT files.

# Run 
your_pdf_path = "../x.pdf"

path_to_save ="../My_project/"

python OCR.py  "your_pdf_path" "path_to_save"

# Add-On
sudo apt-get install imagemagick

python OCR.py "PathToYourImg/img.jpeg" "PathToSaveImg/img1.jpeg"  1

     -- This script will remove all Lines from Image --

