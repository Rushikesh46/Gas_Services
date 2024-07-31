from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ServiceRequest, Customer
from .forms import UserRegisterForm, ServiceRequestForm,ServiceRequestUpdateForm
from django.urls import reverse
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not Customer.objects.filter(user=user).exists():
                Customer.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Your account has been created successfully! You are now logged in.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'services/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'services/login.html', {'error': 'Invalid username or password'})
    # else:
    return render(request, 'services/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def account_info(request):
    return render(request, 'services/account_info.html')

@login_required
def home(request):
    if request.user.is_staff:
        requests = ServiceRequest.objects.all()
    else:
        customer = get_object_or_404(Customer, user=request.user)
        requests = ServiceRequest.objects.filter(customer=customer)
    return render(request, 'services/home.html', {'requests': requests})

@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = get_object_or_404(Customer, user=request.user)
            service_request.save()
            return redirect('home')
    else:
        form = ServiceRequestForm()
    return render(request, 'services/submit_request.html', {'form': form})

@login_required
def track_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id, customer__user=request.user)
    return render(request, 'services/track_request.html', {'request': service_request})
    

@login_required
def track_requests_list(request):
    customer = get_object_or_404(Customer, user=request.user)
    requests = ServiceRequest.objects.filter(customer=customer)
    return render(request, 'services/track_requests_list.html', {'requests': requests})

@login_required
def manage_requests(request):
    if not request.user.is_staff:
        return redirect('home')
    requests = ServiceRequest.objects.all()
    if request.method == 'POST':
        for request_id in request.POST:
            if request_id.startswith('update_'):
                request_id = request_id[len('update_'):]
                service_request = get_object_or_404(ServiceRequest, id=request_id)
                status = request.POST.get(f'status_{request_id}')
                service_request.status = status
                service_request.resolved_at = timezone.now() if status == 'RESOLVED' else None
                service_request.save()
    return render(request, 'services/manage_requests.html', {'requests': requests})

@login_required
def update_request(request, request_id):
    if not request.user.is_staff:
        return redirect('home')
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.method == 'POST':
        form = ServiceRequestUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()
            return redirect('manage_requests')
    else:
        form = ServiceRequestUpdateForm(instance=service_request)
    return render(request, 'services/update_request.html', {'form': form, 'service_request': service_request})
