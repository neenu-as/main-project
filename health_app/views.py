import datetime
import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from health_app.encode_faces import enf
from health_app.models import *
from health_app.recognize_face import rec_face_image


def firstpage(request):
    return render(request,"Admin/homepageindex.html")
@login_required(login_url='/')
def home(request):
    return render(request,"Admin/index.html")

@login_required(login_url='/')
def home2(request):
    return render(request,"Admin/index2.html")

def login(request):
    return render(request,"Admin/loginindex.html")
def logout(request):
    auth.logout(request)
    return render(request,"Admin/loginindex.html")


def logincode(request):
    a=request.POST['textfield']
    b=request.POST['textfield2']

    try:
        ob = login_table.objects.get(Username=a, password=b)
        if(ob.Username==a and ob.password==b):
            if ob.type == 'admin':
                ob1=auth.authenticate(username="123",password="123")
                if ob1 is not None:
                    auth.login(request,ob1)
                request.session['lid']=ob.id
                return HttpResponse('''<script>alert("welcome to admin home");window.location='/home2'</script>''')

            else:
                return HttpResponse('''<script>alert("invalid login");window.location='/login'</script>''')
        else:
            return HttpResponse('''<script>alert("invalid login");window.location='/login'</script>''')

    except:
        return HttpResponse('''<script>alert("invalid username and passsword");window.location='/login'</script>''')


@login_required(login_url='/')
def vchangepsswd(request):
    return render(request,"Admin/changepassword.html")
@login_required(login_url='/')
def changepsswd(request):
    cpwd = request.POST['textfield']
    npwd = request.POST['textfield2']
    lid = request.session['lid']

    try:
        ob = login_table.objects.get(id=lid, password=cpwd)
        ob.password = npwd
        ob.save()
        return HttpResponse('''<script>alert("updated");window.location='/vchangepsswd'</script>''')

    except:
        return HttpResponse('''<script>alert("invalid passsword");window.location='/vchangepsswd'</script>''')










@login_required(login_url='/')
def assign_works(request):
    ob=work_table.objects.filter(status="pending",CARETAKERID__LOGINID__type='caretaker').order_by('-id')
    oo=work_table.objects.exclude(status="pending",CARETAKERID__LOGINID__type='caretaker').order_by('-id')

    my_objects=ob.union(oo)
    # my_objects = caretaker.objects.filter(fname__istartswith=fname)

    # my_objects = user.objects.all().order_by('-id')
    # Set the number of items per page
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)

    return render(request,"Admin/ASSIGN WRKS TO CARETKR.html",{"my_objects":my_objects})



@login_required(login_url='/')
def assn_work_search(request):

    try:
        date=request.POST['textfield']
        request.session['d']=date
        my_objects = work_table.objects.filter(date__istartswith=date).order_by('-id')

        # my_objects = caretaker.objects.filter(fname__istartswith=fname)

        # my_objects = user.objects.all().order_by('-id')
        # Set the number of items per page
        items_per_page = 4

        # Create a Paginator instance
        paginator = Paginator(my_objects, items_per_page)

        # Get the current page number from the request's GET parameters
        page = request.GET.get('page')

        try:
            # Get the Page object for the requested page
            my_objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            my_objects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver the last page
            my_objects = paginator.page(paginator.num_pages)


        return render(request,'Admin/ASSIGN WRKS TO CARETKR.html',{'my_objects':my_objects})
    except:
        date = request.session['d']

        my_objects = work_table.objects.filter(date__istartswith=date).order_by('-id')

        # my_objects = caretaker.objects.filter(fname__istartswith=fname)

        # my_objects = user.objects.all().order_by('-id')
        # Set the number of items per page
        items_per_page = 4

        # Create a Paginator instance
        paginator = Paginator(my_objects, items_per_page)

        # Get the current page number from the request's GET parameters
        page = request.GET.get('page')

        try:
            # Get the Page object for the requested page
            my_objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            my_objects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver the last page
            my_objects = paginator.page(paginator.num_pages)

        return render(request, 'Admin/ASSIGN WRKS TO CARETKR.html', {'my_objects': my_objects})


@login_required(login_url='/')
def add_works(request):
    ob=caretaker.objects.filter(LOGINID__type='caretaker')
    return render(request,"Admin/addworks.html",{'val':ob})
@login_required(login_url='/')
def deleteassign(request,id):
    ob=work_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted');window.location='/assign_works#about'</script>''')

@login_required(login_url='/')
def assignworkcode(request):
    select=request.POST['select']
    workk = request.POST['textfield2']
    deails = request.POST['textfield3']
    ob=work_table()
    ob.CARETAKERID=caretaker.objects.get(id=select)
    ob.work=workk
    ob.details=deails
    ob.date=datetime.datetime.today()
    ob.status="pending"
    ob.save()
    return HttpResponse('''<script>alert('Added');window.location='/assign_works#about'</script>''')


