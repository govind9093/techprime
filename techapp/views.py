from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from techapp.models import Projects
from django.core.paginator import Paginator

def Signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.save()
        return redirect('login')

    return render(request, 'signup.html') 

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')

@login_required
def Dashboard(request):
    # Calculate total projects for each department
    departments = ['Strategy', 'Finance', 'Marketing']  # Example departments
    total_projects = [Projects.objects.filter(project_department=dept).count() for dept in departments]

    # Calculate total closed projects for each department
    closed_projects = [Projects.objects.filter(project_department=dept, project_status='Closed').count() for dept in departments]

    # Calculate success percentage for each department
    success_percentage = [(closed / total) * 100 if total != 0 else 0 for closed, total in zip(closed_projects, total_projects)]

    # Pass the data to the template
    context = {
        'departments': departments,
        'total_projects': total_projects,
        'closed_projects': closed_projects,
        'success_percentage': success_percentage,
        'project_total': Projects.objects.count(),
        'running': Projects.objects.filter(project_status='Running').count(),
        'closed': Projects.objects.filter(project_status='Closed').count(),
        'delay': Projects.objects.filter(project_status='Delay').count(),
        'cancelled': Projects.objects.filter(project_status='Cancelled').count(),
    }

    return render(request, 'dashboard.html', {'context':context})
# def Dashboard(request):
#     running = Projects.objects.filter(project_status='Running').count()
#     closed = Projects.objects.filter(project_status='Closed').count()
#     delay = Projects.objects.filter(project_status='Delay').count()
#     cancelled = Projects.objects.filter(project_status='Cancelled').count()
#     project_total = Projects.objects.count()
    
#     return render(request, 'dashboard.html', {'project_total': project_total,'running':running,'closed':closed,'delay':delay,'cancelled':cancelled})   

def Create_Project(request):
    if request.method=='POST':
        pro_reason=request.POST['reason']
        pro_name=request.POST['pro_name']
        pro_type=request.POST['type']
        pro_division=request.POST['division']
        pro_category=request.POST['category']
        pro_priority=request.POST['priority']
        pro_department=request.POST['department']
        pro_start_date=request.POST['start_date']
        pro_end_date=request.POST['end_date']
        pro_location=request.POST['location']
        pro_status=request.POST['status']
        
        data=Projects.objects.create(project_name = pro_name, project_reason = pro_reason,project_type = pro_type, project_division = pro_division,project_category = pro_category,project_priority = pro_priority,project_department = pro_department,project_start_date= pro_start_date,project_end_date = pro_end_date,project_location = pro_location, project_status = pro_status)
        data.save();
        return redirect('project_list')
    return render(request, 'create_project.html')

project_total = []
def Project_List(request):
    obj = Projects.objects.all().order_by('project_name')
    project_count = obj.count()*5
    project_total.append(project_count)
    paginator = Paginator(obj,1)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1 
    try:
        projects = paginator.page(page)
    except(EmptyPage,InvalidPage):
        projects=paginator.page(paginator.num_pages)  

    print(obj)           
    return render(request, 'project_list.html',{'obj':obj,'projects':projects})


