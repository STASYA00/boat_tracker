# import cv2  # remove later

# def drawPredictions(frame, preds):
#     for i, newbox in enumerate(preds):
#         # box is [x,y,w,h]
#         p1 = (int(newbox[0]), int(newbox[1]))
#         p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
#         cv2.rectangle(frame, p1, p2, [0,0,0], 2, 1)


# def checkPosition(xyxy):
#     # reintegrate later
#     p = (360 - xyxy[0]) / (xyxy[2] - xyxy[0])
#     return p < 0.3