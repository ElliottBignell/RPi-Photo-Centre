import cv2

camera = cv2.VideoCapture(0)

while True:
    return_value,image = camera.read()
    cv2.imshow('image',image)
    if cv2.waitKey(1)& 0xFF == ord('s'):
        break
    cv2.imwrite('./test.jpg',image)
camera.release()
cv2.destroyAllWindows()
