import os
import cv2
import copy


def extract_letters(image_name):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path_img = os.path.join(current_dir, "..", "images", image_name)

    dist_path = os.path.join(current_dir, "./letters")

    im = cv2.imread(path_img)
    im_copy = copy.copy(im)

    def setTresh(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_ISOLATED)
        blur2 = cv2.GaussianBlur(blur1, (5, 5), cv2.BORDER_ISOLATED)
        blur3 = cv2.GaussianBlur(blur2, (5, 5), cv2.BORDER_ISOLATED)
        return cv2.adaptiveThreshold(blur3, 255, 1, 1, 13, 2)

    contours, _ = cv2.findContours(
        setTresh(im), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    def detection(x, y, w, h):
        for cnt in contours:
            if cv2.contourArea(cnt) > 0:
                for i in range(w):
                    if cv2.pointPolygonTest(cnt, (x+i, y), False) > 0 or cv2.pointPolygonTest(cnt, (x+i, y+h), False) > 0:
                        return True
        return False

    def union(a, b):
        x = min(a[0], b[0])
        y = min(a[1], b[1])
        w = max(a[0]+a[2], b[0]+b[2]) - x
        h = max(a[1]+a[3], b[1]+b[3]) - y
        return [x, y, w, h]

    def fusion_i(x, y, w, h):
        for cnt in contours:
            if cv2.contourArea(cnt) > 0:
                for i in range(w+8):
                    if cv2.pointPolygonTest(cnt, (x+w+8-i, y+h+50), False) > 0:
                        [x1, y1, w1, h1] = union(
                            cv2.boundingRect(cnt), [x, y, w, h])
                        cv2.rectangle(im_copy, (x1, y1),
                                      (x1+w1, y1+h1), (0, 0, 0), 2)
                        return [x1, y1, w1, h1]
        return False

    mylist = []

    for cnt in contours:
        if cv2.contourArea(cnt) > 0:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if detection(x, y, w, h) != True:
                if h < 16:
                    if fusion_i(x, y, w, h) != False:
                        contours, _ = cv2.findContours(
                            setTresh(im_copy), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 0:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if detection(x, y, w, h) != True:
                mylist.append([x, y, w, h])

    sorted_list = sorted(mylist, key=lambda x: x[0])

    for elem, i in zip(sorted_list, range(len(sorted_list))):
        roi = setTresh(im)[elem[1]:elem[1]+elem[3], elem[0]:elem[0]+elem[2]]
        roismall = cv2.resize(roi, (28, 28))
        if not os.path.exists(dist_path):
            os.makedirs(dist_path)
        cv2.imwrite(f'{dist_path}/{i}.jpg', roismall)