@login_required(login_url='/')
def edit_works(request,id):
    ob2 = work_table.objects.get(id=id)
    request.session['cid'] =ob2.id
    return redirect("/edit_workscodesss#about")





@login_required(login_url='/')
def edit_workscodesss(request):
    id=request.session['cid']
    print(id,'kkkkkkkkkkkkkkkk')
    ob2 = work_table.objects.get(id=id)
    ob=caretaker.objects.all()
    return render(request,'Admin/editworks.html', {'val': ob2,"car":ob})


@login_required(login_url='/')
def editwork(request):
    select=request.POST['select']
    workk = request.POST['textfield2']
    deails = request.POST['textfield3']
    ob=work_table.objects.get(id=request.session['cid'])
    ob.CARETAKERID=caretaker.objects.get(id=select)
    ob.work=workk
    ob.details=deails
    ob.date=datetime.datetime.today()
    ob.status="pending"
    ob.save()
    return HttpResponse('''<script>alert('Edit');window.location='/assign_works#about'</script>''')




@login_required(login_url='/')
def chatwith_cartkr(request):
    return render(request,"Admin/CHAT WITH CARETAKER.html")

@login_required(login_url='/')
def manag_caminfo(request):
    ob = camera.objects.all()
    return render(request,"Admin/MANAGE CAM INFO.html",{'val':ob})

@login_required(login_url='/')
def add_cam(request):
     ob=camera.objects.all()
     return render(request,"Admin/ADD CAM.html",{'val':ob})
@login_required(login_url='/')
def editcam(request,id):
    request.session['camid']=id
    ob=camera.objects.get(id=id)
    return render(request,"Admin/editcam.html",{'val':ob})


@login_required(login_url='/')
def editcam_info(request):
    name=request.POST['textfield']
    location=request.POST['textfield2']
    ob=camera.objects.get(id=request.session['camid'])
    ob.camname=name
    ob.location = location
    ob.save()
    return HttpResponse('''<script>alert('EDITED');window.location='/manag_caminfo#about'</script>''')



@login_required(login_url='/')
def deletecam_info(request,id):
    ob=camera.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted');window.location='/manag_caminfo#about'</script>''')


@login_required(login_url='/')
def addcam_info(request):
    camname = request.POST['textfield']
    location = request.POST['textfield2']
    ob=camera()
    ob. camname= camname
    ob.location=location
    ob.save()
    return HttpResponse('''<script>alert('Added');window.location='/manag_caminfo#about'</script>''')












@login_required(login_url='/')
def manage_caretkr(request):
    my_objects = caretaker.objects.all().order_by('-id')
    # my_objects = user.objects.all().order_by('-id')
    # Set the number of items per page
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)
    return render(request,'Admin/manage caretaker.html',{'my_objects':my_objects})
