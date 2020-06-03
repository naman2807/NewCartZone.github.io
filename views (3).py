from django.shortcuts import render
from django.http import HttpResponse
from .paytm import Checksum
from .models import Product, Contact, Order, Orderupdate
from math import ceil
from django.views.decorators.csrf import csrf_exempt

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';




def searchmatch(query,item):
    if query in item.desc.lower() or query in item.prod_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query=request.GET.get('search')
    allprods = []
    catprod = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        products=[item for item in prodtemp if searchmatch(query,item)]
        n = len(products)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(products)!=0:
            allprods.append([products, range(1, nslides), nslides])

    params = {'allprods': allprods}
    if len(allprods) == 0:
        return HttpResponse("This item is not available")
    else:
        return render(request, 'shop/index.html', params)


def index(request):
    allprods = []
    catprod = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        products = Product.objects.filter(category=cat)
        n = len(products)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([products, range(1, nslides), nslides])

    params = {'allprods': allprods}

    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank=False
    if request.method == "POST":
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        desc = request.POST.get("desc", "")
        contact = Contact(name=name, phone=phone, email=email, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html',{'thank':thank})




def prodview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        itemsJson = request.POST.get("itemsJson", "")
        name = request.POST.get("name", "")
        amount = request.POST.get("amount", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")

        zip_code = request.POST.get("zip", "")
        order = Order(items_json=itemsJson, name=name, phone=phone, email=email, address=address, city=city,
                      state=state, amount=amount, zip_code=zip_code)
        order.save()
        update = Orderupdate(order_id=order.order_id, update_desc="Congrats, Your order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        param_dict={
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH']= Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html',{'param_dict':param_dict})
    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    form=request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=="CHECKSUMHASH":
            checksum=form[i]
    verify= Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print("Order Successful")
        else:
            print("Order Was not successful Because"+response_dict["RESPMSG"])
    return render(request,"shop/paymentstatus.html", {'response':response_dict})