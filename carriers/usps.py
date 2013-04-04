# encoding: utf-8
import sys
import requests
from lxml import etree
import datetime, locale, pytz
import re
import bases

server_url = 'http://production.shippingapis.com/ShippingAPI.dll'
# I honestly have no idea if USPS are going to ban my API key for publishing it or not.
api_username = '972IKALE7387'

class USPS(bases.PostService):
	@staticmethod
	def info():
		return ('USPS', \
			'United States Postal Service', \
			'National post service of the United States. Tracking numbers follow the AB123456789CD format.')

	@staticmethod
	def parse_event(event):
		get_tag_text = lambda which: event.xpath(which)[0].text or ''
		# location & state are simple
		country = get_tag_text('EventCountry') or 'United States'
		location = country + ' — ' + get_tag_text('EventCity') + ', ' + get_tag_text('EventState')
		state = get_tag_text('Event')

		# now, for the date. fuck.
		for l in ('en_US', 'en_US.utf8'):
			try:
				locale.setlocale(locale.LC_ALL, l)
			except Exception:
				pass
		if get_tag_text('EventTime') == '':
			datetime_string = get_tag_text('EventDate')
			parsed_date = pytz.timezone('US/Central').localize(datetime.datetime.strptime(datetime_string, '%B %d, %Y'))
		else:
			datetime_string = get_tag_text('EventDate') + ' ' + get_tag_text('EventTime')
			parsed_date = pytz.timezone('US/Central').localize(datetime.datetime.strptime(datetime_string, '%B %d, %Y %I:%M %p'))

		return bases.ParcelState(parsed_date, location, state)


	@staticmethod
	def track(tracking):
		r = requests.get(server_url + \
			'?API=TrackV2&XML=<TrackFieldRequest USERID="{userid}"><TrackID ID="{tr}"></TrackID></TrackFieldRequest>'.format(tr=tracking, userid=api_username))

		xml = etree.fromstring(r.text)
		if (len(xml[0]) == 0) or (xml[0][0].tag == 'Error'):
			return []
		res = [USPS.parse_event(e) for e in xml[0]]
		res.sort()

		return res

	@staticmethod
	def valid_tracking_number(tracking):
		if len(tracking) != 13:
			return False
		return re.match(r'[A-Z]{2}[0-9]{9}[A-Z]{2}', tracking) is not None
