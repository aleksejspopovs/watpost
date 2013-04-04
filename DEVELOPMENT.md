Additional carrier implementation
=================================

Adding support for new carriers to Watpost is fairly easy (as long as you have a way to extract information from that carrier's service). I'll try to briefly describe the process here, though you might want to take a look at `bases.py` and `carriers/usps.py` first, as it is a nice example that will probably give you all the information you need.

To implement support for a new carrier, you need to do the following:

1. Decide on a short and a full name for the carrier. A short name will probably be an abbreviation or a common short form of the name (e.g. USPS and FedEx are short names, while United States Postal Service and Federal Express are full ones). I will refer to these names as $short and $full from now on.
2. Create a file named `carriers/lowcase($short).py` and implement a class named `$short` inside it. This class should be a subclass of the `PostService` class defined in `bases.py` and should implement all three of its methods (`info()`, `track(tracking)` and `valid_tracking_number(tracking)`, as described in `bases.py`).
3. Add the following lines to the bottom of `all_carriers.py`:

		from carriers.lowcase($short) import $short
		available_carriers['$short'] = $short
4. You're done! Now test the carrier and, if everything works fine, submit a pull request.
