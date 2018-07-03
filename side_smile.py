# -*- coding: utf-8 -*-

import cv2
import glob
import os
import sys
from datetime import datetime
from face_square_clips import face_square_clips
from dir_exists import dir_exists
class Detection:
    """横側からの笑顔を検出する"""
    """自作検出器による"""
    def __init__(self, path = "./201804280930/",cascade = "cascade/0629_neo/cascade.xml"):
        self.path_img = path
        self.file_lists = glob.glob(self.path_img + "img/*.jpg")
        self.p_list = self.path_img + "positive.dat"
        self.n_list = self.path_img + "negative.dat"
        self.cascade = cv2.CascadeClassifier(path + cascade)
        self.filepath_list = dir_exists(path, str(datetime.now().date()))

        # Positive数読み込み
        self.P_s= sum(1 for line in open(self.p_list))
        self.P_f = open(self.p_list, 'r')
        self.P_l = self.P_f.readlines()
        # Negative数読み込み
        self.N_s = sum(1 for line in open(self.n_list))
        self.N_f = open(self.n_list, "r")
        self.N_l = self.N_f.readlines()

    def check_detection_sideface(self):
        """検出が正しいのか確認を行う関数"""
        P_P = 0
        P_N = 0
        N_P = 0
        N_N = 0
        exc = 0
        for file_list in self.file_lists:
            flg, img, img_file_name = face_square_clips(self.cascade, file_list)
            P_in = [s for s in self.P_l if img_file_name in s]
            if len(P_in) != 0:
                if flg == True:
                    P_P += 1
                    cv2.imwrite(self.filepath_list[0] + "/" + img_file_name + ".jpg", img)
                else:
                    P_N += 1
                    cv2.imwrite(self.filepath_list[1] + "/" + img_file_name + ".jpg", img)
            else:
                N_in = [s for s in self.N_l if img_file_name in s]
                if len(N_in) != 0:
                    if flg == True:
                        N_P += 1
                        img = cv2.imread(file_list, cv2.IMREAD_COLOR)
                        cv2.imwrite(self.filepath_list[2] + "/" + img_file_name + ".jpg", img)
                    else:
                        N_N += 1
                else:
                    exc += 1
        result_d = {"ALL": len(self.file_lists), "P_s": self.P_s, "N_s": self.N_s, "P_P": P_P, "P_N": P_N, "N_P": N_P, "N_N": N_N, "EXC": exc}
        for key, value in result_d.items():
            print("key:", key, "-- value:", str(value))


if __name__ == "__main__":
    arg = sys.argv

    if len(arg) == 1 :
        sideface = Detection()
        sideface.check_detection_sideface()

    else:
        if len(arg) == 3:
            if arg[1] == "flont":
                frontalface = Detection(arg[2], "./haarcascades/haarcascade_frontalface_default.xml")
                frontalface.check_detection_sideface()
            elif arg[1] == "flontsmile":
                frontalsmile = Detection(arg[2], "./haarcascades/haarcascades_smile.xml")
                frontalsmile.check_detection_sideface()
