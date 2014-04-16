# encoding: utf-8
import sys
import pytz
import requests, bs4
from datetime import datetime
import re
from . import bases

class DHLGM(bases.PostService):
	@staticmethod
	def info():
		return ('DHLGM', \
			'Deutsche Post DHL Global Mail', \
			'Tracking numbers follow the GM00000000000000000 format.')

	@staticmethod
	def track(tracking):
		r = requests.get('http://webtrack.dhlglobalmail.com/',
			params={'trackingnumber': tracking})
		soup = bs4.BeautifulSoup(r.text)

		if soup.find(class_='alert-danger') is not None:
			return []

		current_date = None
		results = []
		tz = pytz.utc
		for li in soup.find('ol', class_='timeline')('li'):
			if 'timeline-date' in li.get('class', []):
				current_date = li.text
			elif 'timeline-event' in li.get('class'):
				assert current_date is not None
				time = current_date + ' ' + li.find(class_='timeline-time').text
				date = tz.localize(datetime.strptime(time, '%b %d, %Y %I:%M%p'))
				location = li.find(class_='timeline-location').text.strip()
				state = li.find(class_='timeline-description').text.strip()
				results.append(bases.ParcelState(date, location, state))
		results.sort()
		return results

	@staticmethod
	def valid_tracking_number(tracking):
		if len(tracking) != 19:
			return False
		return re.match(r'GM[0-9]{17}', tracking) is not None
