from django.shortcuts import render, redirect
from .models import Photo, PhotoShare
from django.http import JsonResponse,HttpResponse
from django.core import serializers
import json
# Create your views here.

def gallery(request):
    if request.method == "POST":
        data = request.POST
        search = data['search']
        if search == "" :
            photos = Photo.objects.all()
        else :
            photos = Photo.objects.filter(description__contains = search)
    else :
        photos = Photo.objects.all()
    
    context = {'photos' : photos}
    return render(request,'photos/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {"photo" : photo}
    return render(request,'photos/photo.html',context)

def diaporamaPhoto(request,pk):
    photo = Photo.objects.get(id=pk)
    photos = Photo.objects.all()
    context = {"photo" : photo,'photos' : photos}
    return render(request,'photos/diaporama.html',context)

def addPhoto(request):
    if request.method == "POST":
        data = request.POST
        images = request.FILES.getlist("images")

        for image in images :
            photo = Photo.objects.create(
                description = data["description"],
                image = image,
            )
        return redirect('gallery')

    return render(request,'photos/add.html')

def suppPhoto(request,pk):
    photo = Photo.objects.get(id=pk)

    if request.method =="POST" :
        photo.delete()
        return redirect('gallery')
    
    return render(request,'photos/add.html')

def editPhoto(request,pk):
    photo=Photo.objects.get(id=pk)

    if request.method == "POST":
        data = request.POST
        description = data["description"]
        photo.description = description
        photo.save()

        return redirect('/photo/'+str(photo.id))

    return render(request,'photos/editPhoto.html',{'photo' : photo})
    
def sharePhoto(request):
    photos = Photo.objects.all()

    try :
        currentid = PhotoShare.objects.get(id=1)
    except:
        currentid = PhotoShare.objects.create(
                current_id = photos.first().id,
            )
    print('currentid : ' + str(currentid.current_id))

    context = {'photos' : photos}
    return render(request,'photos/share.html', context)

def getSharePhoto(request):

    photos = Photo.objects.all()
    currentid = PhotoShare.objects.get(id=1)
    currentPhoto = {}

    print("current_id"+str(currentid.current_id))

    for photo in list(photos.values()):
        if photo['id'] == currentid.current_id :
            currentPhoto = photo
    
    return JsonResponse({"photo" : currentPhoto})

def postSharePhoto(request):
    currentid = PhotoShare.objects.get(id=1)
    photos = Photo.objects.all()
    if request.method == "POST":
            data = request.POST
            try:
                move = data['move']
                print('inside try : ' + move)

                if (move == "1"):
                    print('inside move = 1 :')

                    if currentid.current_id==photos.first().id :
                        currentid.current_id=photos.last().id

                    else :
                        currentphoto=Photo.objects.get(id=currentid.current_id)
                        i=0
                        for index,photo in enumerate(photos):
                            if photo == currentphoto :
                                i=index
                                print('index found : ' + str(i))
                        currentid.current_id=photos[i-1].id
                    currentid.save()
                    print('currentid : ' + str(currentid.current_id))

                if (move == "2"):
                    print('inside move = 2 :')

                    if currentid.current_id==photos.last().id :
                        currentid.current_id=photos.first().id

                    else :
                        currentphoto=Photo.objects.get(id=currentid.current_id)
                        i=0
                        for index,photo in enumerate(photos):
                            if photo == currentphoto :
                                i=index
                                print('index found : ' + str(i))
                        currentid.current_id=photos[i+1].id
                    currentid.save()
                    print('currentid : ' + str(currentid.current_id))
            
            except KeyError:
                print('Error')
            return HttpResponse('move sucess')