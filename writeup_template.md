**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./writeup/corners_found11.jpg "Corners Found"
[image2]: ./writeup/distorted.jpg "Distorted"
[image3]: ./writeup/undistorted.jpg "Undistorted"
[image4]: ./writeup/binary.jpg "Binary"
[image5]: ./writeup/warped.jpg "Warped"
[image6]: ./writeup/poly_example.jpg "Lane Lines"
[image7]: ./writeup/result.jpg "Result"
[video1]: ./output1_tracked.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### In this writeup, I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf. 

This is it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the file /camera_cal/cam_cal.py. Note that I make use of the cv2 libary's findChessboardCorners and calibrateCamera functions. 

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the real world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function. Here's an example of a calibrated chessboard image:

![alt text][image1]


### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, let's compare before and after photos. These images are slightly distorted because of the curvature of the camera lens through which the pictures were shot. While the distortion isn't visible without a point of comparison, it becomes more noticeable when you put a distorted image side to side with an undistorted one. Here's an original distored image:

![alt text][image2]

Now, here's that same image after the undistortion. Note the difference in the distance between the white car and the edge of the image. Distortion in camera images occurs primarily at the edges. This explains the relative similarity of the images, save for the noticeable changes in the car at the edge of the image.

![alt text][image3]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image. Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at lines 53 through 58 in `image_gen.py`).  Here's an example of my output for this step.

![alt text][image4]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform can be found in lines 60 to 77 in image_gen.py. I chose to hardcode the source and destination points in the following manner:

```python
bot_width = .76
mid_width = .08
height_pct = .62
bottom_trim = .935
src = np.float32([[img.shape[1]*(.5-mid_width/2),img.shape[0]*height_pct],
				 [img.shape[1]*(.5+mid_width/2), img.shape[0]*height_pct],
				 [img.shape[1]*(.5+bot_width/2),img.shape[0]*bottom_trim],
				 [img.shape[1]*(.5-bot_width/2),img.shape[0]*bottom_trim]])
dst = np.float32([[offset,0],
				 [img_size[0]-offset, 0],
				 [img_size[0]-offset, img_size[1]],
				 [offset,img_size[1]]])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 588.8, 446.4      | 320, 0        | 
| 691.2, 446.4      | 960, 0      |
| 1126.4, 673.2     | 960, 720      |
| 153.6, 673.2      | 320, 720        |

Here's an example of the warped image, which could be considered to be a "bird's eye view" of the road.

![alt text][image5]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial

Next, I call find_window_centroids() in `tracker.py` to use the window-sliding method to detect lane lines. I do so by finding the center point of the right and left lanes, and then convolving over slices of the image. I fit the resulting centroids with a 2nd order polynomial to form a lane line for both the left and right sides. The result can be seen in this image, where I've drawn lines on top of the warped bird's eye view of the lane lines. 

![alt text][image6]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I computed the radius of curvature and position of the vehicle in lines 136-150 of image_gen.py. 

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines 119 through 128 in my code in `image_gen.py`.  Here is an example of my result on a test image. Note that the image in step 4 has been warped using the inverse of the original transform in order to convert from a bird's eye view back to the perspective of the original image. 

![alt text][image7]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./output1_tracked.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I've set up my pipeline to be robust to the provided images and video, but it might do less well under more challenging conditions. For example, varying road gradient may cause my system to fail. A very steep road would occupy more of the image space than I currently consider in my window sliding technique. While I currently consider only the bottom quarter of the image, a very steep hill may require me to consider a third or half of the image to properly detect lanes. In addition, the system could be made more robust if the image source and destination points were calculated dynamically, rather than being hard coded. This would also solve for the challenges presented by gradients. 

If I were to improve this project further, I might experiment with more thresholding techniques. I've used color thresholding and Sobel thresholding in my solution, but there are a number of other thresholding mechanisms that could improve the accuracy of my solution, as well as its robustness to challenging scenarios. There are a number of thresholds which I could explore, like Otsu's threshold or the adaptive threshold.
