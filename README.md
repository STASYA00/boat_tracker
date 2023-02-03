## Task Breakdown

1. Detect all the boats
2. Trace the boats (knowing that boat has already been counted)
3. Make sure boats don't repeat (falling into the camera twice from different sides)


## actions

1. [+] see how different frameworks perform for object detection
1.1 document it
2. [x] try yolo that tracks the objects as well
2.1 rewrite yolov7 to be callable?
2.2 rewrite deepsort?
2.3 implement simple tracking algorithms to be runnable (cv2.legacy issue)

3. [-] get the coordinates from mp4
4. [-] estimate boat positions with respect to the camera
5. [-] make sure they dont repeat / another similarity check
6. [+] assure it works real time
7. docker container
8. good code structure
9. final video

### Assumptions

1. There are no competitor boats going around and counting the boats, thus increasing the count (unreasonably)
2. Neglect the height of the camera over the boat level when calculating the distance to the other boats
3. Assume that field of view is 45 degrees
4. Neglect camera's rotation around the X-axis (the camera is slightly rotated as the horizon is over the middle of the matrix, but it can be neglected in the calculations we make)
5. 

### Future work

Some boats in the video are counted twice due to their position: <illustration>
The guy participating in the competition is smart and probably knows that most of the existing tracking algorithms would not 
be able to tell that it is the exact same boat, just seen from different angles with a large gap in time. The extension of
this work would be to track the positions of the boats on the map with respect to the camera trajectory and check whether
the detected boat was potentially tracked before. <illustration> In a simplified form it would not even need the camera characteristics.