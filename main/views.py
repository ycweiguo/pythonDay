from django.shortcuts import render
import json
from users.models import User

# Create your views here.
def index(request):
    return render(request,'basemain.html')
def accounts_profile(request):
    if request.method == 'POST':
        print( request.body)
        body1 = request.body.decode('utf-8')
        a = json.loads(body1)
        print(a)
        b = User.objects.get(email=request.user.email)
        b.phone=a['phone']
        b.save()
    return render(request,'accounts_profile.html')