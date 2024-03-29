"""pysite URL Configuration

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
from django.contrib import admin
from django.urls import path

import main.views as main_views
import user.views as user_views
import guestbook.views as guestbook_views
import board.views as board_views

urlpatterns = [
    path('', main_views.index),

    path('user/loginform', user_views.loginform),
    path('user/login', user_views.login),
    path('user/logout', user_views.logout),
    path('user/updateform', user_views.updateform),
    path('user/update', user_views.update),

    path('user/joinform', user_views.joinform),
    path('user/joinsuccess', user_views.joinsuccess),
    path('user/join', user_views.join),
    path('user/api/checkmail', user_views.checkemail),

    path('guestbook/', guestbook_views.guestbook_list),
    path('guestbook/add', guestbook_views.guestbook_add),
    path('guestbook/deleteform/<int:id>', guestbook_views.guestbook_deleteform),
    path('guestbook/delete', guestbook_views.guestbook_delete),

    path('board/', board_views.board_list),
    path('board/<int:id>', board_views.board_view),
    path('board/writeform', board_views.board_writeform),
    path('board/writeform/<int:id>', board_views.board_writeform),
    path('board/write/-1', board_views.board_write),
    path('board/write/<int:id>', board_views.board_write),
    path('board/delete/<int:id>', board_views.board_delete),
    path('board/modifyform/<int:id>', board_views.board_modifyform),
    path('board/modify/<int:id>', board_views.board_modify),
    path('board/search', board_views.board_search),

    path('admin/', admin.site.urls),
]
