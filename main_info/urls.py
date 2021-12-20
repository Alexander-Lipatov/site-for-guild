from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import ContactListView, DynamicPostsLoad, ClearNotificationsView, AddMemberNotificationsView, DelMemberNotificationsView

urlpatterns = [
    path('', ContactListView.as_view(), name='contact'),
    path('load-more', DynamicPostsLoad.as_view(), name='load_dynamic'),
    path('clear-notifications/', ClearNotificationsView.as_view(), name='clear_notifications'),
    path('<int:pk>-add/', AddMemberNotificationsView.as_view(), name='added_member'),
    path('<int:pk>-clear/', DelMemberNotificationsView.as_view(), name='del_member'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)