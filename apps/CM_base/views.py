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
		file_name = "C:/Users/jhamayan/OneDrive - Ocwen Financial Corporation/Documents/Study/Classification/8011356311.pdf"
		f_data=None
		##open the file
		with open(file_name,'rb') as f:
			pdf_data=f.read()
		#Split the pages
		pdf_pages = pdf_data.split(b'%%EOF\n')

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


class PDFViewer(View):
    #template_name='test.html'
    def get_context_data(self, request):
        file_name = "C:/Users/jhamayan/OneDrive - Ocwen Financial Corporation/Documents/Study/Classification/8011356311.pdf"
        image_path = "C:/Users/jhamayan/Downloads/LOGO.png"
        with open(image_path,'rb') as image_data:
        	wrapper=FileWrapper(image_data)
        	response=HttpResponse(wrapper,content_type='image/jpeg')
        	response['Content-Disposition']= 'inline; filename='+os.path.basename(image_path)
        	return response

