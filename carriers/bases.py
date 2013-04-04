#!/usr/bin/python3
# encoding: utf-8

class ParcelState():
	def __init__(self, date, location, state):
		self.date = date
		self.location = str(location)
		self.state = str(state)
	def __lt__(self, another):
		return self.date < another.date
	def __str__(self):
		return str(self.date) + u': ' + self.location + u': ' + self.state

class PostService():
	@staticmethod
	def info():
		raise NotImplemented()

	@staticmethod
	def track(tracking):
		raise NotImplemented()
	@staticmethod
	def valid_tracking_number(tracking):
		raise NotImplemented()
