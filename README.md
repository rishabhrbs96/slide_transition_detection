# Automatic Slide Transition Detection in Lecture Videos for MOOCs
### * It detects slide transition in the lecture videos of MOOCs .One can also provide the pdf. It automatically compares the pdf slides with the video frames and outputs the seconds along with the slide number when the instructor has changed the slide in video. For easy use, it has been integrated with a django web portal . 
### * It Uses **Python** and **OpenCV** library for detecting the transition points in the lecture videos of the **MooKIT ( Online Course Site )**  .
### * Proposed method involves using **SIFT algorithm** for comparing video frames based upon a global threshold.
### * Uses face detection technique to distinguish between the frames containing the slide and the frame containing the instructor (for videos where slides and frames are on different frames).
### Converts the pdf into images and finally compared it with the frames of the seconds at which transition slide may have occurred.
### * For easy use it is integrated with web interface on **Django** where one can enter the video and the pdf link and get the results through email or can download the file or can copy the results.

## Technologies Used ::
### Python
### OpenCV
### Django
### Bash Commands
