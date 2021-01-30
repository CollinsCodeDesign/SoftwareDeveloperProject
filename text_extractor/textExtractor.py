#These commands must be ran in the terminal
#before running this
#sudo apt-get update
#sudo apt-get install tesseract-ocr
#sudo apt-get install libtesseract-dev
import pytesseract
#To install Tools > Manage packages > TYPE: pytesseract > install
print(pytesseract.pytesseract.image_to_string('someText.png'))
