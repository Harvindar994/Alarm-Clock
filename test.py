import cv2

#  Loading Video.
video = cv2.VideoCapture('video.mov', cv2.CAP_DSHOW)

while True:
    read_or_not, frame = video.read()
    frame = frame.crop((1, 1, 98, 33))
    # converting into gray scale.
    # grayscaled_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # face_coord = trained_face_data.detectMultiScale(grayscaled_image)
    # for coord in face_coord:
    #     x, y, width, height = coord
    #     cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 1)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)
    if key == 113 or key==81:
        break

video.release()