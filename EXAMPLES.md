Layout examples
===============

Watpost allows you to customize its output to a great extent. Here are some examples of what you can do.

All of the following example outputs were generated with `parcels.json` that looked like this:

	[
		{
			"number": "RS000000000LV",
			"carriers": ["LP"]
		},
		{
			"number": "LJ111111111US",
			"carriers": ["USPS", "LP"]
		},
		{
			"number": "RB222222222HK",
			"carriers": ["LP"]
		}
	]

Minimalistic layout with only the most recent state
---------------------------------------------------
Config:

	{
		"merge_states": true,
		"displayed_state_count": 1,
		"state_order": "asc",
		"output_format": "{parcels}\n",
		"parcel_format": "{tracking}: {data}",
		"parcel_separator": "\n",
		"carrier_format": "  {shortname}: {states}",
		"carrier_separator": "\n",
		"state_format": "{state}",
		"state_separator": "\n",
		"no_data_message": "No data",
		"datetime_format": "%d.%m %H:%M"
	}

Output:

	RS000000000LV: Item sent abroad
	LJ111111111US: Processed through USPS Sort Facility
	RB222222222HK: Item delivered


Minimalistic layout with only the most recent state from each service
---------------------------------------------------------------------
Config:

	{
		"merge_states": false,
		"displayed_state_count": 1,
		"state_order": "asc",
		"output_format": "{parcels}\n",
		"parcel_format": "{tracking}:\n{data}",
		"parcel_separator": "\n",
		"carrier_format": "  {shortname}: {states}",
		"carrier_separator": "\n",
		"state_format": "{state}",
		"state_separator": "\n",
		"no_data_message": "No data",
		"datetime_format": "%d.%m %H:%M"
	}

Output:

	RS000000000LV:
	  LP: Item sent abroad
	LJ111111111US:
	  USPS: Processed through USPS Sort Facility
	  LP: No data
	RB222222222HK:
	  LP: Item delivered

A richer layout
---------------

Config:

	{
		"merge_states": false,
		"displayed_state_count": 3,
		"state_order": "asc",
		"output_format": "Watpost tracking information:\n{parcels}\n",
		"parcel_format": "Parcel #{tracking}:\n{data}",
		"parcel_separator": "\n",
		"carrier_format": "  {fullname}:\n{states}",
		"carrier_separator": "\n",
		"state_format": "    {datetime}: {state}",
		"state_separator": "\n",
		"no_data_message": "No data",
		"datetime_format": "%d.%m %H:%M"
	}

Output:

	Watpost tracking information:
	Parcel #RS000000000LV:
	  Latvijas Pasts:
	    04.04 17:42: Item sent to Sorting centre - Rīga
	    04.04 19:51: Item received at Sorting centre - Rīga
	    04.04 21:24: Item sent abroad
	Parcel #LJ111111111US:
	  United States Postal Service:
	    18.02 08:00: Electronic Shipping Info Received
	    20.02 00:27: Shipment Accepted
	    22.02 19:20: Processed through USPS Sort Facility
	  Latvijas Pasts:
	    No data
	Parcel #RB222222222HK:
	  Latvijas Pasts:
	    25.01 08:09: Item received at Delivery point: PN Rīga 15, PP-1015
	    25.01 08:19: Delivered information notice
	    25.01 14:04: Item delivered

