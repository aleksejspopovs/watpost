#!/usr/bin/python3
# encoding: utf-8
import argparse
import json
import os, sys
from all_carriers import available_carriers

app_short_name = 'watpost'
app_full_name = 'Watpost'
app_version = '1.0.0'
app_web = 'https://github.com/popoffka/watpost'

class TemplateKeyError(KeyError):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return 'Key {key} used in template not found.'.format(key=self.value)

class SettingsKeyError(KeyError):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return 'Required key {key} was not found in settings.'.format(key=self.value)

class Settings():
	def __init__(self, path):
		self.data = read_json(path)
	def __getitem__(self, key):
		if key in self.data:
			return self.data[key]
		else:
			raise SettingsKeyError(key)

def get_default_data_directory():
	if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
		return os.path.join(os.getenv('APPDATA'), app_full_name)
	elif os.getenv('XDG_CONFIG_HOME') is not None:
		return os.path.join(os.getenv('XDG_CONFIG_HOME'), app_short_name)
	else:
		return os.path.expanduser(os.path.join('~', '.config', app_short_name))

def get_default_config_path():
	return os.path.join(get_default_data_directory(), 'settings.json')

def get_default_parcels_path():
	return os.path.join(get_default_data_directory(), 'parcels.json')

def read_json(path):
	return json.load(open(path))

def get_formatted(format_string, **args):
	try:
		return format_string.format(**args)
	except KeyError as ke:
		raise TemplateKeyError(ke.args[0])

def state_format(format_string, datetime_format, state, carrier):
	return get_formatted(format_string, \
		state=state.state, \
		datetime=state.date.astimezone().strftime(datetime_format),\
		location=state.location,\
		carrierfull=available_carriers[carrier].info()[1],\
		carriershort=available_carriers[carrier].info()[0])

def reverse(lst):
	return lst[::-1]

def print_carriers():
	print('Following carriers are supported by this install of {name}:\n'.format(name=app_full_name))
	for carrier in available_carriers:
		info = available_carriers[carrier].info()
		print("{fullname} ({shortname})\n  {description}\n".format( \
			fullname=info[1],
			shortname=info[0],
			description=info[2]))

def main():
	parser = argparse.ArgumentParser(description='Track the states of your parcels sent via global mail carriers.', \
		epilog='This is {name} {version}. Report any bugs to {webpage}.'.format(name=app_full_name, version=app_version, webpage=app_web))
	parser.add_argument('-s', '--settings', \
		help='Load settings from this file instead of the default one.',
		default=get_default_config_path())
	parser.add_argument('-p', '--parcels', \
		help='Use this parcel file instead of the default one.',
		default=get_default_parcels_path())
	parser.add_argument('-c', '--carriers', \
		help='Display a list of all carriers available and quit.', action='store_true')
	parser.add_argument('-v', '--version', \
		help='Report version number and quit.', \
		action='version', version='{name} {version}'.format(name=app_full_name, version=app_version))

	args = parser.parse_args()

	if args.carriers:
		print_carriers()
		return 0

	try:
		settings = Settings(args.settings)
	except:
		print('Error: failed to load settings file {path}.'.format(path=args.settings))
		return 1
	try:
		parcels = read_json(args.parcels)
	except:
		print('Error: failed to load parcel list {path}.'.format(path=args.parcels))
		return 1

	try:
		all_parcels = []
		state_count = settings['displayed_state_count']
		merge = settings['merge_states']
		order = settings['state_order']
		for parcel in parcels:
			if ('carriers' not in parcel) or ('number' not in parcel):
				raise SettingsKeyError('carriers or number')

			number = parcel['number']
			results = []
			for carrier in parcel['carriers']:
				if carrier not in available_carriers:
					print('Unkown carrier {name}.'.format(name=carrier))
					return 1

				if not available_carriers[carrier].valid_tracking_number(number):
					print('{num} is not a valid tracking number for {carrier}.'.format(num=number, carrier=carrier))
					return 1

				if merge:
					results += [(x, carrier) for x in available_carriers[carrier].track(number)]
				else:
					results += [(carrier, available_carriers[carrier].track(number))]

			if merge:
				results.sort()
				if state_count != -1:
					results = results[-state_count:]
				if order == 'desc':
					results = reverse(results)

				all_states = settings['state_separator'].join([state_format(settings['state_format'], settings['datetime_format'], x[0], x[1]) for x in results])
			else:
				all_carriers = []
				for group in results:
					carrier = group[0]
					states = group[1]
					if state_count != -1:
						states = states[-state_count:]
					if order == 'desc':
						states = reverse(states)


					if len(states):
						all_states = settings['state_separator'].join([state_format(settings['state_format'], settings['datetime_format'], x, carrier) for x in states])
					else:
						all_states = settings['no_data_message']
					all_carriers.append(get_formatted(settings['carrier_format'], \
						fullname=available_carriers[carrier].info()[1], \
						shortname=available_carriers[carrier].info()[0], \
						states=all_states))
				all_states = settings['carrier_separator'].join(all_carriers)
			this_parcel = get_formatted(settings['parcel_format'], tracking=number, data=all_states)
			all_parcels.append(this_parcel)

		results = settings['parcel_separator'].join(all_parcels)
		print(get_formatted(settings['output_format'], parcels=results), end='')
	except TemplateKeyError as tke:
		print(tke)
		return 1
	except SettingsKeyError as ske:
		print(ske)
		return 1

	return 0

if __name__ == '__main__':
	sys.exit(main())
