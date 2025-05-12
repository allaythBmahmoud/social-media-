from django.urls import path, include
from rest_framework import routers

from core.views import (
    RetrieveProfileView,
    PostListView,
    LikesView,
    CommentsView,
    BlockedUserView,
    ProfileView,
    LikedPostView,
    FollowSerializer
)
from user.views import UserFollowersFollowingViewSet

router = routers.DefaultRouter()
router.register(r"posts", PostListView)
router.register(
    r"profile/followers-following",
    UserFollowersFollowingViewSet,
    basename="user_followers_following",
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "profile/<int:id>/",
        RetrieveProfileView.as_view(),
        name="profile-retrieve"
    ),
    path(
        "profile/me/",
        ProfileView.as_view(),
        name="profile-me"
    ),
    path(
        "posts/<int:pk>/likes/",
        LikesView.as_view(),
        name="likes-view"
    ),
    path(
        "profile/liked/",
        LikedPostView.as_view(),
        name="liked-posts-view"
    ),
    path(
        "profile/<int:pk>/following-unfollowing/",
        FollowSerializer.as_view(),
        name="following-unfollowing-view"
    ),
    path(
        "posts/<int:pk>/commentaries/",
        CommentsView.as_view(),
        name="commentaries-create-view"
    ),
    path(
        "posts/<int:pk>/commentaries/<int:comment_id>/delete/",
        CommentsView.as_view(),
        name="commentaries-delete"
    ),
    path(
        "profile/blocked_users/",
        BlockedUserView.as_view(),
        name="blocked-users-retrieve"
    ),
    path(
        "profile/<int:pk>/block/",
        BlockedUserView.as_view(),
        name="block-user"
    ),
]

app_name = "core"
