

import numpy as np
import cv2
from keras.models import load_model
font = cv2.FONT_HERSHEY_SIMPLEX
import urllib.request
from time import sleep
import os 

from pydoc import doc
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from pdf2image import convert_from_path
from .models import Profile,CheckResume
from django.utils.datastructures import MultiValueDictKeyError


from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



## load Model


def grayscale(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img

def equalize(img):
    img =cv2.equalizeHist(img)
    return img

def preprocessing(img):
    img = grayscale(img)
    img = equalize(img)
    img = img/255
    return img

def getCalssName(classNo):
    if   classNo == 0: return 'organisé'
    elif classNo == 1: return 'non organisé'



def Classification(request):
    current_user=request.user.id
    print("current user",current_user)
    try:
        if request.method=="POST":
            profile=Profile()
            docfile=request.FILES['docfile']

            try :
                profile=Profile.objects.get(user=request.user.id)
                profile.cv=docfile
                profile.save()
            except Profile.DoesNotExist:
                profile=Profile.objects.create(user=request.user.id,cv=docfile)
                profile.save()

            path=os.path.join(os.getcwd(),"core","media")
            convert_image_path=os.path.join(os.getcwd(),"convertpdf")
            model_path=os.path.join(os.getcwd(),"apps","home")
            
            pages = convert_from_path(path+"/"+str(profile.cv), 500)
            
            for page in pages:
                page.save(convert_image_path+"/"+'out.png', 'PNG')
            
            model=load_model(model_path+"/"+"model1.h5")
            imgOrignal=cv2.imread(convert_image_path+"/"+'out.png')
            img = np.asarray(imgOrignal)
            img = cv2.resize(img, (300, 300))
            img = preprocessing(img)
            img = img.reshape(1, 300, 300, 1)
            # PREDICT IMAGE
            predictions = model.predict(img)
            classIndex = model.predict_classes(img)
            probabilityValue =np.amax(predictions,axis=1)
            print(probabilityValue)
            if probabilityValue > 0.5:
                try:
                    check=CheckResume.objects.get(user=request.user.id)
                    check.statut=str(getCalssName(classIndex))
                    check.score=round(probabilityValue[0]*100,2)
                    check.save()
                except CheckResume.DoesNotExist:
                    check=CheckResume.objects.create(user=request.user.id,statut=str(getCalssName(classIndex)),score=round(probabilityValue[0]*100,2))
                
                
                
                
                context = {
                    "probabilityValue":str(round(probabilityValue[0]*100,2)),
                    "classification":str(getCalssName(classIndex)),
                    "profile":profile,
                    }
                
                
                html_template = loader.get_template('home/dashboard.html')
                return HttpResponse(html_template.render(context, request))
    except MultiValueDictKeyError :
        return HttpResponseRedirect("/resume_classification")
        
        
    classifications=CheckResume.objects.all()
    profiles=Profile.objects.all()
    context = {"classifications":classifications,"profiles":profiles}
    
    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))



    