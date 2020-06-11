import cv2
import os
import possibleChars

MIN_PIXEL_WIDTH = 1
MIN_PIXEL_HEIGHT = 10

MIN_ASPECT_RATIO = 0.1
MAX_ASPECT_RATIO = 0.9

MIN_PIXEL_AREA = 63

MAX_CHANGE_IN_AREA = 0.5

MIN_CONTOUR_AREA = 20


def check_if_char(possibleChar):
    if (possibleChar.int_rect_area > MIN_PIXEL_AREA
        and possibleChar.int_rect_w > MIN_PIXEL_WIDTH
        and possibleChar.int_rect_h > MIN_PIXEL_HEIGHT
        and MIN_ASPECT_RATIO < possibleChar.flt_aspect_ratio
            and possibleChar.flt_aspect_ratio < MAX_ASPECT_RATIO):
        return True
    else:
        return False


path = 'plate_car'
for image in os.listdir(path):
    label = image[9:17]
    path_image = path + '/' + image
    img = cv2.imread(path_image, 0)
    # img_blurred = cv2.GaussianBlur(
    #     img, (3, 3), 0)
    # binary = cv2.adaptiveThreshold(img_blurred, 255.0,
    #                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                cv2.THRESH_BINARY_INV,
    #                                3,
    #                                1)
    # binary = cv2.threshold(img, 100, 255,
    #                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.rectangle(binary, (0, 0), (
    #     img_blurred.shape[1],
    #     img_blurred.shape[0]),
    #     (0, 0, 0), 3)
    # contours, _ = cv2.findContours(
    #     binary, cv2.RETR_EXTERNAL,
    #     cv2.CHAIN_APPROX_SIMPLE)
    # fill_cotours = []
    # count = 0
    # for contour in contours:
    #     possibleChar = possibleChars.PossibleChar(contour)
    #     if check_if_char(possibleChar):
    #         count += 1
    #         continue
    #     fill_cotours.append(contour)
    # print(count)
    # cv2.drawContours(binary, fill_cotours, -1, (0, 0, 0))
    write_path = os.path.join('data', 'plate-ground-truth', image)
    cv2.imwrite(write_path[:-4] + '.tif', img)
    file1 = open(write_path[:-4] + ".gt.txt", "w")
    file1.write(str(label))
    file1.close()
