#! -*- coding:utf-8 -*-

from html.parser import HTMLParser
from urllib import request
import pdb

class MyHTMLPaser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.__event={}
		self.__events=[]
		self.__flags={
			'event_title': False,
			'datetime': False,
			'event_location': False
		}

	def handle_starttag(self, tag, attrs):
		for attr in attrs:
			if 'event-title' in attr:
				self.__flags['event_title'] = True
			elif 'datetime' in attr:
				self.__flags['datetime'] = True
			elif 'event-location' in attr:
				self.__flags['event_location'] = True

	def handle_data(self,data):
		if self.__flags['event_title']:
			self.__event['event_title'] = data
			self.__flags['event_title'] = False
		elif self.__flags['datetime']:
			self.__event['datetime'] = data
			self.__flags['datetime'] = False
		elif self.__flags['event_location']:
			self.__event['event_location'] = data
			self.__flags['event_location'] = False
			self.__events.append(self.__event)
			self.__event = {}

	def get_data(self):
		return self.__events

def getHTML():
	with request.urlopen('https://www.python.org/events/python-events/') as f:
		data = f.read().decode('utf-8')
	return data


if __name__ == '__main__':
	parser = MyHTMLPaser()
	parser.feed(getHTML())
	# pdb.set_trace()
	events = parser.get_data()
	print(events)