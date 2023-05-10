import sys
import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PIL import Image

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 600, 370))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setScaledContents(True)  # Escala la imagen al tamaño del QLabel sin deformarla
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.uploadButton.setGeometry(QtCore.QRect(20, 400, 110, 31))
        self.uploadButton.setObjectName("uploadButton")
        self.generateButton = QtWidgets.QPushButton(self.centralwidget)
        self.generateButton.setGeometry(QtCore.QRect(120, 400, 130, 31))
        self.generateButton.setObjectName("generateButton")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(240, 400, 110, 31))
        self.exitButton.setObjectName("exitButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect buttons to functions
        self.uploadButton.clicked.connect(self.select_image)
        self.generateButton.clicked.connect(self.generate_nc)
        self.exitButton.clicked.connect(self.exit_application)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.uploadButton.setText(_translate("MainWindow", "Subir Imagen"))
        self.generateButton.setText(_translate("MainWindow", "Procesar imagen"))
        self.exitButton.setText(_translate("MainWindow", "Salir"))

    def select_image(self):
        # Open file dialog to select image file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png)")
        file_dialog.setDefaultSuffix("png")
        file_name, _ = file_dialog.getOpenFileName(None, "Seleccionar imagen", "", "Images (*.png)")
            
        # If a file was selected, display it in the label
        if file_name:
            pixmap = QtGui.QPixmap(file_name)
            self.label.setPixmap(pixmap)
            self.image_path = file_name
            self.label.setScaledContents(True)
        else:
            self.image_path = None

    
    def generate_nc(self):
        # Check if an image has been uploaded
        if not hasattr(self, "image_path"):
            self.show_error_message("Debe subir una imagen antes de procesar la imagen")
            return

        # Open file dialog to select output directory
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        # file_path = file_dialog.getExistingDirectory(None, "Seleccionar carpeta de salida")
        # file_path = os.path.dirname(self.image_path)
        file_path = "/Users/david/Desktop/CNC"


        # If a directory was selected, generate the .nc file
        if file_path:
            # Load image and convert it to black and white
            image = Image.open(self.image_path).convert("L")

            # Convert image to numpy array
            image_array = np.array(image)

            # Save image as text file
            file_name = os.path.basename(self.image_path)
            np.savetxt(os.path.join(file_path, file_name + ".txt"), image_array, fmt="%d")

            # Rename text file to .nc
            os.rename(os.path.join(file_path, file_name + ".txt"), os.path.join(file_path, file_name + ".nc"))

            # Show success message
            self.show_message("Comenzando grabación")

    def exit_application(self):
        # Show confirmation message before closing application
        result = QMessageBox.question(None, "Salir", "¿Está seguro que desea salir de la aplicación?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            sys.exit()

    def show_message(self, message):
        QMessageBox.information(None, "Mensaje", message, QMessageBox.Ok)

    def show_error_message(self, message):
        QMessageBox.warning(None, "Error", message, QMessageBox.Ok)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
