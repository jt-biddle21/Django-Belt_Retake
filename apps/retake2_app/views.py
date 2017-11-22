from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render(request, 'retake2_app/index.html')


def register(request):
    response = User.objects.basic_validator(request.POST, "Register")
    if type(response) == list:
        for error in response:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = response.id
    messages.success(request, "Registration Complete!")
    return redirect('/')


def login(request):
    response = User.objects.basic_validator(request.POST, "Login")
    if type(response) == list:
        for lerror in response:
            messages.error(request, lerror)
        return redirect('/')
    request.session['user_id'] = response.id
    return redirect('/loggedin')


def loggedin(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    messages.success(request, "Logged In!")
    discontext = {
        "wishes": Wishlist.objects.exclude(wishedby=User.objects.get(id=request.session['user_id'])),#worked on it for hour 1/2. Cant exclude... even referenced quotes assigment
        "mywishes": User.objects.get(id=request.session['user_id']).wishes.all(),
        "test": User.objects.get(id=request.session['user_id']).items.all(),
    }
    return render(request, 'retake2_app/accounthome.html', discontext)


def additem(request):
    return render(request, 'retake2_app/additem.html')


def itemadded(request, number):
    response = User.objects.basic_validator(request.POST, "NewItem")
    if type(response) == list:
        for perror in response:
            messages.error(request, perror)
        return redirect('/items/add')
    user = User.objects.get(id=number)
    w = Wishlist.objects.create(item=request.POST['newitem'], users=user)
    w.save()
    User.objects.get(id=number).items.add(w)
    return redirect('/loggedin')


def wishadd(request, number):
    user = User.objects.get(id=request.session['user_id'])
    wish = Wishlist.objects.get(id=number)
    user.wishes.add(wish)
    return redirect('/loggedin')


def show(request, number):
    context = {
        "item": Wishlist.objects.filter(id=number),
        "users": User.objects.filter(wishes=number)
    }
    print (User.objects.filter(wishes=number))
    return render(request, "retake2_app/showitem.html", context)

# def about(request, number):
#     usercontext = {
#         "count": len(Quotes.objects.filter(users_id=number)),
#         "quotes": Quotes.objects.filter(users_id=number),
#         "username": User.objects.get(id=request.session['user_id']),
#     }
#     return render(request, 'retake_app/aboutme.html', usercontext)


def delete(request, number):
    Wishlist.objects.get(id=number).delete()
    return redirect('/loggedin')


def remove(request, number):
    Wishlist.objects.get(id=number).wishedby.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/loggedin')


def logout(request):
    del request.session['user_id']
    return redirect('/')
