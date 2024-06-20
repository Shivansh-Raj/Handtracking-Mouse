# Handtracking-Mouse

**Project Description**
The "Handtracking-Mouse" project is an innovative application that transforms hand movements into mouse control actions on a computer.

****Key Features:-****
**Hand Tracking**: Utilizes real-time hand tracking to detect and follow the movements of your hand and fingers.
Mouse Control: Converts hand gestures into mouse actions, such as moving the cursor, clicking, and dragging.
User-Friendly Interface: Provides an intuitive and responsive experience, making it easy to control the computer without physical contact.
Technologies Used
**OpenCV**: A powerful open-source computer vision library used for image and video processing.
**MediaPipe**: A cross-platform framework by Google for building multimodal machine learning pipelines, crucial for efficient hand tracking.
**PyAutoGUI**: A Python module used to programmatically control the mouse and keyboard, allowing seamless integration of hand gestures with system controls.
Python: The foundational programming language for the project, ensuring simplicity and readability.
****How It Works****
Capture Video Feed: OpenCV captures the video feed from your webcam.
Hand Detection and Tracking: MediaPipe processes the video feed to detect and track hand landmarks in real-time.
**Gesture Interpretation**: The detected hand movements are interpreted to correspond with mouse actions.
**Mouse Action Execution**: PyAutoGUI translates these interpreted gestures into actual mouse movements and clicks on the screen.
