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
		# returns a tuple with the folowing information:
		# (short name, full name, description)
		raise NotImplemented()

	@staticmethod
	def track(tracking):
		# returns a sorted list of ParcelStates for this tracking number.
		# if it isn't possible to get information because the service doesn't have any, should return an empty list.
		raise NotImplemented()

	@staticmethod
	def valid_tracking_number(tracking):
		# checks if the supplied tracking number is a valid one (is allowed to give false positives).
		# returns a bool.
		raise NotImplemented()
