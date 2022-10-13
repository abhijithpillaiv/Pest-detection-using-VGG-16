from django.shortcuts import render,redirect,get_object_or_404,reverse
from modules.forms import ListForm,ListForm1,ListForm3,ListForm4
from modules.models import feed,user_login,userreg,farmerreg,krishireg1,farmerrequest1,krishreply,pfeedback1
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.template  import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.db.models import Max
from datetime import datetime,timedelta,date
import os
import cv2
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from django.shortcuts import render
from keras.models import model_from_json
from keras.preprocessing import image
from django.core.files.storage import FileSystemStorage
from skimage import io
from keras.utils import load_img,img_to_array
from keras.models import load_model
import numpy as np
from keras.preprocessing import image

pest_pred = ['aphids','armyworm','beetle','bollworm','grasshopper','mites','mosquito','sawfly','stem_borer']
IMAGE_SIZE = 224
vgg16_model = 'modules/model_weights/MobileNetModel/model.hdf5'
vgg16_json = 'modules/model_weights/MobileNetModel/model.json'


def home(request):
     return render(request,'index.html')
def aboutus(request):
     return render(request,'about.html')
def contactus(request):
     return render(request,'contact-us.html')
def login(request):
     return render(request,'login.html')
def success(request):
     return render(request,'successful.html')
def invalid(request):
     return render(request,'invalid.html')     
def admin(request):
     return render(request,'adminindex.html')
def farmer(request):
     return render(request,'farmer.html')
def user(request):
     return render(request,'user.html')
def krishi(request):
     return render(request,'krishibhavan.html')
def userhome(request):
     return render(request,'userhome.html')
def farmerhome(request):
     return render(request,'farmerhome.html')
def krishihome(request):
     return render(request,'krishihome.html')
def feedback(request):
     return render(request,'feedback.html')

 
def read_image(filepath):
    return cv2.imread(filepath) 

def resize_image(image, image_size):
    return cv2.resize(image.copy(), image_size, interpolation=cv2.INTER_AREA)

def clear_mediadir():
    media_dir = "./media"
    for f in os.listdir(media_dir):
        os.remove(os.path.join(media_dir, f))
             
def img(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        img_path = fs.path(filename)

        pred_arr = np.zeros(
            (1, IMAGE_SIZE, IMAGE_SIZE, 3))

        im = read_image(img_path)
        if im is not None:
            pred_arr[0] = resize_image(im, (IMAGE_SIZE, IMAGE_SIZE))
        
        pred_arr = pred_arr/255
        
        vgg_start = time.time()
        with open(vgg16_json, 'r') as vggjson:
            vgg16model = model_from_json(vggjson.read())

        vgg16model.load_weights(vgg16_model)
        label_vgg = vgg16model.predict(pred_arr)
        idx_vgg = np.argmax(label_vgg[0])
        cf_score_vgg = np.amax(label_vgg[0])
        vgg_end = time.time()

        vgg_exec = vgg_end  - vgg_start
        

        print('Prediction (VGG16): ', idx_vgg)
        print("\n")
        print(img_path)

        response = {}
        response['table'] = "table"
        response['col0'] = " "
        response['col1'] = "VGG16"
        response['row1'] = "Results"
        response['row2'] = "Confidence Score"
        response['row3'] = "Prediction Time (s)"
        response['v_pred'] = pest_pred[idx_vgg]
        response['x_pred'] = im
        response['v_cf'] = cf_score_vgg
        response['image'] = fs.url(filename)
        return render(request, 'img.html', response)
    else:
        return render(request, 'img.html')
    return render(request,'img.html')     


def admin_login(request):

    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(username=un, pass1=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].username
            request.session['user_id'] = ul[0].id
            return render(request,'adminindex.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, 'login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, 'login.html',context)    


        
def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)



