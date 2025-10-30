import os 
import cv2
import mediapipe as mp
from tkinter import filedialog, Tk, messagebox
import tkinter as tk


# Initialize tkinter (but don't show the main window)
root = Tk()
root.withdraw()
file_path = "abc"

# Open webcam / file dialog 
def input():
	root = tk.Tk()
	root.withdraw()
	
	if (messagebox.askyesno("Webcam", "Do you want to use webcam instead of a file?")):
		return "webcam"
	else:
		root.withdraw()
		file_path = filedialog.askopenfilename(
		title="Select a file",
		filetypes=[
				("Image files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"),
				("Video files", "*.mp4 *.avi *.mov *.mkv *.flv"),
				("All files", "*.*")
			])
		return file_path
	
		
file_path = input()

def process_img(img, face_detection):
	H, W, _ = img.shape
	
	img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	out = face_detection.process(img_rgb)
	
	if out.detections is not None:
		for detection in out.detections:
			location_data = detection.location_data
			bbox = location_data.relative_bounding_box
		
			x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height
			x1 = int(x1 * W)
			y1 = int(y1 * H)
			w = int(w * W)
			h = int(h * H)
			
			# cv2.rectangle(img, (x1, y1), (x1+w, y1+h), (0, 255, 0), 10)
			
			# cv2.imshow('img', img)
			# cv2.waitKey(0)
			
#blur faces
			img[y1:y1+h, x1:x1+w, :] = cv2.blur(img[y1:y1+h, x1:x1+w, :], (50, 50)) 
			
	return img


output_dir = './output'
if not os.path.exists(output_dir):
	os.makedirs(output_dir)

#detect faces
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:

	if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')):
#read image
		img = cv2.imread(file_path)
		# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = process_img(img, face_detection)
#save image
		cv2.imwrite(os.path.join(output_dir, 'output.png'), img)
	

	elif file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv')):
#read video
		cap = cv2.VideoCapture(file_path)
		ret, frame = cap.read()
		output_video = cv2.VideoWriter(os.path.join(output_dir, 'output.mp4'),
			cv2.VideoWriter_fourcc(*'MP4V'),
			25,
			(frame.shape[1], frame.shape[0]))
	
		while ret:
			frame = process_img(frame, face_detection)
			output_video.write(frame)
			ret, frame = cap.read()
		
		cap.release()
		output_video.release()
	
	
	elif file_path == "webcam":
	#read webcam
		cap = cv2.VideoCapture(0)
		ret, frame = cap.read()
		while ret:
			frame = process_img(frame, face_detection)
			cv2.imshow('frame', frame)
			if cv2.waitKey(40) & 0xFF == ord('q'):
				break
			ret, frame = cap.read()
		
		cap.release()