<!-- Improved compatibility of back to top link: See: https://github.com/STASYA00/boat_tracker/pull/73 -->
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/STASYA00/boat_tracker">
    <img src="assets/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center" Boat Tracker </h3>

  <p align="center">
    Track the boats!
    <br />
    <a href="https://github.com/STASYA00/boat_tracker">View Demo</a>
    ·
    <a href="https://github.com/STASYA00/boat_tracker/issues">Report Bug</a>
    ·
    <a href="https://github.com/STASYA00/boat_tracker/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#design">Design</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <ul>
        <li><a href="#challenges">Challenges</a></li>
        <li><a href="#futurework">Future work</a></li>
    </ul>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


https://user-images.githubusercontent.com/30144984/216849013-6fe10463-b513-4231-aa69-81f21d8ab5cc.mp4


This is an application to track and count boats with a moving camera.

#### Some assumptions

1. There are no competitor boats going around and counting the boats, thus increasing the count (unreasonably)
2. The trajectory of the boat is more or less straight and other boats do not move around entering in the camera view from unexpected sides. Let's say one example that would not work here is camera following a spiral trajectory, so a boat can potentially be counted on each loop as a new boat.
3. The lower part of the image will not contain any boats (except for the boat the camera is placed on) due to the specifics of the situation. This area in the camera view covers approximately 1 m distance from the boat which is unlikely to be entered by any other boat. Moreover, if a boat partially enters this area, there is an extremely low chance that this boat was not in the fov earlier or will not be there later on.



<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With


