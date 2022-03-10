from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from aceapi.views import (register_user, login_user, DayView, AppUserView,
                          SubjectView, SubjectAreaView, NoteView, TestView,
                          LikeView, TutorStudentView)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'days', DayView, 'day')
router.register(r'users', AppUserView, 'user')
router.register(r'users', AppUserView, 'user')
router.register(r'subjects', SubjectView, 'subject')
router.register(r'subjectareas', SubjectAreaView, 'subject area')
router.register(r'notes', NoteView, 'note')
router.register(r'tests', TestView, 'test')
router.register(r'likes', LikeView, 'like')
router.register(r'pairs', TutorStudentView, 'pair')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
