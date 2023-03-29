from django.urls import reverse
from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView,View
######### Custom Libs for other functions
from wsgiref.util import FileWrapper
import os
import shutil
import base64
####### Local Libs
from .util import *


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



class PDFViewer(TemplateView):
    template_name='test.html'
	
    def get_context_data(self, **kwargs):
        file_path=r"C:\DEV_TEMP\TEMP\page_"
        context=super().get_context_data(**kwargs)
        pdf_name=kwargs['image_path']
        page_no= kwargs['page_no'] if kwargs['page_no'] else 0
        #print(page_no)
        context['pdf_name']=pdf_name
        context['page_no']=page_no
        file_path+=str(page_no)+'.jpg'
        with open(file_path,'rb') as img:
            img_data=img.read()
        img_data=base64.b64encode(img_data).decode('utf-8')
        context['image']=img_data
        context['next_page_no']=page_no+1
        context['prev_page_no']=page_no-1 if (page_no-1 )>=0 else 0
        return context
    

