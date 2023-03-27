from django.shortcuts import render
from django.views.generic import TemplateView,View
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from wsgiref.util import FileWrapper
import os
# Create your views here.


class HomePage(TemplateView):
	template_name='home.html'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		file_name="C:/Users/jhamayan/OneDrive - Ocwen Financial Corporation/Documents/Study/ClassificaitonModel/8011356311.pdf"
		f_data=None
		##open the file
		with open(file_name,'rb') as f:
			pdf_data=f.read()
		#Split the pages
		pdf_pages = pdf_data.split(b'%%EOF/n')

		#save the PDF pages to the cache
		cache.set('pdf_pages',pdf_pages)

		#INIT the page_no and the pg_dict
		context['page_number'] = 1
		context['page_data'] = {}

		return context

	def post(self, request, *args, **kwargs):
		#get the page number and the page data from the request
		page_number= int(request.POST.get('page_number'))
		page_data= request.POST.get('page_data')

		#save the page data to the cache
		cache.set(f'page_data_{page_number}',page_data)

		#If this is the last page, combine all the page data into a single dict
		if page_number == cache.get('num_pages'):
			all_page_data={}
			for i in range(1,page_number+1):
				all_pages_data.update(cache.get(f'page_data_{i}'))

			#Save the combined data
			cache.set('all_page_data',all_page_data)

		#return JSON stating added all the data and it was success
		return JsonResponse({'success':True})


class PDFViewer(TemplateView):
    template_name='test.html'


import os
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt





@csrf_exempt
def stream_image(request):
    file_path=r"C:\DEV_TEMP\1457490.jpg"
    file_path=copy_file(file_path)
    print(file_path)
    try:
        external_path = os.path.abspath(file_path)
        if not external_path.startswith(os.path.abspath('media')):
            # If the file is not inside the media directory, return a 403 Forbidden response
            return HttpResponse("Access denied", status=403)
        wrapper = FileWrapper(open(external_path, 'rb'))
        response = HttpResponse(wrapper, content_type='image/jpeg')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(external_path)
        return response
    except FileNotFoundError:
        return HttpResponse("File not found.")

import shutil
from django.conf import settings

def copy_file(cpath):
	abs_path=os.path.abspath(cpath)
	final_path= os.path.join(settings.MEDIA_ROOT,os.path.basename(abs_path))
	if os.path.exists(final_path):
		os.remove(final_path)
	shutil.copy(cpath,settings.MEDIA_ROOT)
	return final_path