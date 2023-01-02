from django.shortcuts import render,redirect

# Create your views here.
from socialapp.forms import PostForm, RegistrationForm,LoginForm
from django.contrib.auth.models import User
from django.views.generic import View,CreateView,FormView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from socialapp.models import Posts,Comments
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"u must login to continue")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

decorators=[signin_required,never_cache]


@method_decorator(decorators,name="dispatch")
class SignUpView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")

class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"
    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("success")
                return redirect("home")
            else:
                return render(request,self.template_name,{"form":form})

@method_decorator(decorators,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    success_url=reverse_lazy("home")
    context_object_name="posts"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        return Posts.objects.all().exclude(user=self.request.user)

decorators
def add_comments(request,*args,**kw):
    post_id=kw.get("id")
    pst=Posts.objects.get(id=post_id)
    com=request.POST.get("comment")
    pst.comments_set.create(comment=pst,user=request.user)
    return redirect("home")

decorators
def like_view(request,*args,**kw):
    pst_id=kw.get("id")
    pst=Posts.objects.get(id=pst_id)
    pst.like.add(request.user)
    pst.save()
    return redirect("home")

decorators
def signout(request,*args,**kw):
    logout(request)
    return redirect("signin")

class MyPostsView(ListView):
    model=Posts
    context_object_name="posts"
    template_name: str="myposts.html"

    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user)