from django.urls import path,include
from .views import ProfileUpdateById, SignUpView, ProfileUpdate, DeleteUserListView, delete_user, EmailUpdate, ProfileDetail


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileDetail.as_view(), name='profile'), 
    path('', include('django.contrib.auth.urls')),
    path('delete_user/', DeleteUserListView.as_view(), name='delete_userlist'),
    path('delete_user/<slug:username>/', delete_user , name='delete_user')  ,
    path('profile/update/', ProfileUpdate.as_view(), name='update_profile'),
    path('profile/update/P<pk>/', ProfileUpdateById.as_view(), name='update_profilebyid'),            
    path('profile/email/', EmailUpdate.as_view(), name='email')      
    
]