def dlt_ckr(request,id):
    ob=login_table.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('deleted...');window.location='/manage_caretkr#about'</script>''')


@login_required(login_url='/')
def activecaretkr(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='caretaker'
    ob.save()
    return HttpResponse('''<script>alert('actived...');window.location='/manage_caretkr#about'</script>''')


@login_required(login_url='/')
def inactivecaretkr(request,id):
    ob=login_table.objects.get(id=id)
    ob.type='inactive'
    ob.save()
    return HttpResponse('''<script>alert('inactived...');window.location='/manage_caretkr#about'</script>''')



@login_required(login_url='/')
def add_caretkr(request):
    return render(request,"Admin/formindex.html")

@login_required(login_url='/')
def addcartkr(request):
    try:
        fnm=request.POST['textfield2']
        lnm = request.POST['textfield3']
        gd=request.POST['radiobutton']
        img = request.FILES['file']
        fs=FileSystemStorage()
        fn=fs.save(img.name,img)
        phn = request.POST['textfield5']
        eml = request.POST['textfield6']
        unm = request.POST['textfield7']
        psd = request.POST['textfield8']
        plce =request.POST['textfield9']
        pst =request.POST['textfield10']
        pin = request.POST['textfield11']
        qlfctn = request.POST['textfield12']

        ob=login_table()
        ob.Username=unm
        ob.password=psd
        ob.type="caretaker"
        ob.save()

        obu=caretaker()
        obu.fname=fnm
        obu.lname=lnm
        obu.gender=gd
        obu.phone = phn
        obu.email = eml
        obu.photo = fn
        obu.place= plce
        obu.post = pst
        obu.pin = pin
        obu.qualification = qlfctn
        obu.join_date = datetime.datetime.today()
        obu.LOGINID=ob
        obu.save()
        return HttpResponse('''<script>alert('Added');window.location='/manage_caretkr#about'</script>''')
    except Exception as e:
        print(e,"--------------------------------")
        return HttpResponse('''<script>alert('Duplicate entry');window.location='/manage_caretkr#about'</script>''')




@login_required(login_url='/')
def edit_caretkr(request,id):
    ob2 = caretaker.objects.get(id=id)
    request.session['cid'] =ob2.id
    return redirect("/edit_caretkr1#about")


@login_required(login_url='/')
def edit_caretkr1(request):
    id=request.session['cid']
    ob2 = caretaker.objects.get(id=id)
    request.session['cid']=ob2.id
    return render(request,'Admin/editcaretakr_new.html',{'val':ob2})

@login_required(login_url='/')
def edit_crtkr(request):
    if 'file' in request.FILES:
        fnm = request.POST['textfield2']
        lnm = request.POST['textfield3']
        gd = request.POST['radiobutton']
        img = request.FILES['file']
        fs = FileSystemStorage()
        fsave = fs.save(img.name, img)
        phn = request.POST['textfield5']
        eml = request.POST['textfield6']
        plce = request.POST['textfield9']
        pst = request.POST['textfield10']
        pin = request.POST['textfield11']
        qlfctn = request.POST['textfield12']
        ob = caretaker.objects.get(id= request.session['cid'])
        ob.fname = fnm
        ob.lame = lnm
        ob.gender = gd
        ob.photo=fsave
        ob.phone=phn
        ob.email=eml
        ob.place = plce
        ob.post = pst
        ob.pin = pin
        ob.qualification = qlfctn
        ob.save()
        return HttpResponse(''' <script>alert("edited");window.location="/manage_caretkr#about"</script>''')
    else:

        fnm = request.POST['textfield2']
        lnm = request.POST['textfield3']
        gd = request.POST['radiobutton']
        phn = request.POST['textfield5']
        eml = request.POST['textfield6']
        plce = request.POST['textfield9']
        pst = request.POST['textfield10']
        pin = request.POST['textfield11']
        qlfctn = request.POST['textfield12']
        ob = caretaker.objects.get(id= request.session['cid'])
        ob.fname = fnm
        ob.lname = lnm
        ob.gender = gd
        ob.phone=phn
        ob.email = eml
        ob.place = plce
        ob.post = pst
        ob.pin = pin
        ob.qualification = qlfctn
        ob.save()
        return HttpResponse(''' <script>alert("edited");window.location="/manage_caretkr#about"</script>''')


@login_required(login_url='/')
def search_crtkr(request):
    fname = request.POST['textfield']
    my_objects = caretaker.objects.filter(fname__istartswith=fname)

    # my_objects = user.objects.all().order_by('-id')
    # Set the number of items per page
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)
    return render(request, 'admin/manage caretaker.html',{'my_objects':my_objects})














def p_h_reports(request):
    return render(request,"Admin/p_h_report.html")







@login_required(login_url='/')
def manage_patient_info(request):
    my_objects =  patient.objects.all().order_by('-id')
    # my_objects = user.objects.all().order_by('-id')
    # Set the number of items per page
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)
    return render(request, 'Admin/MANAGE PATIENT INFO.html', {'my_objects': my_objects})
    # ob = patient.objects.all().order_by('-id')
    # return render(request,'Admin/MANAGE PATIENT INFO.html',{'val':ob})



@login_required(login_url='/')
def manage_patient_info_update_death(request,id):
    ob = patient.objects.filter(id=id).update(type="no more")
    return HttpResponse(''' <script>alert("updated");window.location="/manage_patient_info#about"</script>''')



@login_required(login_url='/')
def manage_patient_info_search(request):
    name=request.POST['textfield']
    my_objects = patient.objects.filter(fname__istartswith=name).order_by('-id')
    # my_objects = caretaker.objects.filter(fname__istartswith=fname)

    # my_objects = user.objects.all().order_by('-id')
    # Set the number of items per page
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)
    return render(request, 'admin/MANAGE PATIENT INFO.html', {'my_objects': my_objects})


# return render(request,'Admin/MANAGE PATIENT INFO.html',{'val':ob})



@login_required(login_url='/')
def add_patient_info(request):
    ob=caretaker.objects.filter(LOGINID__type='caretaker')
    return render(request,"Admin/add patient info.html",{'val':ob})


@login_required(login_url='/')
def addpatientinfo(request):
        fnm=request.POST['textfield2']
        lnm = request.POST['textfield']
        gd=request.POST['radiobutton']
        age=request.POST['textfield3']
        img = request.FILES['file2']
        fs=FileSystemStorage()
        fn=fs.save(img.name,img)
        crtkr = request.POST['select']
        hlth_cndtn = request.POST['textfield4']
        dt = request.POST['textfield40']

        obu=patient()
        obu.fname=fnm
        obu.lname=lnm
        obu.gender=gd
        obu.age = age
        obu.photo = fn
        obu.admit_date = dt
        obu.type="alive"
        obu.CARETAKERID= caretaker.objects.get(id=crtkr)
        obu.healthcondition = hlth_cndtn

        obu.save()

        data = patient.objects.all()
        result = []
        for i in data:
            print(i.photo)
            print(i.id)
            row = [i.id, "media/" + str(i.photo)]
            result.append(row)
        enf(result)

        return HttpResponse('''<script>alert('added');window.location='/manage_patient_info#about'</script>''')


@login_required(login_url='/')
def editpatientinfo_post(request):
    try:
        fnm = request.POST['textfield2']
        lnm = request.POST['textfield']
        gd = request.POST['radiobutton']
        age = request.POST['textfield3']
        crtkr = request.POST['select']
        hlth_cndtn = request.POST['textfield4']
        dt = request.POST['textfield40']
        # obu = patient()
        # obu.fname = fnm
        # obu.lname = lnm
        # obu.gender = gd
        # obu.age = age
        # if 'file' in request.FILES:
        img = request.FILES['file2']
        fs = FileSystemStorage()
        fn = fs.save(img.name, img)
        # obu.photo = fn
        # obu.CARETAKERID = caretaker.objects.get(id=crtkr)
        # obu.healthcondition = hlth_cndtn
        #
        # obu.save()
        patient.objects.filter(id=request.session['pid']).update(CARETAKERID = caretaker.objects.get(id=crtkr),fname = fnm,lname = lnm,gender = gd,age = age,photo = fn,healthcondition = hlth_cndtn,admit_date=dt)

        data = patient.objects.all()
        result = []
        for i in data:
            print(i.photo)
            print(i.id)
            row = [i.id, "media/" + str(i.photo)]
            result.append(row)
        enf(result)

        return HttpResponse('''<script>alert('edited');window.location='/manage_patient_info#about'</script>''')
    except Exception as e:
        print(e)
        fnm = request.POST['textfield2']
        lnm = request.POST['textfield']
        gd = request.POST['radiobutton']
        age = request.POST['textfield3']
        crtkr = request.POST['select']
        hlth_cndtn = request.POST['textfield4']
        dt = request.POST['textfield40']
        patient.objects.filter(id=request.session['pid']).update(CARETAKERID = caretaker.objects.get(id=crtkr),fname=fnm, lname=lnm, gender=gd, age=age,admit_date=dt,
                                                                 healthcondition=hlth_cndtn,)
        return HttpResponse('''<script>alert('edited');window.location='/manage_patient_info#about'</script>''')



@login_required(login_url='/')
def edit_patient_info(request,id):
    request.session['pid']=id
    return redirect('/edit_patient_info1')



@login_required(login_url='/')
def edit_patient_info1(request):
    obb=patient.objects.get(id=request.session['pid'])
    ob = caretaker.objects.all()
    return render(request,"Admin/edit patient info.html",{'val':obb,'val1':ob,'cid':obb.CARETAKERID.id,'dt':str(obb.admit_date)})


@login_required(login_url='/')
def deletepatientinfo(request,id):
    ob = patient.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted');window.location='/manage_patient_info#about'</script>''')