def user_details_add(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')   
        pass1= request.POST.get('pass1')
        
        status = "new"
        if userreg.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('invalid')  

        ul = user_login(username=username, pass1=pass1, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = userreg(user_id=user_id,name=name,
                               email=email,username=username,pass1=pass1,status=status,)
        ud.save()

        print(user_id)
        context = { 'msg': 'Record Added'}
        return render(request, 'successful.html',context)

    else:
        return render(request, 'userreg.html')


def user_login_check(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(username=un, pass1=pwd, u_type='user')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].username
            request.session['user_id'] = ul[0].id
            return render(request,'userhome.html')
        else:
            msg = 'Invalid Uname or Password !!!'
            context ={ 'msg':msg }
            return render(request, 'userlogin.html',context)
    else:
        msg = ''
        context ={ 'msg':msg }
        return render(request, 'userlogin.html',context)        
        

    


def farmer_details_add(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        place = request.POST.get('place')
        pincode = request.POST.get('pincode')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        

        if farmerreg.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('invalid')  

       

        ul = user_login(username=username, pass1=pass1, u_type='farmer')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = farmerreg(user_id=user_id,name=name,address=address,phone=phone,place=place,pincode=pincode,
                              email=email,pass1=pass1,username=username)
        ud.save()

        print(user_id)
        context = { 'msg': 'Record Added'}
        return render(request, 'index.html',context)

    else:
        return render(request, 'farmerreg.html')




def farmer_login_check(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(username=un, pass1=pwd, u_type='farmer')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].username
            request.session['user_id'] = ul[0].id
            return render(request,'farmerhome.html')
        else:
            msg = 'Invalid Uname or Password !!!'
            context ={ 'msg':msg }
            return render(request, 'farmerlogin.html',context)
    else:
        msg = ''
        context ={ 'msg':msg }
        return render(request, 'farmerlogin.html',context)    


def farmer_changepassword(request):
    if request.method == 'POST':
        username = request.session['user_name']
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('new_password1')
        current_password = request.POST.get('current_password')
        id = request.session['user_id']
        print("username:::" + username)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.filter(id = int(id)).values().first()
            
            if ul is not None:
                if ul['pass1'] == current_password:
                    if new_password == confirm_password:

                        ul = user_login.objects.filter(id = int(id)).update(pass1=new_password)
                        context = {'msg':'Password Changed Successfully'}
                        return render(request, 'farmerhome.html',context)
                    else:
                        context = {'msg':'Password are not same'}
                        return render(request, 'user_changepassword.html', context)
                else:
                    context = {'msg':'Wrong Password'}
                    return render(request, 'user_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, 'user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, 'user_changepassword.html', context)
    else:
        return render(request, 'user_changepassword.html')

def krishi_details_add(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        
        status = 0
        if userreg.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('invalid')  


        ul = user_login(username=username, pass1=pass1, u_type='krishi')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = krishireg1(user_id=user_id,name=name,address=address,phone=phone,city=city,pincode=pincode,
                              email=email,pass1=pass1,username=username,status=status)
        ud.save()

        print(user_id)
        context = { 'msg': 'Record Added'}
        return render(request, 'index.html',context)

    else:
        return render(request, 'kreg.html')


def krishi_login_check(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition


        ul = user_login.objects.filter(username=un, pass1=pwd, u_type='krishi')
        if ul:
            krishi_status = krishireg1.objects.filter(user_id= ul[0].id,status=True)
            if krishi_status:
                request.session['user_name'] = ul[0].username
                request.session['user_id'] = ul[0].id
                return render(request,'krishihome.html')
            else:
                msg = 'Krishibhavan is not Approved'
                context = {'msg':msg}
                return render(request, 'krilogin.html',context)
        else:
            msg = 'Invalid Uname or Password !!!'
            context ={ 'msg':msg }
            return render(request, 'krilogin.html',context)
    else:
        return render(request, 'krilogin.html')      
  

def userview(request):
    all=userreg.objects.all()
    return render(request,'userview.html',{'disp':all})


def farmerview(request):
    all=farmerreg.objects.all()
    return render(request,'farmerview.html',{'disp':all})

    
def feedback(request):
     if request.method =="POST":
         form =ListForm4(request.POST)
         if form.is_valid():
            form.save()
         return redirect('userhome')
     else:
        form =ListForm4()
     return render(request,'feedback.html',{"form":form})

def search(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        sh_l =krishireg1.objects.filter(city__contains=query)
        context = {'krishi': sh_l}
        return render(request, 'farmerkrishiview.html', context)

    else:
        return render(request, 'search.html')

   

def approve_krishi_view(request,pk):
    krishi=krishireg1.objects.get(id=pk)
    krishi.status=True
    krishi.save()
    return redirect(reverse('admin_kview'))


def krishideletedata(request,pk):
    data=get_object_or_404(krishireg1,pk=pk)
    if request.method=='POST':
        data.delete()
        return redirect('admin_kview')
    return render(request,'delete.html',{'delete1':data})

def krishiview(request):
    krishi=krishireg1.objects.all().filter(status=False)
    return render(request,'adminapprove.html',{'krishi':krishi})
     

def krishi_approved_view(request):
    krishi=krishireg1.objects.all().filter(status=True)
    return render(request,'adminapprovekrishi.html',{'krishi':krishi})


def userdelete(request,pk):
    data=get_object_or_404(userreg,pk=pk)
    if request.method=='POST':
        data.delete()
        return redirect('admin_userview')
    return render(request,'userdelete.html',{'delete1':data})

def farmerdelete(request,pk):
    data=get_object_or_404(farmerreg,pk=pk)
    if request.method=='POST':
        data.delete()
        return redirect('admin_farmerview')
    return render(request,'farmerdelete.html',{'delete1':data})

def  farmer_request(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        user_id = int(request.session['user_id'])
        name =request.POST.get('name')
        email =request.POST.get('email')
        description= request.POST.get('description')
        dt = datetime.today().strftime('%Y-%m-%d')
        status="pending"
        jm = farmerrequest1(user_id=user_id,kid_id=id,name=name,email=email,description=description,dt=dt,status=status)
        jm.save()
        context = {'msg': 'New News Response Added'}
        return render(request, 'farmerhome.html', context)
    else:
        id=request.GET.get("id")
        context = {'msg': 'not added',"id":id}
        return render(request, 'solution.html',context)

def krishiviewrequest(request):
    user_id = request.session['user_id']
    print("id1:",user_id)
    data_1=krishireg1.objects.get(user_id=user_id)
    data=farmerrequest1.objects.filter(kid_id=data_1.id)
    return render(request,'krishifarmerrequest.html',{"data":data})

def farmer_request_view(request):
    user_id = request.session['user_id']
    jm_l =farmerrequest1.objects.filter(user_id=int(user_id))
    krishi = krishireg1.objects.all()
    context = {'farmer': jm_l, 'msg': '', 'krishi':krishi}
    return render(request, 'farmerrequestview.html', context)

def  krishi_reply(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        user_id = int(request.session['user_id'])
        description= request.POST.get('description')
        dt = datetime.today().strftime('%Y-%m-%d')
        status="replayed"
        jm = krishreply(user_id=user_id,farmer_id_id=id,description=description,dt=dt,status=status)
        jm.save()
        context = {'msg': 'New News Response Added'}
        return render(request, 'krishihome.html', context)
    else:
        id=request.GET.get("id")
        context = {'msg': 'not added',"id":id}
        return render(request, 'krishireply.html',context)


def farmerviewreply(request):
    user_id = request.session['user_id']
    print("id1:",user_id)
    data_1=farmerrequest1.objects.get(user_id=user_id)
    data=krishreply.objects.filter(kid_id=data_1.id)
    return render(request,'farmerviewreply.html',{"data":data})

#own profile view
#farmer


def profile(request):
    user_id = request.session['user_id']
    jm_l =farmerreg.objects.filter(user_id=int(user_id))
    context = {'farmer': jm_l, 'msg': ''}
    return render(request, 'profile.html', context)


#profile edit
def profile_edit(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        name= request.POST.get('name')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        email= request.POST.get('email')
        place= request.POST.get('place')
        pincode= request.POST.get('pincode')
        username= request.POST.get('username')
        jm = farmerreg.objects.get(user_id=int(user_id))
        jm.name = name
        jm.address = address
        jm.phone = phone
        jm.email = email
        jm.place=place
        jm.pincode = pincode
        jm.username=username
        jm.save()

        msg = 'News Record Updated'
        user_id = int(request.session['user_id'])
        jm_l = farmerreg.objects.filter(user_id=user_id)
        context = {'farmer': jm_l, 'msg': msg}
        return render(request, 'profile.html', context)

#krishibhavan        

def kprofile(request):
    user_id = request.session['user_id']
    jm_l =krishireg1.objects.filter(user_id=int(user_id))
    context = {'krishi': jm_l, 'msg': ''}
    return render(request, 'krishiprofile.html', context)



    #krishiprofile edit
def krishiprofile_edit(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        name= request.POST.get('name')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        email= request.POST.get('email')
        city= request.POST.get('city')
        pincode= request.POST.get('pincode')
        username= request.POST.get('username')
        jm = krishireg1.objects.get(user_id=int(user_id))
        jm.name = name
        jm.address = address
        jm.phone = phone
        jm.email = email
        jm.city =city
        jm.pincode = pincode
        jm.username=username
        jm.save()

        msg = 'News Record Updated'
        user_id = int(request.session['user_id'])
        jm_l = krishireg1.objects.filter(user_id=user_id)
        context = {'krishi': jm_l, 'msg': msg}
        return render(request, 'krishiprofile.html', context)


#user       

def uprofile(request):
    user_id = request.session['user_id']
    jm_l =userreg.objects.filter(user_id=int(user_id))
    context = {'user': jm_l, 'msg': ''}
    return render(request, 'userprofile.html', context)



    #user edit
def userprofile_edit(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        name= request.POST.get('name')
        email= request.POST.get('email')
        username= request.POST.get('username')
        jm = userreg.objects.get(user_id=int(user_id))
        jm.name = name
        jm.email = email
        jm.username=username
        jm.save()

        msg = 'News Record Updated'
        user_id = int(request.session['user_id'])
        jm_l = userreg.objects.filter(user_id=user_id)
        context = {'user': jm_l, 'msg': msg}
        return render(request, 'userprofile.html', context)
        
def krishi_notification(request):
    user_id = krishireg1.objects.filter(user_id = int(request.session['user_id'])).values('id').first()
    
    ins_farmer = list(farmerrequest1.objects.filter(kid = user_id['id'],status="pending").values('name','email','description','dt','id'))
    return render(request,'krishi_notification.html',{'data':ins_farmer})



def savereply(request):
    if request.method == 'POST':
        if request.POST.get('replymsg'):
            ins_farmer = farmerrequest1.objects.filter(id = request.POST.get('row_id')).update(status = 'Replied',reply_msg = request.POST.get('replymsg'))
            if ins_farmer:
                return redirect(krishi_notification)
        else:
            return redirect(krishi_notification)

def patientfeedback(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        description= request.POST.get('description')
        dt = datetime.today().strftime('%Y-%m-%d')
        
        jm = pfeedback1(user_id=user_id,description=description,dt=dt)
        jm.save()
        context = {'msg': 'New News Response Added'}
        return render(request, 'farmerhome.html', context)
    else:
        context = {'msg': 'not added'}
        return render(request, 'patient_feedback.html',context)
def patient_feedback_view(request):
    user_id = int(request.session['user_id'])
    jm_l = pfeedback1.objects.filter(user_id=user_id).values()
    lst_data=[]
    for i in jm_l:
        dct_data={}
        dct_data['id'] = i['id']
        dct_data['description'] = i['description']
        dct_data['dt'] = i['dt']
        dct_data['user_id'] = i['user_id']
        dct_data['reply'] = i['reply']
        if i['status'] == True:
            dct_data['status'] =1
        else:
            dct_data['status'] = 0
        lst_data.append(dct_data)
        
    patient_list = farmerreg.objects.all()
    context = {'feedback_list':lst_data,'patient_list':patient_list}
    return render(request, 'patient_view_feedback.html',context)

def admin_view_feedback(request):
    jm_l = pfeedback1.objects.all()
    patient_list = farmerreg.objects.all()
    context =  {'feedback_list':jm_l,'patient_list':patient_list}
    return render(request, 'admin_view_patient_feedback.html',context)        

def admin_reply(request,id):
   # import pdb;pdb.set_trace()
    ins_id = id
    return render(request,'admin_reply.html',{'id':ins_id})

def reply(request,id):
    ins_id = id
    reply = request.POST.get('reply')
    ins_feedback = pfeedback1.objects.filter(id=ins_id).update(reply=reply,status=1)
    return redirect('admin-view-feedback')

def admin_view_solution(request):
    jm_l =all=farmerrequest1.objects.all()
    krishi = krishireg1.objects.all()
    context = {'farmer': jm_l, 'msg': '', 'krishi':krishi}
    return render(request, 'adminviewrequest.html', context)

    

def logout_request(request):
       
    return redirect('home')  



