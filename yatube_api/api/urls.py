from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, FollowList, GroupViewSet, PostViewSet

router = SimpleRouter()
router.register("posts", PostViewSet)
router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comment"
)
router.register("groups", GroupViewSet)

app_name = "api"

urlpatterns = [
    path("v1/", include("djoser.urls")),
    path("v1/", include("djoser.urls.jwt")),
    path("v1/", include(router.urls)),
    path("v1/follow/", FollowList.as_view()),
]
