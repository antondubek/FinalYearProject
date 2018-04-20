"""
Raspberry Pi Face Recognition Treasure Box
Treasure Box Script
Copyright 2013 Tony DiCola
"""
import cv2

import config
import face

import RPi.GPIO as GPIO


def checkFace():
	# Turn Flash ON
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(2,GPIO.OUT)
	GPIO.output(2,GPIO.HIGH)
	output = False
	# Load training data
	print 'DEBUG: Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'DEBUG: Training data loaded!'
	# Initialize camera and box.
	camera = config.get_camera()
	print 'DEBUG: Running recognition sequence'
	for i in range(10):
		print 'DEBUG: Looking for face... Attempt %s /10' %i
		# Check for the positive face and unlock if found.
		image = camera.read()
		# Convert image to grayscale.
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image.
		result = face.detect_single(image)
		if result is None:
			print 'Could not detect single face!  Check the image in capture.pgm' \
				  ' to see what was captured and try again with only one face visible.'
			continue
		x, y, w, h = result
		# Crop and resize image to face.
		crop = face.resize(face.crop(image, x, y, w, h))
		# Test face against model.
		label, confidence = model.predict(crop)
		print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
			'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE',
			confidence)
		if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
			print 'DEBUG: Face recognised - Returning True'
			output = True
			break
		else:
			print 'DEBUG: Face not recognised'
	GPIO.output(2,GPIO.LOW)
	return output
