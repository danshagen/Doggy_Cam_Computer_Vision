"""This module runs the dog unrest detection algorithm and saves the video and
result as files."""

import plac
import cv2
from algorithm import motion_detection, get_algorithm_version
import telegram

import numpy as np
import cv2

def start_bot():
	"""Start the bot."""
	global bot
	bot = telegram.Bot("2071914358:AAH_aStmNRKCehcM-GlMlU1gC5WD7sJTcRM")
	status = bot.send_message(chat_id="-1001643202570", text="Starting doggy cam!")


def run():
	"""Press Ctrl-C to terminate."""

	print('Opening webcam stream...')
	video = cv2.VideoCapture(0)

	frame_width = int(video.get(3))
	frame_height = int(video.get(4))
	size = (frame_width, frame_height)
	webcam = cv2.VideoWriter('webcam.avi', 
							 cv2.VideoWriter_fourcc(*'MJPG'),
							 10, size)
	print('Start telegram bot...')
	start_bot()

	print('Starting doggy cam...')
	events = 0 
	unrest = False
	temp = None

	try:
		while True:
			global frame
			ret, frame = video.read()
			if frame is None:
				break

			# detect motion
			result, _, _ = motion_detection(frame)
			# cv2.imshow('Doggy Cam: Standard View', frame) # DEBUG

			# save video to file
			webcam.write(frame)

			# detect event times and save video
			# new unrest
			if result and not unrest:
				events += 1
				temp = cv2.VideoWriter('temp_{}.avi'.format(events), 
										cv2.VideoWriter_fourcc(*'MJPG'),
										10, size)
				cv2.imwrite('temp.png', frame)
				global bot
				bot.send_photo(chat_id="-1001643202570", 
					photo=open('temp.png', 'rb'),
					caption="doggy movement!")
			# active unrest
			if result:
				temp.write(frame)

			# unrest over
			if not result and unrest:
				cv2.imwrite('temp.png', frame)
				global bot
				bot.send_photo(chat_id="-1001643202570", 
					photo=open('temp.png', 'rb'),
					caption="unrest over.")

			unrest = result

			# cv2.waitKey(1) # DEBUG
	except KeyboardInterrupt:
		pass

	print('Exiting doggy cam.')
	bot.send_message(chat_id="-1001643202570", text="Stopping doggy cam!")
	video.release()

	print('{} events detected.'.format(events))


if __name__ == '__main__':
	plac.call(run)