from PyQt5 import QtWidgets, QtGui, QtCore

from UI import Ui_MainWindow

import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import os
import sys
import re


class MainWindow_controller(QtWidgets.QMainWindow):

    # img1 = cv2.imread('Dataset_OpenCvDl_Hw1\Q1_Image\Sun.jpg')

    image = []
    path = "Q2_Image/"
    dirs = os.listdir(path)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.pushButton.clicked.connect(self.showCorner)
        self.ui.pushButton_2.clicked.connect(self.Intrinsic)
        self.ui.pushButton_5.clicked.connect(self.Extrinsic)
        self.ui.pushButton_3.clicked.connect(self.Distortion)
        self.ui.pushButton_4.clicked.connect(self.Result)

    def findCorner(self, img):
        temp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(temp,
                                                 (11, 8))
        cv2.cornerSubPix(temp, corners, (11, 11), (-1, -1),
                         (cv2.TermCriteria_MAX_ITER+cv2.TERM_CRITERIA_EPS,
                          40,
                          0.1))
        return ret, corners

    def showCorner(self):
        path = "Q2_Image/"
        dirs = os.listdir(path)
        for file in dirs:
            img = cv2.imread(path + file)
            ret, corners = self.findCorner(img)
            cv2.drawChessboardCorners(img, (11, 8), corners, ret)
            img = cv2.resize(img, (800, 800),
                             interpolation=cv2.INTER_AREA)
            cv2.imshow('image', img)
            # pauses for 3 seconds before fetching next image
            cv2.waitKey(500)

    def Intrinsic(self):
        objp = np.zeros((11*8, 3), np.float32)
        objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2)
        objpoints = []
        imgpoints = []
        path = "Q2_Image/"
        dirs = os.listdir(path)

        for file in dirs:
            img = cv2.imread(path + file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = self.findCorner(img)
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

        # calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)
        print("Intrinsic:")
        print(mtx)

    def Extrinsic(self):
        text = self.ui.lineEdit.text()
        objp = np.zeros((11*8, 3), np.float32)
        objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2)
        objpoints = []
        imgpoints = []
        path = "Q2_Image/"
        dirs = os.listdir(path)

        for file in dirs:
            img = cv2.imread(path + file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = self.findCorner(img)
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

        # calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)

        # print(tvecs[int(text)-1])
        img = cv2.imread(path + text + ".bmp")
        Rvecs = np.zeros((3, 3))
        cv2.Rodrigues(rvecs[int(text)-1], Rvecs, jacobian=0)
        extrinsic = np.hstack([Rvecs, tvecs[int(text)-1]])
        print("Extrinsic: ")
        print(extrinsic)

    def Distortion(self):
        objp = np.zeros((11*8, 3), np.float32)
        objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2)
        objpoints = []
        imgpoints = []
        path = "Q2_Image/"
        dirs = os.listdir(path)

        for file in dirs:
            img = cv2.imread(path + file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = self.findCorner(img)
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

        # calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)
        print("Distortion:")
        print(dist)

    def Result(self):
        objp = np.zeros((11*8, 3), np.float32)
        objp[:, :2] = np.mgrid[0:11, 0:8].T.reshape(-1, 2)
        objpoints = []
        imgpoints = []
        path = "Q2_Image/"
        dirs = os.listdir(path)

        for file in dirs:
            img = cv2.imread(path + file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = self.findCorner(img)
            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)

        # calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)

        for file in dirs:
            img = cv2.imread(path + file)
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
                mtx, dist, (11, 8), 1, (11, 8))
            # undistort
            dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
            img = cv2.resize(img, (800, 800),
                             interpolation=cv2.INTER_AREA)
            dst = cv2.resize(img, (800, 800),
                             interpolation=cv2.INTER_AREA)
            CompareImg = np.hstack([img, dst])
            cv2.imshow("compare", CompareImg)
            cv2.waitKey(500)
