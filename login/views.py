from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login as auth_login


# #login views
def login(request):
    if request.method=='POST':

        username=request.POST.get('username')
        password=request.POST.get('password')

        if username=="" or password=="":
           warn="Please fill all the field"
           return render(request,'login.html',context={'error':warn})
        
        else:
            user=authenticate(request,username=username,password=password)
    
            if user is None:
               warn="Credential Doesnot Match"
               return render(request,'login.html',context={'error':warn})

        auth_login(request,user)
        return HttpResponseRedirect('/dataset')
    return render(request,'login.html')



def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/login')


