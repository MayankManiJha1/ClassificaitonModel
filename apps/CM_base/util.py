import os
import shutil
import traceback
#from send2trash import send2trash
import PyPDF2
from pdf2image import convert_from_path


def copy_file(cpath,MEDIA):
    abs_path=os.path.abspath(cpath)
    final_path= os.path.join(MEDIA,os.path.basename(abs_path))
    if os.path.exists(final_path):
        send2trash(final_path)
    shutil.copy(cpath,MEDIA)
    return final_path

def split(file_path,out_path):
    try:
        print("files to be split:",file_path)
        images = convert_from_path(file_path)
        for i in range(len(images)):
            images[i].save(out_path+'page_'+str(i) +'.jpg', 'JPEG')
    except:
        traceback.print_exc()
