import os
from keras.models import load_model
from PIL import Image, ImageOps #Install pillow instead of PIL
import numpy as np

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton,QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model('./keras_Model.h5', compile=False)

# Load the labels
class_names = open('./labels.txt', 'r').readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

form_class = uic.loadUiType("./keras.ui")[0]

class MainClass(QMainWindow, form_class):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)

        self.btnImgLoad.clicked.connect(self.imgLoad)

        self.show()

    def imgLoad(self):
        fname = QFileDialog.getOpenFileName(self,'Open File','','All File(*);; Image File(*.png *.jpg *.gif)')

        if fname[0]:
            pixmap = QPixmap(fname[0])

            self.tblImgView.setPixMap(pixmap)

            self.tblImgView.resize(pixmap.width(),pixmap.height())


            # Replace this with the path to your image
            image = Image.open(fname[0]).convert('RGB')

            #resize the image to a 224x224 with the same strategy as in TM2:
            #resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

            #turn the image into a numpy array
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

            # Load the image into the array
            data[0] = normalized_image_array

            # run the inference
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            print('Class:', class_name, end='')
            print('Confidence score:', confidence_score)

            self.tblPredict.setText('예측 결과 :'+class_name)
        else:
            QMessageBox.about(self,'파일 없음','파일을 선택하지 않았습니다')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainClass()
    app.exec_()