@login_required(login_url='/')
def medicin_notifctn(request):
        ob = medicine_notification.objects.filter(status="pending")
        x=medicine_notification.objects.filter(status="verified")

        my_objects=ob.union(x)

        # my_objects = caretaker.objects.filter(fname__istartswith=fname)

        # my_objects = user.objects.all().order_by('-id')
        # Set the number of items per page
        items_per_page = 3

        # Create a Paginator instance
        paginator = Paginator(my_objects, items_per_page)

        # Get the current page number from the request's GET parameters
        page = request.GET.get('page')

        try:
            # Get the Page object for the requested page
            my_objects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            my_objects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver the last page
            my_objects = paginator.page(paginator.num_pages)





        return render(request,"Admin/medice notification.html", {'val': ob,"my_objects":my_objects})



@login_required(login_url='/')
def medcn_notfcn_verify(request,id):
        ob = medicine_notification.objects.get(id=id)
        ob.status="verified"
        ob.save()
        return HttpResponse('''<script>alert('Verified');window.location='/medicin_notifctn#about'</script>''')


@login_required(login_url='/')
def medcn_notfcn_search(request):
    name = request.POST['textfield']
    # print(name)
    # ob = medicine_notification.objects.filter(CARETAKERID__fname__istartswith=name).order_by('-id')
    # print(ob)
    # ob = medicine_notification.objects.filter(status="pending")
    my_objects = medicine_notification.objects.filter(CARETAKERID__fname__istartswith=name)

    # my_objects = ob.union(x)
    # my_objects = medicine_notification.objects.filter(CARETAKERID__fname__istartswith=name).order_by('-id')
    # my_objects = caretaker.objects.filter(fname__istartswith=fname)

    # my_objects = user.objects.all().order_by('-id')
    # Set the number of items per page
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)
    return render(request, 'Admin/medice notification.html',{"my_objects":my_objects})






