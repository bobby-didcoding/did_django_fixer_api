from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode
import requests
import json
from datetime import datetime



'''
Used to append url parameters when redirecting users
'''
def RedirectParams(**kwargs):
	url = kwargs.get("url")
	params = kwargs.get("params")
	response = redirect(url)
	if params:
		query_string = urlencode(params)
		response['Location'] += '?' + query_string
	return response

'''
Handles currency from Fixer.io
'''
class Converter:

	def __init__ (self, *args, **kwargs):

		self.base = kwargs.get("base")
		self.symbols = kwargs.get("symbols")

	def get_data(self):

		print(self.symbols)

		result = requests.get(
			'http://data.fixer.io/api/latest',
			 params={
			 'base': self.base,
			 'symbols': self.symbols,
			 "access_key": settings.API_KEY
			 })

		conversion = result.json()

		if conversion["success"] == True:

			return {
				'base': self.base,
				'rates': conversion["rates"],
				'date': datetime.utcfromtimestamp(conversion["timestamp"]).date()
			}
		return None

	def get_symbols(self):

		result = requests.get(
			'http://data.fixer.io/api/symbols',
			 params={
			 "access_key": settings.API_KEY
			 })
		symbols = result.json()

		if symbols["success"] == True:
			return {
				'symbols': symbols["symbols"],
			}
		return None




	