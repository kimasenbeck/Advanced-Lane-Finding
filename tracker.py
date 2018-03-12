import numpy as np 
import cv2
class tracker():

	def __init__(self,Mywindow_width, Mywindow_height, Mymargin, My_ym = 1, My_xm = 1, Mysmooth_factor = 15):
		#list that stores all past center set values used for smoothing output
		self.recent_centers = []

		#the window pixel width of the center values, used to count pixels inside cetner windows, used to determine curve values
		self.window_width = Mywindow_width

		#the window pixel height of the center values, used to count pixels inside center windows to determine curve values
		# breaks the image into vertical levels
		self.window_height = Mywindow_height

		# the pixel distance in both directions to slide (left_window + right_window) template for searching
		self.margin = Mymargin

		self.ym_per_pix = My_ym #meters per pixel in vertical axis
		self.xm_per_pix = My_xm #meters per pixel in horizontal axis
		self.smooth_factor = Mysmooth_factor

	#the main tracking function for finding and storing lane segment positions
	def find_window_centroids(self, warped):
		window_width = self.window_width
		window_height = self.window_height
		margin = self.margin

		window_centroids = []
		window = np.ones(window_width)

		# Determine where the lanes begin by summing up a vertical image slice, then convolving that slice, and finally taking the max
		# We get our slices by taking the sum of the bottom fourth of the image
		l_sum = np.sum(warped[int(3*warped.shape[0]/4):,:int(warped.shape[1]/2)], axis=0)
		l_center = np.argmax(np.convolve(window,l_sum))-window_width/2
		r_sum = np.sum(warped[int(3*warped.shape[0]/4):,int(warped.shape[1]/2):], axis=0)
		r_center = np.argmax(np.convolve(window,r_sum))-window_width/2+int(warped.shape[1]/2)
		
		# Add the newly found centorid to our collection
		window_centroids.append((l_center,r_center))

		#go through each layer looking for max pixel locations
		for level in range(1,(int)(warped.shape[0]/window_height)):
			#convolve the window into the vertical slice of the image
			image_layer = np.sum(warped[int(warped.shape[0]-(level+1)*window_height):int(warped.shape[0]-level*window_height),:], axis=0)
			conv_signal = np.convolve(window, image_layer)
			#Use window_width/2 as offset because convolution signal reference is at right side of window, not center of window
			offset = window_width/2
			#Find the left center point. Begin the search by starting with the location of the last center point we found.
			l_min_index = int(max(l_center+offset-margin,0))
			l_max_index = int(min(l_center+offset+margin,warped.shape[1]))
			l_center = np.argmax(conv_signal[l_min_index:l_max_index])+l_min_index-offset
			#Find the right center point. Begin the search based on the location of the last r_center we found
			r_min_index = int(max(r_center+offset-margin,0))
			r_max_index = int(min(r_center+offset+margin,warped.shape[1]))
			r_center = np.argmax(conv_signal[r_min_index:r_max_index])+r_min_index-offset
			#Add what we found for that layer
			window_centroids.append((l_center,r_center))

		# Append the center points we just found so that we can smooth our results
		self.recent_centers.append(window_centroids)
		return np.average(self.recent_centers[-self.smooth_factor:], axis = 0) #perform the smoothing by taking the average of our recent center points