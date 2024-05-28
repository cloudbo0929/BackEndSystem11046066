from django.db.models import Q
from django.db.models.functions import Concat
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from backendApp.middleware import login_required
from backendApp.decorator import group_required
from backendApp.forms import UserProfileForm, CustomUserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@group_required('admin')
@login_required
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, '註冊成功！')
            return redirect('user_manager')
    else:
        form = CustomUserCreationForm()
    return render(request, 'userManagement/add_user.html', {'form': form})

@group_required('admin')
@login_required
def user_manager(request):
    query = request.GET.get('search', '').strip()
    group_id = request.GET.get('group', '').strip()
    users = User.objects.all()
    groups = Group.objects.all()

    if query:
        users = User.objects.all().annotate(
            full_name=Concat('first_name', 'last_name')
        ).filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(full_name__icontains=query)
        )

    if group_id:
        users = users.filter(groups__id=group_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            user_id = request.POST.get('delete')
            User.objects.filter(id=user_id).delete()
        elif 'edit' in request.POST:
            user_id = request.POST.get('edit')
            user_to_edit = get_object_or_404(User, id=user_id)
            form = UserProfileForm(request.POST, instance=user_to_edit)
            if form.is_valid():
                form.save()
                return redirect('user_manager')

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'userManagement/user_list.html', {
        'page_obj': users,
        'groups': groups,
        'query': query,
        'group_id': group_id
    })

@login_required
@group_required('admin')
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return redirect('user_manager')
    else:
        form = UserProfileForm(instance=user_to_edit)
    
    return render(request, 'userManagement/edit_user.html', {'form': form, 'user_id': user_id})

