from __future__ import absolute_import

from wall.views.viewset import WriterViewSet
from wall.views.viewset import PostViewSet

from wall.views.writer_auth import Registration
from wall.views.writer_auth import Activate
from wall.views.writer_auth import Login
from wall.views.writer_auth import Logout

from wall.views.post_crud import CreatePost
from wall.views.post_crud import ReadPost
from wall.views.post_crud import PostComment
