from django.urls import reverse
from django.core.cache import cache
from django.shortcuts import render,redirect
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
        page_no=kwargs.get('page_no')
        pdf_name=kwargs.get('pdf_path')
        img_data=self.getImage(pdf_name,page_no)
        if img_data is None:
            return "Issue in the URL"
        ########### Setting and prepping the data to be displayed on the page
        context['pdf_name']=pdf_name
        context['page_no']=page_no
        context['image']=self.getImage(pdf_name,page_no)
        context['next_page_no']=page_no+1 if int(cache.get(pdf_name)['total_pg'])-1>page_no else page_no ##last page condition
        context['prev_page_no']=page_no-1 if (page_no-1 )>=0 else 0  ## First Page condition
        print(f"PAGE:{context['page_no']}\nNEXT PAGE:{context['next_page_no']}\nPREV_PAGE:{context['prev_page_no']}")
        return context

    def post(self, request, *args, **kwargs):
        print("POST CALLED")
        ## Get data from Arguments
        page_no=kwargs.get('page_no')
        pdf_name=kwargs.get('pdf_path')
        ## Get data from Post Request
        data=request.POST
        loan_number=data.get('loan_number')
        doc_id=data.get('doc_id')
        #save the page data to the cache
        cache_key= f"{pdf_name}_{page_no}"
        print(f"Loan:{loan_number}\ndocID:{doc_id}\nPDF_NAME: {pdf_name}\npage_no :{page_no}")
        cache.set(cache_key,{'loan_number':loan_number,'doc_id':doc_id,'pdf_name':pdf_name,'page_no':page_no})
        
        #If next page load next page else show the final page and move to the next doc
        total_pages=cache.get(pdf_name)
        if total_pages['total_pg']>page_no:
            return redirect('home',pdf_path=pdf_name,page_no=page_no+1)
        else:
            print("last page")

    def getImage(self,pdf_nm,page_no):
        file_path="C:\DEV_TEMP\TEMP\\"
        file_nm="page_"
        final_name=file_path+file_nm+str(page_no)+'.jpg'
        ######Checking if file exists else return None
        if not os.path.exists(final_name):
            return None
        ###### Setting up the initial cache to show the max pages
        elif not cache.get(pdf_nm):
            files=os.listdir(file_path)
            cache.set(pdf_nm,{'total_pg':len(files)})
        ###### Reading Image
        with open(final_name,'rb') as img:
            img_data=img.read()
        img_data=base64.b64encode(img_data).decode('utf-8')
        print(f"Rendering {pdf_nm} for page {page_no}")
        return img_data





class PDFViewer(TemplateView):
    template_name='test.html'
	
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pdf_name=kwargs['image_path'] 
        page_no= kwargs['page_no']
        if not cache.get(pdf_name):
            #files=os.listdir(file_path)
            cache.set(pdf_name,{'total_pages':8})
            print("Cache value set for {pdf_name}",pdf_name)
            print(pdf_name,cache.get(pdf_name))
        #print(page_no)
        context['pdf_name']=pdf_name
        context['page_no']=page_no
        
        context['image']=self.getImage(pdf_name,page_no)
        context['next_page_no']=page_no+1
        context['prev_page_no']=page_no-1 if (page_no-1 )>=0 else 0
        return context

    def post(self,request,*args,**kwargs):
        data=request.POST
        loan_number=data.get('loan_number')
        doc_id=data.get('doc_id')
        pdf_name=kwargs.get('image_path')
        page_no=kwargs.get('page_no')
        print(f"Loan:{loan_number}\ndocID:{doc_id}\nPDF_NAME: {pdf_name}\npage_no :{page_no}")
        cache_key=f"{pdf_name}_{page_no}"
        print(pdf_name,cache.get(pdf_name))
        cache.set(cache_key,{'loan_number':loan_number,'doc_id':doc_id,'pdf_name':pdf_name,'page_no':page_no})
        if int(cache.get(pdf_name)['total_pages'])-1>page_no:
            page_no+=1
            '''
            context={
                'image_path':pdf_name,
                'page_no':page_no,
                'next_page_no':page_no+1,
                'prev_page_no':page_no-1,
                'image':self.getImage(pdf_name,page_no)
            }
            '''
            #return self.render_to_response(context)
            return redirect('test',image_path=pdf_name,page_no=page_no)
        else:
            print("last page")
    
    def getImage(self,pdf_nm,page_no):
        file_path="C:\DEV_TEMP\TEMP\\"
        file_nm="page_"
        file_path+=file_nm+str(page_no)+'.jpg'
        with open(file_path,'rb') as img:
            img_data=img.read()
        img_data=base64.b64encode(img_data).decode('utf-8')
        print(f"Rendering {pdf_nm} for page {page_no}")
        return img_data
        