* [python](https://www.python.org/)
* [torch](https://pytorch.org/)
* [openCV](https://opencv.org/)
* [Docker](https://docs.docker.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites


* Docker
  install [Docker](https://docs.docker.com/get-docker/)
* with conda or venv: create a new environment
```sh
conda create -n py3
```
```sh
conda activate py3
```

* to run with GPU install CUDA Toolkit and follow the instruction on configuring the environment
to run torch with CUDA
### Installation

* with Docker
  ```sh
  docker build . -t name:tag
  ```
  ```sh
  docker run -dit --name NAME name:tag
  ```
* alternatively
1. Clone the repo
   ```sh
   git clone https://github.com/STASYA00/boat_tracker.git
   ```
3. Install pip packages
   ```sh
   pip install -r requirements.txt
   ```
4. run the code
   ```sh
   cd boat_tracker/src
   python main.py --source VIDEO.mp4
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

In case you ever need to count boats on a video (or other objects as well, which will be supported later on), use this application on it!


https://user-images.githubusercontent.com/30144984/216849201-4ac91c37-8f5f-4a28-be91-b5377a2d3314.mp4



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DESIGN -->
## Design

The objective of this app was to count all the different boats in the video.
This task can be broken down into the following parts:

+ Detecting the boats
+ Identifying the boats across the frames (tracking)
+ doing it fast

Since the speed was the main constraint, the model chosen for the object detection part was Yolo. It has [higher
inference speed](https://jonathan-hui.medium.com/object-detection-speed-and-accuracy-comparison-faster-r-cnn-r-fcn-ssd-and-yolo-5425656ae359) due to its architecture (you only look once, right?) even though other models can be slightly more accurate. In this case the accuracy was not the main objective. Comparing different versions of Yolo for this problem it turned out that Yolov5l gives the best speed with acceptable accuracy. Yolov7 [showed](https://learnopencv.com/performance-comparison-of-yolo-models/) to be even faster and more accurate, one of the future steps would be using its detections for boat tracking. It was tested applied to the current problem as well and the performance is better with respect to the other models. The models were evaluated on a very small subset of frames with manual annotation of the number of boats that were supposed to be seen. The idea is to enlarge the subset and make a more thorough comparison. 
Moreover, the model is fairly compact and can potentially be implemented on an edge device if needed.

Second part involved tracking the objects across different frames. There are several tracking algorithms, they can be divided into batch and online algorithms. Since speed was the main factor, the choice fell on the online algorithms. Some of the [batch algorithms implemented by OpenCV](https://broutonlab.com/blog/opencv-object-tracking) were also tested applied to the video and work relatively well applied to the problem. However, even the fastest algorithm ([MOSSE](https://docs.opencv.org/3.4/d0/d02/classcv_1_1TrackerMOSSE.html)) was too slow for online detection, not talking about CSRT.
[DeepSort](https://arxiv.org/abs/1703.07402) is an extension of the SORT algorithm with the use of the appearance information. [Here](https://learnopencv.com/understanding-multiple-object-tracking-using-deepsort/) there is a more detailed explanation and comparison of different trackers' speed and accuracy. DeepSort does not provide the highest accuracy, but it is faster than the alternative algorithms.

These two parts were combined in an application designed with the possibility of changing the chosen models (using other Yolo versions or other tracker versions), the detected category and the objective. The architecture is thought to be recyclable and usable in the future projects as well. The graphical part is implemented with the use of OpenCV functions. Both parts together work relatively fast on GPU (realtime) and quite slow on CPU. We assume that GPU is used.

<!-- ROADMAP -->
## Roadmap

### Challenges

Some boats in the video are counted twice due to their position: <illustration>
The guy participating in the competition is smart and probably knows that most of the existing tracking algorithms would not 
be able to tell that it is the exact same boat, just seen from different angles with a large gap in time. The extension of
this work would be to track the positions of the boats on the map with respect to the camera trajectory and check whether
the detected boat was potentially tracked before. <illustration> In a simplified form it would not even need the camera characteristics.

Some of the assumptions we can make for this solution:
1. Neglect the height of the camera over the boat level when calculating the distance to the other boats
2. Assume that field of view is 45 degrees
3. Neglect camera's rotation around the X-axis (the camera is slightly rotated as the horizon is over the middle of the matrix, but it can be neglected in the calculations we make)
4. Camera path is added to the video stream and synchronized with it.

Thus the problem can be solved as simply as defining vectors on a coordinate field.

Another obvious issue is the occlusion problem. The objects are neither detected nor tracked well when they are occluded by other objects (especially the ones belonging to the same category)

Yolo is not good at recognizing small objects, so some boats that are far away remain undetected. It works better with Yolo7, but it's not perfect. It would be interesting to create an assemble of models to resolve this issue.

### Future work

- [ ] Add support for different types of vehicles;
- [ ] Add recognition of different boat(/vehicle) types (sailing boats, electric boats etc);
- [ ] Add support for Yolov7 as it proved to be the best at detecting the boats;
- [ ] Generalize the solution to different video types (trajectory, illumination)
- [ ] Work on detection of distant objects
- [ ] Add camera trajectory to the algorithm, creating a coordinate field with approximate positions of the detected
      objects with respect to camera position to double check the new objects that enter in the camera view with the 
      change of its normal.
- [ ] Work on the occlusion problem
- [ ] add support of different trackers, including cv2 legacy trackers
- [ ] add test frame set for automatic model speed and accuracy comparison

See the [open issues](https://github.com/STASYA00/boat_tracker/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contact

Stasja - [@stasya00](https://stasyafedorova.wixsite.com/designautomation) - [e-mail](mailto:0.0stasya@gmail.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Yolo](https://github.com/ultralytics/yolov5)
* [Yolo7 Implementation](https://github.com/WongKinYiu/yolov7)
* [DeepSort implementation](https://github.com/mahimairaja/vehicle-counting-yolov5)
* [Ffmpeg](https://www.ffmpeg.org/)
* [My favorite README template](https://github.com/othneildrew/Best-README-Template)
* [Candela](https://candela.com/) - inspiration, input and great task!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/STASYA00/boat_tracker.svg?style=for-the-badge
[contributors-url]: https://github.com/STASYA00/boat_tracker/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/STASYA00/boat_tracker.svg?style=for-the-badge
[forks-url]: https://github.com/STASYA00/boat_tracker/network/members
[stars-shield]: https://img.shields.io/github/stars/STASYA00/boat_tracker.svg?style=for-the-badge
[stars-url]: https://github.com/STASYA00/boat_tracker/stargazers
[issues-shield]: https://img.shields.io/github/issues/STASYA00/boat_tracker.svg?style=for-the-badge
[issues-url]: https://github.com/STASYA00/boat_tracker/issues
[license-shield]: https://img.shields.io/github/license/STASYA00/boat_tracker.svg?style=for-the-badge
[license-url]: https://github.com/STASYA00/boat_tracker/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/STASYA00
[product-screenshot]: assets/screenshot.png