@login_required(login_url='/')
def patient_needs(request):
    ob = patients_needs.objects.filter(status="pending")
    x = patients_needs.objects.filter(status="verified")
    my_objects=ob.union(x)
    # my_objects = caretaker.objects.filter(fname__istartswith=fname)

    # my_objects = user.objects.all().order_by('-id')
    # Set the number of items per page
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)


    return render(request,'Admin/patient needs.html', {'val': ob,"my_objects":my_objects})



@login_required(login_url='/')
def patient_needs_verify(request, id):
        ob = patients_needs.objects.get(id=id)
        ob.status = "verified"
        ob.save()
        return HttpResponse('''<script>alert('Verified');window.location='/patient_needs#about'</script>''')


@login_required(login_url='/')
def patient_needs_search(request):
    name = request.POST['textfield']
    my_objects = patients_needs.objects.filter(CARETAKERID__fname__istartswith=name).order_by('-id')
    items_per_page = 4

    # Create a Paginator instance
    paginator = Paginator(my_objects, items_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the Page object for the requested page
        my_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        my_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        my_objects = paginator.page(paginator.num_pages)


    return render(request, 'Admin/patient needs.html',{'my_objects':my_objects})









@login_required(login_url='/')
def view_complnt(request):
    ob=complaint.objects.filter(reply='pending').union(complaint.objects.exclude(reply='pending'))
    return render(request,"Admin/view cmplnt.html",{"val":ob})


@login_required(login_url='/')
def send_rply(request,id):
    request.session['pp']=id
    return render(request,"Admin/send reply.html")



@login_required(login_url='/')
def sendreplycode(request):
    reply=request.POST['textfield']
    ob=complaint.objects.get(id=request.session['pp'])
    ob.reply=reply
    ob.save()
    return HttpResponse('''<script>alert("Reply Sent");window.location='/view_complnt'</script>''')


@login_required(login_url='/')
def complaint_search(request):
    date=request.POST['textfield']
    ob = complaint.objects.filter( date__istartswith=date).order_by('-id')
    return render(request,'Admin/view cmplnt.html',{'val':ob})







@login_required(login_url='/')
def view_patient_recods(request,id):
    request.session['rrid']=id
    return redirect('/viewprecords1')


@login_required(login_url='/')
def viewprecords1(request):
    obb=patientrecords.objects.filter(PATIENTID=request.session['rrid']).order_by('-id')

    return render(request,"Admin/VIEW PATIENT RECORDS.html",{'val':obb})


def main_alert(request):
    return HttpResponse('''<script>alert('alert');window.location=#about'</script>''')
#---------------------------_____________________webchat---

@login_required(login_url='/')
def chatwithuser(request):
    ob = caretaker.objects.all()
    return render(request,"Admin/fur_chat.html",{'val':ob})



@login_required(login_url='/')
def chatview(request):
    ob = caretaker.objects.all()
    d=[]
    for i in ob:
        r={"name":i.fname+i.lname,'photo':i.photo.url,'email':i.email,'loginid':i.LOGINID.id}
        d.append(r)
    return JsonResponse(d, safe=False)



@login_required(login_url='/')
def coun_insert_chat(request,msg,id):
    print("===",msg,id)
    ob=chat_table()
    ob.FROMID=login_table.objects.get(id=request.session['lid'])
    ob.TOID=login_table.objects.get(id=id)
    ob.message=msg
    ob.date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    ob.save()

    return JsonResponse({"task":"ok"})
    # refresh messages chatlist


@login_required(login_url='/')
def coun_msg(request,id):

    ob1=chat_table.objects.filter(FROMID__id=id,TOID__id=request.session['lid'])
    ob2=chat_table.objects.filter(FROMID__id=request.session['lid'],TOID__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.FROMID.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=caretaker.objects.get(LOGINID__id=id)


    return JsonResponse({"data":res,"name":obu.fname+obu.lname,"photo":obu.photo.url,"user_lid":obu.LOGINID.id})




# "=====================android=================="


def logincodeand(request):
    print(request.POST)
    un = request.POST['uname']
    pwd = request.POST['pass']
    print(un, pwd)
    try:
        users = login_table.objects.get(Username=un, password=pwd,type="caretaker")
        if (users.Username == un and users.password == pwd):
            if users is None:
                data = {"task": "invalid"}
            else:
                print("in user function")
                data = {"task": "valid", "id": users.id}
        else:
            data = {"task": "invalid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)
    except Exception as e:
        print(e)
        data = {"task": "invalid"}
        r = json.dumps(data)
        print(r)
        return HttpResponse(r)


def  viewassginedwork(request):
    lid=request.POST['lid']
    ob = work_table.objects.filter(CARETAKERID__LOGINID__id=lid).order_by('-id')

    # o=ob.union(obB)
    data = []
    for i in ob:
        row = {"work": i.work, "details": i.details,"status":i.status,"date":str(i.date),"wid":i.id}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)

def updatework(request):
    print(request.POST)
    wid=request.POST['wid']
    status=request.POST['status']
    ob=work_table.objects.get(id=wid)
    ob.status=status
    ob.save()
    data = {"task": "success"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)

def check_uname_web(request):
    username  = request.GET['username']
    print(username)
    data = {
        'is_taken': login_table.objects.filter(Username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this username already exists."

        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)


def check_email_web(request):
    username  = request.GET['em']
    print(username)
    data = {
        'is_taken': caretaker.objects.filter(email__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this email  already exists."

        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)


def check_phone_web(request):
    username  = request.GET['phone']
    print(username)
    data = {
        'is_taken': caretaker.objects.filter(phone__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this phone number already exists."

        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)
def change_password(request):
    cpwd = request.POST['cpwd']
    npwd = request.POST['npwd']
    lid = request.POST['lid']

    try:
        ob=login_table.objects.get(id=lid,password=cpwd)
        ob.password=npwd
        ob.save()
        return JsonResponse({"task":"valid"})
    except:
        return JsonResponse({"task": "invalid"})

def update_patient_info(request):
    patientid = request.POST['pid']
    file = request.FILES['file']
    fs=FileSystemStorage()
    f=fs.save(file.name,file)

    try:
        ob=patientrecords()
        ob.PATIENTID_id=patientid
        ob.report=f
        ob.date=datetime.datetime.now()
        ob.save()

        return JsonResponse({"task":"success"})
    except:
        return JsonResponse({"task": "invalid"})

def viewpatient_info(request):
    lid = request.POST['lid']
    ob = patient.objects.filter(CARETAKERID__LOGINID__id=lid,type="alive")
    data = []
    for i in ob:
        row = {"fname": i.fname,"lname": i.lname,"gender": i.gender,"age": i.age,"photo": i.photo.url,"healthcondition":i.healthcondition,'date':str(i.admit_date),'caretaker':i.id}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)





def viewmang_pills_setalaram(request):
    lid = request.POST['lid']
    ob = pillreminder.objects.filter(CARETAKERID__LOGINID__id=lid)
    data = []
    for i in ob:
        row = {"pname": i.PATIENTID,"medicine": i.medicine,"date": i.date,"time": i.time,"times": i.no_oftimes,"days": i.days,}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)




def view_patient(request):
    lid = request.POST['lid']
    ob = patient.objects.filter(CARETAKERID__LOGINID__id=lid,type="alive")
    data = []
    for i in ob:
        row = {"pname": i.fname + i.lname,"pid":i.id,}
        data.append(row)
    r = json.dumps(data)
    print(r,"hhhhhhhhhhhhhhhh")
    return HttpResponse(r)
def view_med(request):
    pid = request.POST['pid']
    ob = medicine_table.objects.filter(PATIENTID__id=pid)
    data = []
    for i in ob:
        row = {"mname": i.medicine, "mid": i.id,'details':i.details}
        data.append(row)
    r = json.dumps(data)
    print(r, "hhhhhhhhhhhhhhhh")
    return HttpResponse(r)

def addreminder(request):
    print(request.POST,"jjjjjjjjjjjjj")
    pid = request.POST['PATIENTID']
    medn_name=request.POST['medicine']
    date = request.POST['date']
    timme=request.POST['time']
    no_of_times = request.POST['no_oftimes']
    days = request.POST['days']


    obu=pillreminder()

    obu.PATIENTID_id=pid
    obu.medicine_id=medn_name
    obu.date=date
    obu.time = timme
    obu.no_oftimes = no_of_times
    obu.days = days
    obu.save()
    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def mednoti(request):
    lid=request.POST['lid']
    ob=pillreminder.objects.filter(PATIENTID__CARETAKERID__LOGINID__id=lid,date__lte=datetime.datetime.today())
    h=datetime.datetime.now().strftime("%H:%M")

    result=[]
    for i in ob:
        rr=i.time.split(',')
        for j in rr:
            print(j,h)
            if h[0]== "0":
                h=h[1:]
            if j==h:
                row = {"msg": "Time for give "+i.medicine.medicine+" to "+i.PATIENTID.fname+" "+i.PATIENTID.lname}
                result.append(row)
    r = json.dumps(result)
    return HttpResponse(r)

def view_medicine_info(request):
    lid=request.POST['lid']
    ob=pillreminder.objects.filter(PATIENTID__CARETAKERID__LOGINID__id=lid,date__lte=datetime.datetime.today())

    result=[]
    for i in ob:


        row = {"id":i.id,"name":i.PATIENTID.fname+" "+i.PATIENTID.lname,"medicine":i.medicine.medicine,"date":str(i.date),"time":str(i.time),"no_tims":i.no_oftimes,"days":i.days}
        result.append(row)
    r = json.dumps(result)
    return HttpResponse(r)

def delete_medicine_info(request):
    mid=request.POST['mid']
    ob=pillreminder.objects.get(id=mid)
    ob.delete()
    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


# ---------------------------------

def view_suffict_medicine(request):
    lid = request.POST['lid']
    ob = medicine_notification.objects.filter(CARETAKERID__LOGINID__id=lid)
    data = []
    for i in ob:
        row = {"medicine": i.medicine.medicine,"details":i.details,"date":str(i.date),"status":i.status,"PATIENTID":i.PATIENTID.fname+""+i.PATIENTID.lname,"pid":i.id}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)


def add_s_med_info(request):
    print(request.POST,"jjj")
    pid = request.POST['PATIENTID']
    lid = request.POST['lid']
    medn_name=request.POST['medicine']
    details = request.POST['det']

    obu=medicine_notification()
    print("---------------",lid)
    obu.PATIENTID_id=pid
    obu.CARETAKERID=caretaker.objects.get(LOGINID=lid)
    obu.medicine_id=medn_name
    obu.details=details
    obu.date = datetime.datetime.today()
    obu.status = 'pending'
    obu.save()
    data = {"task": "ADDED"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def delete_s_med_info(request):
    mid=request.POST['rid']
    ob=medicine_notification.objects.get(id=mid)
    ob.delete()
    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)

def search_s_med_info(request):
    name=request.POST['date']
    lid = request.POST['lid']
    ob = medicine_notification.objects.filter(CARETAKERID__LOGINID__id=lid,PATIENTID__fname__icontains=name)
    data = []
    for i in ob:
        row = {"medicine": i.medicine.medicine, "details": i.details, "date": str(i.date), "status": i.status,
               "PATIENTID": i.PATIENTID.fname + "" + i.PATIENTID.lname, "pid": i.id}
        data.append(row)
    print(data)
    r = json.dumps(data)
    return HttpResponse(r)

#---------------------------------------------------

def view_patient_needs(request):
    lid = request.POST['lid']
    ob =patients_needs.objects.filter(CARETAKERID__LOGINID__id=lid)
    data = []
    for i in ob:
        row = {"needs": i.needs,"details":i.details,"date":str(i.date),"status":i.status,"PATIENTID":i.PATIENTID.fname+""+i.PATIENTID.lname,"pid":i.id}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)

def view_alert(request):
    lid=request.POST["lid"]
    ob = patient.objects.filter(CARETAKERID__LOGINID__id=lid)
    patient_list = []
    for i in ob:
        patient_list.append(i.id)
        # row = {"needs": i.needs, "details": i.details, "date": str(i.date), "status": i.status,
        #        "PATIENTID": i.PATIENTID.fname + "" + i.PATIENTID.lname, "pid": i.id}
        # data.append(row)
    ob = fall_detection.objects.filter(PATIENTID__in=patient_list , status="pending")
    data=[]
    for i in ob:
        row = {"img": str(i.photo.url),"time":i.time,"date":str(i.date),"status":i.status,"patientname":i.PATIENTID.fname+""+i.PATIENTID.lname,"id":i.id,"camerainfo":i.CAMERAID.location,"condition":i.condition}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)






