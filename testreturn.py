import cv2 as cv
img = cv.imread("assets/images/icons/IOMedGrey-16px.png", cv.IMREAD_GRAYSCALE)
x = cv.spatialGradient(img)

print(type(x[1]))
