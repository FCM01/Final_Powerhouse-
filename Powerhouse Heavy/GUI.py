import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

import os
import json
from powerhouse_encrypt import Encrptor
from powerhouse_decrypt import Decrptor
from unrar import rarfile

       

def decrypt(data_array, final_text_data, key, tail):
        head, fileName = os.path.split(tail)
        export_data = Decrptor()
        decryptedDataArray = export_data.powerhouse_decrypt(data_array, final_text_data, key,fileName)

        decryptedData = bytearray(decryptedDataArray)
        with open(f"reversed_files/ph_{fileName}", "wb") as outfile:
            outfile.write(decryptedData)
            print("decryption completed")

files = []
def pool_search(key):
    try:
        #checks what files are in the pool
        path_array =[]
        file_names = []
        for directory ,subdirectories,filenames in os.walk("endpool"):
            for files in filenames:
                file_names.append(files)
                paths = os.path.join(directory,files)
                path_array.append(paths)
        print("Array of files>>>:",file_names)
        print("Array of paths>>>:",path_array)

        file_path_finder(path_array,key,"Decrypt")
    except Exception as e:
        print("ERROR-in->pool_serch>>>:", e)
 
def  file_path_finder(path_array,key,password = ""):

  
    try :
     
        print(path_array)
        for file_path in path_array:
            head, tail = os.path.split(file_path)
            if tail.endswith(".rar"):
                print("RAR file to be encrypted")
                final_extract_path = "extract_point"
                try:
                    files=[]
                    with rarfile.RarFile(file_path ,"r",pwd = f"{password}") as rf :
                        files  = rf.namelist()
                        rf.extractall(final_extract_path)
                    print("Files in RAR file >>>:",files)
                    for fls in files :
                        file_path =  fr"{final_extract_path}\{fls}"
                        with open (file_path ,"r") as infile:
                            data = infile.readlines()
                            for line in data:
                                line =line.strip()

                    temp_file = []
                    for directory ,subdirectories,filenames in os.walk(f"{final_extract_path}"):
                        for files in filenames:
                            temp_file.append(files)
                            for file_path in  temp_file:
                                head, tail = os.path.split(file_path)
                                #RAR file files type check 
                                if tail.endswith(".jpg") or tail.endswith(".png") or tail.endswith("jpeg"):
                                    print("Photo to be encrypted") 
                                    file1 = file_path
                                    if file1 is not None:
                                        infile = open (f"{final_extract_path}/{tail}","rb")
                                        image = infile.read()
                                        infile.close()
                                        image = bytearray(image)
                                        print("MODE == ENCRYPT")   
                                        image_data = Encrptor()  
                                        image = image_data.powerhouse(image,key,tail)
                                        reverse_arrays, final_text_data = image
                                        with open(f"endpool/{tail.split('.')[0]}.ph", "w") as outfile:
                                            file_content = json.dumps(
                                                    {
                                                        "reverse_arrays": reverse_arrays,
                                                        "final_text_data": final_text_data,
                                                        "file_name": file_path,
                                                    }
                                                )
                                            outfile.write(file_content)
                                        print("Encrypted file saved")
                        
                                elif tail.endswith(".txt"):
                                    print("Text file to be encrypted")
                                    data_array = []
                                    with open(f"{final_extract_path}/{tail}","r") as fi:
                                        text_file = fi.read()
                                        array = text_file
                                        for values in array:
                                            data_array.append(ord(values))  
                                        print("MODE==ENCRYPT")
                                        export_data= Encrptor()
                                        textfile_data = export_data.powerhouse(data_array,key,tail)
                                        reverse_arrays, final_text_data = textfile_data
                                        with open(f"endpool/{tail.split('.')[0]}.ph", "w") as outfile:
                                            file_content = json.dumps(
                                            {
                                                "reverse_arrays": reverse_arrays,
                                                "final_text_data": final_text_data,
                                                "file_name": file_path,
                                            }
                                            )
                                            outfile.write(file_content)
                                        print("Encrypted file saved")
                                    
                except Exception as e :
                    print("ERROR-in->RAR decompression>>>:", e)

        

            elif tail.endswith(".jpg") or tail.endswith(".png") or tail.endswith(".jpeg"):
                print("Photo to be encrypted") 
                file1 = file_path
                if file1 is not None:
                    infile = open (file1,"rb")
                    image = infile.read()
                    infile.close()
                    image = bytearray(image)
                    print("MODE == ENCRYPT")   
                    image_data = Encrptor()  
                    image = image_data.powerhouse(image,key,tail)
                    reverse_arrays, final_text_data = image
                    with open(f"endpool/{tail.split('.')[0]}.ph", "w") as outfile:
                        file_content = json.dumps(
                                {
                                    "reverse_arrays": reverse_arrays,
                                    "final_text_data": final_text_data,
                                    "file_name": file_path,
                                }
                            )
                        outfile.write(file_content)
                    print("Encrypted file saved")
                    
            
            elif  tail.endswith(".txt"):
                print("Text file to be encrypted")
                data_array = []
                with open(file_path,"r") as fi:
                    text_file = fi.read()
                    array = text_file
                    for values in array:
                        data_array.append(ord(values))
                        print(data_array)   
                    print("MODE==ENCRYPT")
                    export_data= Encrptor()
                    textfile_data = export_data.powerhouse(data_array,key,tail)
                    reverse_arrays, final_text_data = textfile_data
                    with open(f"endpool/{tail.split('.')[0]}.ph", "w") as outfile:
                        file_content = json.dumps(
                        {
                            "reverse_arrays": reverse_arrays,
                            "final_text_data": final_text_data,
                            "file_name": file_path,
                        }
                        )
                        outfile.write(file_content)
                    print("Encrypted file saved")
        # Decryption Area for all files 
            elif tail.endswith(".ph"):
                data_array = []
                with open(file_path,"r") as fi:
                        text_file = fi.read()
                        array = json.loads(text_file)
                        final_text_data =  array["final_text_data"]
                        reverse_arrays =  array["reverse_arrays"]
                        filepath =  array["file_name"]
                        for values in final_text_data:
                            data_array.append(values)
  
                        print("MODE == DECRYPT")
                        decrypt(data_array , reverse_arrays, key, filepath)
                        print("Encrypted file saved")
            
    except Exception as e :
        print(e)

