from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from Ecommapp.models import product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
def home(request):
    context={}
    context['name']="john"
    context['age']=200
    userid=request.user.id
    print("id logged in user:",userid)
    print("result:",request.user.is_authenticated)
    #return HttpResponse("<h1>tihs is home page</h1>")
    return render(request,'home.html',context)
def about(request):
    #return HttpResponse("<i>this is about page</i>")
    return render(request,'about.html')
def contact(request):
    return HttpResponse("this is contact page")
def addition(request,a,b):
    # print(a)
    # print(b)
    # #print(int(a)+int(b))
    # print(type(a))
    #res=int(a)+int(b)
    if int(a)>int(b):
        res="a is greater"
        return HttpResponse(res)
    else:
        res="b is greter"
        return HttpResponse(res)
    #return HttpResponse(res)
#class based views
class SimpleView(View):
    def get(self,request):
        return HttpResponse("hello from siimple view")
def checkgreaternum(request):
    context={}
    context['x']=10
    context['y']=20
    context['l']=[10,20,30,40]
    context['products']=[
    {'id':1,'name':'samsung','cat':'mobile','price':20000},
    {'id':2,'name':'jeans','cat':'cloth','price':500},
    {'id':3,'name':'adidas shoes','cat':'shoes','price':2200},
    {'id':4,'name':'vivo','cat':'mobile','price':15000}
]
    return render(request,'checkgreaternum.html',context)
def index(request):
    context={}
    p=product.objects.filter(is_active=True)
    print(p)
    print(p[0].price)
    print(p[0].name)
    print(p[0].cat)
    context['Products']=p
    return render(request,'index.html',context)
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1&q2)
    context={}
    context['Products']=p
    return render(request,'index.html',context)
def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['Products']=p
    return render(request,'index.html',context) 
def addtocart(request,pid):
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        #print(u)
        p=product.objects.filter(id=pid)
        #print(p)
        #check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        #print(c)
        n=len(c)
        context={}
        context['Products']=p
        if n==1:
            context['msg']="product already exist in acrt"
            return render(request,'product_detail.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="product added successfully to cart!!"
            return render(request,'product_detail.html',context)
    else:
        return redirect('/login')

def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    # print(c[0])
    # print(c[0].uid)
    # print(c[0].pid.name)
    s=0
    np=len(c)
    for x in c:
        print(x)
        print(x.pid.price)
        s=s+x.pid.price*x.qty
    context={}
    context['Products']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')
def updateqty(request,qv,cid):
    # print(type(qv))
    # return HttpResponse("in update quantity")
    c=Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/cart')
def place_order(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    print("order id:",oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.uid)
        # print(x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    #np=len(orders)
    np=0
    for x in orders:
        s=s+x.pid.price*x.qty
        np=np+x.qty
    context={}
    context['Products']=orders
    context['total']=s
    context['n']=np
    context['u']=orders
    return render(request,'place_order.html',context)
def product_detail(request,pid):
    context={}
    context['Products']=product.objects.filter(id=pid)
    return render(request,'product_detail.html',context)        
        
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    print(min)
    print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1&q2&q3)
    #print(p)
    context={}
    context['Products']=p
    return render(request,'index.html',context)


def registration(request):
    context={}
    if request.method=='POST':
        u=request.POST['uname']
        up=request.POST['upass']
        ucp=request.POST['ucpass']
        if u=="" or up=="" or ucp=="":
            context['errmsg']="fields cnnot be empty"
            return render(request,'registration.html',context)
        elif up!=ucp:
            context['errmsg']="password and confirm password did not match"
            return render(request,'registration.html',context)
        else:
            try:
                u=User.objects.create(username=u,email=u)        
                u.set_password(up)
                u.save()
                context['success']="user created successfully"
                return render(request,'registration.html',context)
            except Exception:
                context['errmsg']="user with same username already exist"
                return render(request,'registration.html',context)
    return render(request,'registration.html')
def user_login(request):
    context={}
    if request.method=='POST':
        u=request.POST['uname']
        up=request.POST['upass']
        print(u)
        print(up)
        if u=="" or up=="":
            context['errmsg']="fields cannot be empty"
            return render(request,'login.html',context)
        else:
            k=authenticate(username=u,password=up)
            print(k)
            # print(k)
            # print(k.email)
            # print(k.username)
            # print(k.is_superuser)
            if k is not None:
                login(request,k)#start session and store id of logged in user in session
                return redirect('/index')
            else:
                context['errmsg']="invalid username and password"
                return render(request,'login.html',context)
                #return HttpResponse("in else part")
    else:
        return render(request,'login.html')
def user_logout(request):
    logout(request)
    return redirect('/index')

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_qPpA776V9DCblP", "TWcWQeLgGmHfG66yYcv7tzhJ"))
    data = { "amount":s*100 , "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)

def search_view(request):
    query = request.GET.get('query')
    results = []
    if query:
        results = product.objects.filter(name__icontains=query)  # Adjust the field name as necessary
    return render(request, 'search_results.html', {'query': query, 'results': results})    

def sendusermail(request):
    uemail=request.user.email
    print(uemail)
    userid=request.user.id
    print(userid)
    send_mail(
    "Ekart-order placed successfully",
    "order details are:",
    "mis.ae2@grouparvind.com",
    [uemail],
    fail_silently=False,
    )
    return HttpResponse("Mail send successfully")
