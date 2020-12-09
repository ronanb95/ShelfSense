from django.shortcuts import render

def deviceSetHome(request):
	return render(request, 'deviceSetup/deviceSetHome.html')