def add_p_needs(request):
    print(request.POST,"jjj")
    pid = request.POST['PATIENTID']
    lid = request.POST['lid']
    needs=request.POST['needs']
    details = request.POST['details']

    obu=patients_needs()
    print("---------------",lid)
    obu.PATIENTID=patient.objects.get(id=pid)
    obu.CARETAKERID=caretaker.objects.get(LOGINID=lid)
    obu.needs=needs
    obu.details=details
    obu.date = datetime.datetime.today()
    obu.status = 'pending'
    obu.save()
    data = {"task": "ADDED"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def delete_p_needs(request):
    nid=request.POST['rid']
    ob=patients_needs.objects.get(id=nid)
    ob.delete()
    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)

def search_p_needs(request):
    name=request.POST['name']
    lid = request.POST['lid']
    ob = patients_needs.objects.filter(CARETAKERID__LOGINID__id=lid,PATIENTID__fname__icontains=name)
    data = []
    for i in ob:
        row = {"needs": i.needs, "details": i.details, "date": str(i.date), "status": i.status,
               "PATIENTID": i.PATIENTID.fname + "" + i.PATIENTID.lname, "pid": i.id}
        data.append(row)
    print(data)
    r = json.dumps(data)
    return HttpResponse(r)

def add_medicine(request):
    pid = request.POST['pid']
    medicine=request.POST['medicine']
    details = request.POST['details']
    obu=medicine_table()
    obu.PATIENTID = patient.objects.get(id=pid)
    obu.medicine=medicine
    obu.details=details
    obu.save()
    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)

