from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#如果用户在没有登陆的情况下，跳转到登陆界面
class LoginRequiredMIxin(object):
    @method_decorator(login_required(login_url='/users/dl/')) #如果在用户未登录的状态下，自动 跳转到登陆页面
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMIxin, self).dispatch(request, *args, **kwargs)