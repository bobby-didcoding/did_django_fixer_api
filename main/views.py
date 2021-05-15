from django.shortcuts import render, redirect, reverse
from django.conf import settings

from .mixins import RedirectParams, Converter
'''
Basic view for viewing currency exchange rates 
'''
def index(request):

	if request.method == "POST":

		symbols = request.POST.getlist("symbols", None)
		base = request.POST.get("base", None)

		if symbols and base:
			symbols = "|".join(symbols)

			return RedirectParams(url = 'main:results', params = {"base": base, "symbols": symbols})

	symbols = Converter().get_symbols()
	context = {}

	if symbols:
		context["symbols"] = symbols["symbols"]

	return render(request, 'main/index.html', context)
	


def results(request):

	base = request.GET.get("base", None)
	symbols = request.GET.get("symbols", None)

	if symbols and base:

		symbols = ",".join(symbols.split("|"))

		conversion = Converter(base = base, symbols = symbols).get_data()

		if conversion:

			context = {
				"conversion": conversion
			}

			return render(request, 'main/results.html', context)

	return redirect(reverse("main:index"))