def getAlert(request):
    lid=request.POST["lid"]

    ob =patient.objects.filter(CARETAKERID__LOGINID__id=lid)
    patient_list = []
    for i in ob:
        patient_list.append(i.id)
        # row = {"needs": i.needs, "details": i.details, "date": str(i.date), "status": i.status,
        #        "PATIENTID": i.PATIENTID.fname + "" + i.PATIENTID.lname, "pid": i.id}
        # data.append(row)
    obb = fall_detection.objects.filter(PATIENTID__in=patient_list,status="pending")
    if len(obb)>0:
        print(obb,"==============================================ppppp")
        data = {"task": "valid"}
    else:
        data = {"task":"invalid"}

    r = json.dumps(data)
    return HttpResponse(r)

def update_alert(request):
    alerid=request.POST["id"]


    ob = fall_detection.objects.get(id=alerid).delete()

    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)



def update_alertall(request):
    lid=request.POST["lid"]


    ob = fall_detection.objects.filter(PATIENTID__CARETAKERID__LOGINID=lid).update(status="solved ")

    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)



def c_send_complaint(request):
    print(request.POST,"jjj")
    lid = request.POST['lid']
    comp=request.POST['comp']
    obu=complaint()
    print("---------------",lid)
    obu.CARETAKERID=caretaker.objects.get(LOGINID=lid)
    obu.complaint=comp
    obu.date = datetime.datetime.today()
    obu.reply='pending'
    obu.save()
    data = {"task":"valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)


def view_complaint(request):
    lid = request.POST['lid']
    ob =complaint.objects.filter(CARETAKERID__LOGINID__id=lid)
    data = []
    for i in ob:
        row = {"complaint": i.complaint,"reply":i.reply,"date":str(i.date),"id":i.id}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)

