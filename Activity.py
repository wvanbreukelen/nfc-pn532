from gpiozero import Button
from signal import pause
import time

class Activity:

	lastInputTime = time.time()
	buffer = ""

	def bindButton(self, gpio, char):
		"""
		Bind GPIO input to a button
		"""
		button = Button(gpio, False)

		button.when_pressed = lambda: self.btnPressed(char)

	def btnPressed(self, char):
		curTime = time.time()

		self.buffer = ""
		self.buffer = char


		if (curTime - self.lastInputTime) < 1:
			return


		lastInputTime = curTime

	def getCharBuffer(self):
		return self.buffer;

	def waitForPress(self):
		while self.buffer == "":
			time.sleep(0.2)

		res = self.buffer

		self.buffer = ""
		return res
