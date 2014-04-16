# encoding: utf-8

available_carriers = {}

from carriers.usps import USPS
available_carriers['USPS'] = USPS

from carriers.lp import LP
available_carriers['LP'] = LP

from carriers.dhlgm import DHLGM
available_carriers['DHLGM'] = DHLGM
