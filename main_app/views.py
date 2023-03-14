from django.shortcuts import render, redirect
from .models import Apparel, Outfit, User, UserProfile, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from main_app.forms import ApparelForm 
import uuid #creates our unique ids for 
import boto3 #connects us to s3
from django.conf import settings

# AWS s3 KEYS
AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
S3_BUCKET = settings.S3_BUCKET
S3_BASE_URL = settings.S3_BASE_URL

# Create your views here.

def home(request):
    return render(request, 'home.html')


# APPAREL VIEWS
# display all apparels 
def apparels_index(request):
    apparels = Apparel.objects.filter(user=request.user)

    return render(request, 'apparels/index.html', { 'apparels': apparels})
# display one apparel item
def apparels_detail(request, apparel_id):
    apparel = Apparel.objects.get(id=apparel_id)

    return render(request, 'apparels/detail.html', { 'apparel': apparel })


class ApparelCreate(CreateView):
    model = Apparel
    fields = ['name', 'brand', 'color', 'size', 'style', 'type']
    # apparel_form = ApparelForm
    def form_valid(self, form):
    # self.request.user is assigning the user
        form.instance.user = self.request.user  
        return super().form_valid(form)

# apparels can update everything except the type field
class ApparelUpdate(UpdateView):
    model = Apparel
    fields = ['name', 'brand', 'color', 'size', 'style']

class ApparelDelete(DeleteView):
    model = Apparel
    success_url = '/apparels/'


#OUTFIT VIEWS

# this index represents the inspo page (all user outfits will be here)
def outfits_index(request):
    outfits = Outfit.objects.all()

    return render(request, 'outfits/index.html', { 'outfits': outfits})

# displays only the users outfits
def outfits_user_index(request):
    outfits = Outfit.objects.filter(user=request.user)

    return render(request, 'outfits/user_index.html', { 'outfits': outfits})

# view one outfit 
def outfits_detail(request, outfit_id):
    outfit = Outfit.objects.get(id=outfit_id)

    id_list = outfit.apparels.filter(user=request.user).values_list('id')

    unused_apparels = Apparel.objects.exclude(id__in=id_list)
    photos = Photo.objects.all()

    return render(request, 'outfits/detail.html', {'outfit': outfit, 'apparels': unused_apparels, 'photos':photos })

class OutfitCreate(CreateView):
    model = Outfit
    fields = ['name', 'date', 'event', 'caption']

    def form_valid(self, form):
    # self.request.user is assigning the user
        form.instance.user = self.request.user  
        return super().form_valid(form)

class OutfitUpdate(UpdateView):
    model = Outfit
    fields = ['name', 'date', 'event', 'caption']

class OutfitDelete(DeleteView):
    model = Outfit
    success_url = '/outfits/'

# the assoc apparel func will handle when apparels are added to an outfit
def assoc_apparel(request, outfit_id, apparel_id):
    Outfit.objects.get(id=outfit_id).apparels.add(apparel_id)
    return redirect('outfits_detail', outfit_id=outfit_id)

# the unassoc apparel func will handle removing apparels from an outfit 
def unassoc_apparel(request, outfit_id, apparel_id):
    Outfit.objects.get(id=outfit_id).apparels.remove(apparel_id)
    return redirect('outfits_detail', outfit_id=outfit_id)


#USER VIEWS
# sign up 
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def user_profile(request, user_id):
    user = User.objects.get(id=user_id)

    return render(request, 'accounts/user_profile.html', {'user': user, })

class ProfileUpdate(UpdateView):
    model = User
    fields = ['body_type', 'color_palette', 'top_styles', 'profile_img']


# Adding a View for Apparel Photos 
def add_photo(request, apparel_id):
    photo_file = request.FILES.get('photo-file', None)
    # If photo is present, make reference to boto3 and create unique id for photo
    if photo_file:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # handling success/failure
        try:
            # build url string for upload to s3
            s3.upload_fileobj(photo_file, S3_BUCKET, key)
            url = f"{S3_BASE_URL}{S3_BUCKET}/{key}"
            # create photo model using photo location then save
            photo = Photo(url=url, apparel_id=apparel_id)
            photo.save()
        except Exception as error:
            # print an error message
            print('Error uploading photo', error)
            return redirect('detail', apparel_id=apparel_id)
    # success = redirect to detail
    return redirect('detail', apparel_id=apparel_id)