from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import List, Record
from .forms import ListForm

import datetime
from constants import LOGIN_URL

# Create your views here.
@login_required(login_url=LOGIN_URL)
def index(request):
    return render(request, "main/index.html")

@login_required(login_url=LOGIN_URL)
def dashboard(request):
    return render(request, 'main/dashboard.html')

@login_required(login_url=LOGIN_URL)
def upload(request):
    if request.method == 'POST':
        #抓取上傳資料
        uploadedFile = request.FILES.get('uploadFile')
        if not uploadedFile:
            print('沒有選擇文件')
            return render(request, 'main/upload.html', {'msg': '沒有選擇文件'})
        if not uploadedFile.name.endswith('.xlsx'):
            print('必須選擇xlsx文件')
            return render(request, 'main/upload.html', {'msg': '必須選擇xlsx文件'})
    
        #Clean data
        import pandas as pd
        #data_cleaning function is located in "functions"
        import functions
        df = pd.read_excel(uploadedFile)
        df = df[['案發日期', '出勤車輛', '案件細項', '發生地點']]
        df_info = functions.data_cleaning(df)
        insert_data(df_info)
        create_record(request, 'upload', 'UploadFiles in Database')
        return render(request, 'main/index.html')
    return render(request, 'main/upload.html')

def insert_data(df):
    #dataframe length
    df_len = len(df)
    #iterator through whole dataframe
    for num in range(0, df_len):
        #create objects in List Model
        List.objects.create(
            DateTime = df.iloc[num][0], 
            Car= df.iloc[num][1],
            Detail = df.iloc[num][2], 
            Location  = df.iloc[num][3]
        )

@login_required(login_url=LOGIN_URL)
def list(request):
    list_table = List.objects.all()
    context = {'list_table': list_table}
    return render(request, 'main/list.html', context)

@login_required(login_url=LOGIN_URL)
def listEdit(request):
    #Form
    submitted = False
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            form.save()
            create_record(request, 'edit', 'Edit the Emergency Cases List')
            context = {'form': form}
            return HttpResponseRedirect('/emergency_list/edit?submitted=True/', context)
    else:
        form = ListForm
        if 'submitted' in request.GET:
            submitted = True
    context = {'form': form, 'submitted': submitted}
    return render(request, 'main/listEdit.html', context)

@login_required(login_url=LOGIN_URL)
def listUpdate(request, Em_id):
    #Get Each ID
    list_obj = List.objects.get(pk = Em_id)
    #Form request or None
    form = ListForm(request.POST or None, instance = list_obj)
    if form.is_valid():
        form.save()
        #Create Reocrd
        create_record(request, 'update', 'update' + '-caseID: ' + str(Em_id))
        messages.success(request, f"Update List {Em_id} Scuessfully!!")
        return redirect('list')
    context = {'list_obj': list_obj, 'form': form}
    return render(request, 'main/listUpdate.html', context) 

@login_required(login_url=LOGIN_URL)
def listDelete(request, Em_id):
    #Get Each ID
    list_obj = List.objects.get(pk = Em_id)
    #Delete
    list_obj.delete()
    #Create Record
    create_record(request, 'delete', 'delete' + '-caseID: ' + str(Em_id))
    return redirect('list')

@login_required(login_url=LOGIN_URL)
def user(request):
    all_users = User.objects.values()
    context = {'all_users': all_users}
    return render(request, 'main/user.html', context)

@login_required(login_url=LOGIN_URL)
def record(request):
    record_table = Record.objects.all()
    context = {'record_table': record_table}
    return render(request, 'main/record.html', context)

def create_record(request, active, active_content):
    #create objects in Record Model
    Record.objects.create(
        Active = active, 
        IP = get_client_ip(request), 
        Content = active_content, 
        Member = request.user.username, 
        DateTime = datetime.datetime.now()
    )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip