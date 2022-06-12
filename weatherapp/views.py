from weatherapp.models import City
from django.shortcuts import get_object_or_404, redirect, render
from decouple import config
import requests
from pprint import pprint
from django.contrib import messages

def home(request):
    API_key = config('API_KEY')

    u_city=request.GET.get('name')
    # print(city)
    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_key}&units=metric"
        response = requests.get(url)
        if response.ok: # yazilan sehir db de varsa response ok olur.(400 altinda ise)
            content = response.json()
            r_city=content['name']
            if City.objects.filter(name=r_city):
                messages.warning(request,'City already exists!')
            else:
               City.objects.create(name=r_city) 
               messages.success(request,'city created!')
        else:
            messages.error(request,'There is no city!')

        return redirect('home')

    # city='Yozgat'
    city_data=[]
    cities=City.objects.all()
    for city in cities :
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric"
        # ! request kutuphanesini yukle  url den bilgi cek sonucunda json data verecek
        response = requests.get(url)
        # !response json formatinda gelir python dict. formatina cevirmek icin yazdik
        content = response.json()
        # print(content)
        # pprint(content)
        # ! sergilemek istediklerini context(data) e yaz
        data={
            'city':city, #! bu city i db den aliyor bunun icinde id var delete de id yi kullanacagimiz icin bunu kullandik.
            # 'city':content['name'], bu city adini url den aliyor icinde id yok
            'temp':content['main']['temp'],
            'desc':content['weather'][0]['description'],
            'icon':content['weather'][0]['icon'],

        }
        city_data.append(data)
        # pprint(city_data)

    contex={
       'city_data':city_data, 
    }
    return render(request, 'weatherapp/home.html',contex)


def delete_city(request,id):
    city=get_object_or_404(City,id=id)
    city.delete()
    messages.success(request, 'City deleted!')
    return redirect('home')