class Mainwindow(QDialog):
    def __init__(self):
        super(Mainwindow, self).__init__()
        loadUi("gui.ui", self)
        self.Browse.clicked.connect(self.browsefiles)
        self.Encrypt.clicked.connect(self.encryptfiles) 
        self.Decrypt.clicked.connect(self.decryptfiles)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'open file')
        self.lstFile.addItem(fname[0])
        files.append(fname[0])
        print (fname)

    def encryptfiles(self):
       

        key = self.filename.text()
        self.filename.setMaxLength(12)
        print(key)
        self.filename.clear()
        
        password = self.rarFile.text()
        self.rarFile.setMaxLength(8)
        print(password)
        self.rarFile.clear()
        print(files)
        if (len(key) ==12):
            self.lstError.clear()
            if ( files != []):
                self.lstError.addItem("Processing....")
                file_path_finder(files,key,password)
                self.lstError.addItem("File has been encrypted")      
            else:
                self.lstError.addItem("Please select a file to be encrypted")        
        else :
            self.lstError.addItem("Incorrect key must be length 12")
        

    def decryptfiles(self):
        self.lstError.addItem("Bye World")

        key = self.filename.text()
        self.filename.setMaxLength(12)
        print(key)
        self.filename.clear()
        
        if (len(key) ==12):
            self.lstError.clear()
            self.lstError.addItem("Processing....")
            pool_search(key) 
            self.lstError.addItem("File has been encrypted")

        else :
            self.lstError.addItem("Incorrect key must be length 12")
      

app = QApplication(sys.argv)
mainwindow = Mainwindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(563)
widget.setFixedHeight(573)
widget.setWindowTitle("Powerhouse")
widget.show()
app.exec_()
sys.exit()