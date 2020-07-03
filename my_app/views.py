import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

# Create your views here.

base_craigslist_url='https://bangladesh.craigslist.org/search/?query={}'
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=base_craigslist_url.format(quote_plus(search))
    BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
    #print(final_url)
    response=requests.get(final_url)
    data=response.text
    #print(data)
    soup=BeautifulSoup(data,features='html.parser')
   #post_title=soup.find_all('a',{'class':'result-title'})

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url,post_price,post_image_url  ))

    print(post_title)
    print(post_url)
    print(post_price)
    #print(post_price)
    stuff_for_frontend ={
        'search':search,
        'final_postings': final_postings,
    }
    return render(request,'my_app/my_search.html',stuff_for_frontend)
