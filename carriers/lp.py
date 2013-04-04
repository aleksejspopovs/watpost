# encoding: utf-8
import sys
import requests, bs4
import datetime, pytz
import re
import bases

class LP(bases.PostService):
	@staticmethod
	def info():
		return ('LP', \
			'Latvijas Pasts', \
			'National post service of Latvia. Tracking numbers follow the AB123456789CD format.')

	@staticmethod
	def track(tracking):
		postdata = {
			'fid': tracking
		}
		r = requests.post('http://www.manspasts.lv/webtracking_test/?' +
			'lang=en&' +
			'webtracking2=find', data=postdata)
		response = r.text

		# fuck fuck fuck. sorry. i'm very sorry.
		# Latvijas Pasts, why can't you just make an API?
		# what's the point of these session IDs, anyway?
		uid = response[response.index('uid=') + 4:response.index('uid=') + 4 + 32]

		r = requests.get('http://www.manspasts.lv/webtracking_test/ipsweb.php?lang=en&fid={tr}&uid={uid}'.format(tr=tracking, uid=uid))
		r.encoding = 'utf-8'
		soup = bs4.BeautifulSoup(r.text)

		header = soup.find('tr', class_='table_lo').text
		if ('Incorrect control number' in header) or ('No postal item with such number has been found' in header):
			return []

		results = []
		for line in soup('tr'):
			# we ignore the header and the footer
			if line.td == None:
				continue

			columns = line('td')
			# why does dealing with dates have to be so painful?
			# anyway, this parses the provided date as Europe/Riga and returns the corresponding date in UTC
			parsed_date = pytz.timezone('Europe/Riga').localize(datetime.datetime.strptime(columns[0].text, '%d.%m.%Y %H:%M:%S')).astimezone(pytz.utc)
			location = columns[1].text + ' — ' + columns[2].text
			state = columns[3].text
			results.append(bases.ParcelState(parsed_date, location, state))

		results.sort()
		return results

	@staticmethod
	def valid_tracking_number(tracking):
		if len(tracking) != 13:
			return False
		return re.match(r'[A-Z]{2}[0-9]{9}[A-Z]{2}', tracking) is not None
