
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from app.forms import TODOForm
from app.models import TODO
from django.utils import timezone
from django.db.models import Q


@login_required(login_url='login')
def home(request):
    user = request.user
    form = TODOForm()
   
    # --- GET FILTER PARAMETERS ---
    # Retrieve filter values from the URL query string (GET request)
    search_query = request.GET.get('q', '')      # Search box value
    category_filter = request.GET.get('category', '') # Category dropdown value
    status_filter = request.GET.get('status', '')    # Status dropdown value
    priority_filter = request.GET.get('priority', '') # <--- NEW: Priority dropdown value
    order_by = request.GET.get('order', 'priority')  # Ordering field
    # -----------------------------


    # Start with all todos for the logged-in user
    todos = TODO.objects.filter(user=user)


    # 1. Apply Search Filter (checks title or description)
    if search_query:
        todos = todos.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
       
    # 2. Apply Category Filter
    # Check if a category is selected (not 'All Category', which submits an empty string)
    if category_filter:
        todos = todos.filter(category=category_filter)
       
    # 3. Apply Status Filter
    # Check if a status is selected (not 'All Status', which submits an empty string)
    if status_filter:
        todos = todos.filter(status=status_filter)
       
    # 4. Apply Priority Filter (<--- NEW LOGIC)
    # Check if a priority is selected (not 'All Priority', which submits an empty string)
    if priority_filter:
        todos = todos.filter(priority=priority_filter)


    # 5. Apply Ordering
    if order_by == 'date':
        todos = todos.order_by('-date')
    elif order_by == 'due':
        todos = todos.order_by('due_date')
    else:
        # Default sort by priority (assuming priority is a field that sorts naturally, e.g., an integer field)
        todos = todos.order_by('priority')


    # Progress calculation
    total = todos.count()
    completed = todos.filter(status='C').count()
    progress = int((completed / total) * 100) if total > 0 else 0


    context = {
        'form': form,
        'todos': todos,
        'q': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'priority_filter': priority_filter, # <--- NEW: Pass filter back to template
        'order_by': order_by,
        'progress': progress,
        'total': total,
        'completed': completed,
    }
    return render(request, 'index.html', context=context)


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {"form": form}
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        context = {"form": form}
        return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {"form": form}
        return render(request, 'signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login')
        context = {"form": form}
        return render(request, 'signup.html', context=context)


@login_required(login_url='login')
def add_todo(request):
    user = request.user
    if request.method == 'POST':
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            # if status is completed, set completed_at
            if todo.status == 'C' and not todo.completed_at:
                todo.completed_at = timezone.now()
            todo.save()
            return redirect("home")
        else:
            # re-render with validation errors (if you want to re-render, you need to grab filters/todos)
            todos = TODO.objects.filter(user=user).order_by('priority')
            return render(request, 'index.html', context={'form': form, 'todos': todos})
    return redirect('home')


@login_required(login_url='login')
def edit_todo(request, id):
    user = request.user
    todo = get_object_or_404(TODO, pk=id, user=user)
    if request.method == 'GET':
        form = TODOForm(instance=todo)
        return render(request, 'edit_todo.html', context={'form': form, 'todo': todo})
    else:
        form = TODOForm(request.POST, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            # update completed_at logically
            if todo.status == 'C' and not todo.completed_at:
                todo.completed_at = timezone.now()
            if todo.status == 'P':
                todo.completed_at = None
            todo.save()
            return redirect('home')
        return render(request, 'edit_todo.html', context={'form': form, 'todo': todo})


@login_required(login_url='login')
def delete_todo(request, id):
    todo = get_object_or_404(TODO, pk=id, user=request.user)
    todo.delete()
    return redirect('home')


@login_required(login_url='login')
def change_todo(request, id, status):
    todo = get_object_or_404(TODO, pk=id, user=request.user)
    todo.status = status
    if status == 'C':
        todo.completed_at = timezone.now()
    else:
        todo.completed_at = None
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')





 