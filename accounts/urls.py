from django.urls import path, reverse, reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import views as auth_views
from .views import *
from .forms import PasswordResetForm
from django.urls import reverse_lazy

app_name = 'accounts'

urlpatterns = [
    # Login
    path(
        'login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True, 
        redirect_field_name='/core/'
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/'
        ),
        name='logout'
    ),
    # Recovery Password
    path(
            'alterar/senha/',
            auth_views.PasswordChangeView.as_view(
                template_name='accounts/password_change.html',
                success_url=reverse_lazy('accounts:password_reset_complete'),
            ),
            name='password_change'
    ),
    #path('alterar/senha/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),name='password_change'),
    #url('password_change/done/$', password_change_done, { 'template_name': 'accounts/password_change_done.html'}, name='password_change_done'),
    path(
            'recuperar/senha/',
            auth_views.PasswordResetView.as_view(
                template_name='accounts/password_reset.html',
                form_class=PasswordResetForm,
                email_template_name='accounts/password_reset_email.txt', # Template padrao sem formatação
                success_url=reverse_lazy('accounts:password_reset_done'),
                from_email='SEMEX: <sti.cshnb@ufpi.edu.br>',
                html_email_template_name='accounts/password_reset_email.html',
            ),
            name='password_reset'
    ),
    path(
            'recuperar/senha/done/',
            auth_views.PasswordResetDoneView.as_view(
                template_name='accounts/password_reset_done.html',
            ),
            name='password_reset_done'
    ),
    path(
            'reset/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/password_reset_confirm.html',
                success_url=reverse_lazy('accounts:password_reset_complete'),
                post_reset_login=True,
            ),
            name='password_reset_confirm'
    ),
    path(
            'recuperar/done/',
            auth_views.PasswordResetCompleteView.as_view(
                template_name='accounts/password_reset_complete.html',
            ),
            name='password_reset_complete'
    ),
    # Edit
    path('alterar-dados/', UpdateUserView.as_view(), name='update_user'),
    path('alterar-senha/', UpdatePasswordView.as_view(), name='update_password'),
    
    path('participant/add/', CreateUser.as_view(), name='add_user'),
    path('admin/add/', CreateUserAdmin.as_view(), name='add_user_admin'),
    
    path('admin/list/', ListUserAdmin.as_view(), name='list_user_admin'),
    path('participant/list/', ListUser.as_view(), name='list_user'),
    
    path('edit/<int:pk>/', EditUser.as_view(), name='edit_user'),
    path('user/delete/<int:pk>/', user_delete, name='delete_user',),
]
