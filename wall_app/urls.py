"""wall_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework import routers
from wall.views import WriterViewSet
from wall.views import PostViewSet
from wall.views import Registration
from wall.views import Activate
from wall.views import Login
from wall.views import Logout
from wall.views import CreatePost
from wall.views import ReadPost
from wall.views import PostComment

router = routers.DefaultRouter()
router.register(r'writers', WriterViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/user/registration/', Registration.as_view(), name='writer-registration'),
    path('api/user/login/', Login.as_view(), name='writer-login'),
    path('api/user/logout/', Logout.as_view(), name='writer-logout'),
    path('api/post/create/', CreatePost.as_view(), name='post-create'),
    path('api/post/read/', ReadPost.as_view(), name='post-read'),
    path('api/post/comment/', PostComment.as_view(), name='post-comment'),
    path('api/activate/', Activate.as_view(), name='writer-activation'),
]