def delete_complaint(request):
    cid=request.POST['cid']
    ob=complaint.objects.get(id=cid)
    ob.delete()
    data = {"task": "valid"}
    r = json.dumps(data)
    print(r)
    return HttpResponse(r)







#---------------------------camera-------------
def fall_detecion(request):
    pid = request.GET['pid']
    fn = request.GET['fn']
    cam=request.GET["cam"]
    con=request.GET["con"]
    time = datetime.datetime.now().time()
    date = datetime.datetime.now().date()
    obu=fall_detection()
    obu.PATIENTID = patient.objects.get(id=pid)
    obu.time=time
    obu.CAMERAID_id=cam
    obu.photo=fn
    obu.date=date
    obu.condition=con
    obu.status="pending"
    obu.save()
    return HttpResponse("ok")





# ///////////////////////////////////android chat //////////////////////////////////////////////

def view_message2(request):
    print(request.POST)
    fromid=request.POST['fid']
    toid=request.POST['toid']
    mid=request.POST['lastmsgid']
    print(mid,"uuuuuuuuuuuu0")
    ob=chat_table.objects.filter(Q(TOID__id=toid,FROMID__id=fromid,id__gt=mid)|Q(TOID_id=fromid,FROMID_id=toid,id__gt=mid)).order_by('id')
    print(ob,"YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
    data=[]
    print("++++++++==============================")
    print("++++++++==============================")
    print("++++++++==============================")
    for i in ob:
        r={"msgid":i.id,"date":i.date,"message":i.message,"fromid":i.FROMID.id}
        data.append(r)
        print(r,"KKKKKKKKKKKKKKKKKKKKKKKKKKKK")
    # print(data,"JJJJJJJJJJJJJJJJJJJJJJJJJ")
    print(len(data),"=========================================")
    if len(data)>0:
        return JsonResponse({"status":"ok","res1":data})
    else:
        return JsonResponse({"status": "na"})



def in_message2(request):
    fromid = request.POST['fid']
    toid=request.POST['toid']
    chat = request.POST['msg']

    ob = chat_table()
    ob.message = chat
    # ob.time = datetime.now().strftime("%H:%M:%S")
    ob.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    ob.FROMID = login_table.objects.get(id=fromid)
    ob.TOID = login_table.objects.get(id=toid)
    ob.save()
    data = {"status": "send"}
    r = json.dumps(data)

    print(r)
    return HttpResponse(r)


# ////////////////////////////////// android chat///////////////////////////////////////////
