import pytesseract
import cv2
import argparse
import os
from sklearn import metrics

find_char = False
get_accuracy = False

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",
                help="Path to the plate image")
ap.add_argument("-f", "--folder", default=None,
                help="Path to the folder plate images")
args = vars(ap.parse_args())
if args['image'] is not None:
    find_char = True
    if not os.path.exists(args['image']):
        print("The image path doesn't exist!")
        find_char = False
if args['folder'] is not None:
    get_accuracy = True
    if not os.path.exists(args['folder']):
        print("The folder path doesn't exist!")
        get_accuracy = False
args = vars(ap.parse_args())

# Dinh nghia cac ky tu tren bien so
char_list = '0123456789ABCDEFGHKLMNPRSTUVXYZ'

# Ham fine tune bien so, loai bo cac ki tu khong hop ly


def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString


def main():
    if find_char:
        img = cv2.imread(args['image'], 0)
        # img_blurred = cv2.GaussianBlur(
        #     img, (3, 3), 0)
        # binary = cv2.adaptiveThreshold(img_blurred, 255.0,
        #                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                cv2.THRESH_BINARY_INV,
        #                                3,
        #                                1)
        # contours, _ = cv2.findContours(
        #     binary, cv2.RETR_EXTERNAL,
        #     cv2.CHAIN_APPROX_SIMPLE)
        # fill_cotours = []
        # for contour in contours:
        #     possibleChar = possibleChars.PossibleChar(contour)
        #     if check_if_char(possibleChar):
        #         continue
        #     fill_cotours.append(contour)
        # cv2.drawContours(binary, fill_cotours, -1, (0, 0, 0))
        text = pytesseract.image_to_string(
            img, lang="plate0.025_3326", config="--psm 8")
        str_plate = fine_tune(text)
        print(str_plate)
    elif get_accuracy:
        count_images = 0
        count_true_plate = 0
        count_chars = 0
        count_true = 0
        str_plates = []
        labels = []
        for image in os.listdir(args['folder']):
            count_images += 1
            label = image[9:17]
            labels += label
            pathImage = args['folder'] + "/" + image
            img = cv2.imread(pathImage, 0)
            # img_blurred = cv2.GaussianBlur(
            #     img, (3, 3), 0)
            # binary = cv2.adaptiveThreshold(img_blurred, 255.0,
            #                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            #                                cv2.THRESH_BINARY_INV,
            #                                3,
            #                                1)
            text = pytesseract.image_to_string(
                img, lang="plate0.025_3326", config="--psm 8")
            str_plate = fine_tune(text)
            if len(str_plate) < len(label):
                for i in range(0, len(label) - len(str_plate)):
                    str_plate = str_plate + '0'
            str_plates += str_plate
            for i in range(0, len(label)):
                count_chars += 1
                if label[i] == str_plate[i]:
                    count_true += 1
            if (label == str_plate):
                count_true_plate += 1
            else:
                print(label)
                print(str_plate + "\n")
        confusion_matrix = metrics.confusion_matrix(labels, str_plates)
        print("Total chars: " + str(count_chars) + "\n")
        print("True chars: " + str(count_true) + "\n")
        print("Accuracy chars: " + str(float(count_true/count_chars)) + "\n")
        print("Accuracy plate: " + str(float(count_true_plate/count_images)))
        print("confusion matrix: \n{}".format(confusion_matrix))
        report = metrics.classification_report(labels, str_plates)
        print(report)
    else:
        print("Nothing to do, pass args to do some thing!")
    return


if __name__ == '__main__':
    main()
