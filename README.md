## Task Breakdown

1. Detect all the boats
2. Trace the boats (knowing that boat has already been counted)
3. Make sure boats don't repeat (falling into the camera twice from different sides)


## actions

1. see how different frameworks perform for object detection
2. try yolo that tracks the objects as well
3. get the coordinates from mp4
4. estimate boat positions with respect to the camera
5. make sure they dont repeat / another similarity check
6. assure it works real time
7. docker container
8. good code structure

### Assumptions

1. There are no competitor boats going around and counting the boats, thus increasing the count (unreasonably)
2. Neglect the height of the camera over the boat level when calculating the distance to the other boats
3. Assume that field of view is 45 degrees
4. Neglect camera's rotation around the X-axis (the camera is slightly rotated as the horizon is over the middle of the matrix, but it can be neglected in the calculations we make)
5. 