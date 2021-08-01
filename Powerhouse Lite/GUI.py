import sys
import os 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


from powerhouse_encrypt import Encrptor
from powerhouse_decrypt import Decrptor
import json

class Mainwindow(QDialog):
    def __init__(self):
        super(Mainwindow, self).__init__()
        loadUi("gui.ui", self)
        self.files = []
        self.Encrypt.clicked.connect(self.encryptfiles) 
        self.Decrypt.clicked.connect(self.decryptfiles)
    def encrypt(self, filePath, key):
        fileDataArray = []
        head, fileName = os.path.split(filePath)
        file = open(filePath, "rb")
        fileData = file.read()
        file.close()
        fileDataArray = bytearray(fileData)
        print("[head] -> ", head)
        print("[fileName] -> ", fileName.split("."))
        # print("[fileDataArray] -> ", fileDataArray)
        export_data = Encrptor()
        encryptedData = export_data.powerhouse(fileDataArray, key, fileName)
        reverse_arrays, final_text_data = encryptedData
        with open(f"endpool/{fileName.split('.')[0]}.ph", "w") as outfile:
            file_content = json.dumps(
                {
                    "reverse_arrays": reverse_arrays,
                    "final_text_data": final_text_data,
                    "file_name": fileName,
                }
            )
            outfile.write(file_content)
            print("encryption completed")

    def encryptfiles(self):
        fname = QFileDialog.getOpenFileName(self, 'open file')
        self.lstFile.addItem(fname[0])
        self.files = []
        self.files.append(fname[0])
        print (fname)
        key = self.filename.text()
        self.filename.setMaxLength(12)
        if (len(key) ==12):
            self.lstError.clear()
            if (self.files != []):
                self.lstError.addItem("Processing....")
                self.encrypt(self.files[0], key)
                self.lstError.addItem("Please end program a locate your file (eg: original final.ph) in endpool")
                self.lstError.addItem("File has been Encrypted")      
            else:
                self.lstError.addItem("Please select a file to be Encrypted")        
        else :
            self.lstError.addItem("Incorrect key must be length 12")
        
       

        self.filename.clear()

    def decrypt(self, filePath, data_array, final_text_data, key, tail):
        head, fileName = os.path.split(filePath)
        export_data = Decrptor()
        decryptedDataArray = export_data.powerhouse_reverse(
            data_array, final_text_data, key, tail
        )

        decryptedData = bytearray(decryptedDataArray)
        with open(f"{head}/ph_{tail}", "wb") as outfile:
            outfile.write(decryptedData)
            print("decryption completed")   

    def decryptfiles(self):
        fname = QFileDialog.getOpenFileName(self, 'open file')
        self.lstFile.addItem(fname[0])
        self.files.append(fname[0])
        print (fname)
        key = self.filename.text()
        self.filename.setMaxLength(12)
        if (len(key) ==12):
            self.lstError.clear()
            if (self.files != []):
                self.lstError.addItem("Processing....")
                with open(self.files[0], "r") as file1:
                    text_file = file1.read()
                    data = json.loads(text_file)
                    final_text_data = data["final_text_data"]
                    reverse_arrays = data["reverse_arrays"]
                    file_name = data["file_name"]
                    self.decrypt(self.files[0], final_text_data, reverse_arrays, key, file_name)
                    key = self.filename.clear()
                self.lstError.addItem("File has been Decrypted") 

                self.filename.clear()     
            else:
                self.lstError.addItem("Please select a file to be Decrypted")        
        else :
            self.lstError.addItem("Incorrect key must be length 12")
        

app = QApplication(sys.argv)
mainwindow = Mainwindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(563)
widget.setFixedHeight(552)
widget.setWindowTitle("Powerhouse")
widget.show()
app.exec_()
sys.exit() 