from django.shortcuts import redirect, render, HttpResponse 
# from stackoverflowApp.models import Stackoverflow
import requests
from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

url = 'https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&site=stackoverflow'

def home(request):
    # print('HOME')
    # print(request.query_params)
    context = {'success': False, 'res': 'Search'}
    # print(context, request.session)
    # print('GET', request.method)
    if 'count' not in request.session:
        request.session['count'] = 0
        val = datetime.time(datetime.now()).__str__().split('.')[0]
        request.session['time'] = val
        request.session['day_count'] = 0
        val = datetime.time(datetime.now()).__str__()
        request.session['day_time'] = val.split('.')[0]
        # print('1ST',request.session['count'], request.session['time'])
        # print('2ND',request.session['day_count'], request.session['day_time'])
    print('ReInitialCOUNT&TIME',request.session['count'], request.session['time'])
    print('ReInitialDAYcount&DAYtime',request.session['day_count'], request.session['day_time'])
    # print(type(request.session['count']), type(request.session['day_count']))
    # sp = datetime.time(datetime.now()).__str__().split('.')[0].split(':')
    # sec = int(sp[0])*3600+int(sp[1])*60+int(sp[2])
    # print(sp, sec)
    # print(datetime.time(datetime.now()).__str__().split('.')[0])
    # sp = datetime.strptime(datetime.time(datetime.now()).__str__().split('.')[0], '%H:%M:%S') - datetime.strptime(request.session['time'], '%H:%M:%S')
    # print(sp)
    return render(request, 'index.html', context)


def search(request):
    print('SEARCH')
    # print((datetime.time(datetime.now()).__str__().split('.')[0]))
    # consumeTime = datetime.strptime(datetime.time(datetime.now()).__str__().split('.')[0], '%H:%M:%S')
    # ot = request.session['time']
    # print(consumeTime, ot) 
	
    # spent = datetime.strptime(datetime.time(datetime.now()).__str__().split('.')[0], '%H:%M:%S') - datetime.strptime(request.session['time'], '%H:%M:%S')
    # print(spent)
    # xyz=spent.__str__().split(':')
    # print(xyz)
    # sec = (int(xyz[0])*3600)+(int(xyz[1])*60)+int(xyz[2])
    # print(sec)
    # question = request.GET['title']
    # # print(question)
    # data = questionApi(question)
    # # print(data)
    # # return HttpResponse('it worked')
    # context = {'success':True, 'data': data, 'res': 'Result'}
    # return render(request, 'index.html', context)
    print(request.session['time'])
    print(datetime.strptime(request.session['time'], '%H:%M:%S'))
    spent = datetime.strptime(datetime.time(datetime.now()).__str__().split('.')[0], '%H:%M:%S') - datetime.strptime(request.session['time'], '%H:%M:%S')
    xyz=spent.__str__().split(':')
    sec = (int(xyz[0])*3600)+(int(xyz[1])*60)+int(xyz[2])
    print(request.session['count'], sec, request.session['day_count'])
    if request.session['count'] < 5 and sec < 60 and request.session['day_count'] < 100:
        question = request.GET.get('title')
        print(question)
        # return HttpResponse('if condition')
        request.session['count'] += 1
        request.session['day_count'] += 1
        data = questionApi(question)
        paginator = Paginator(data, 10)
        print(paginator.count)
        print(paginator.num_pages)
        print(paginator.page_range)
        page = request.GET.get('page',1)
        print(page)
        data = paginator.page(1)
        print(data)
        # print(len(data.object_list))
        # print(data.has_next())
        # if data.has_previous():
        #     data['has_previous'] = data.has_previous()
        #     data['previous_page_number'] = data.previous_page_number()
        print(data.has_next(), data.has_previous())
        # if data.has_next():
        #     data['has_next'] = data.has_next()
        #     data['next_page_number'] = data.next_page_number()

        # data['last_page'] = paginator.num_pages
        # data['current'] = page
        context = {'success':True, 'data': data, 'res': 'Result'}
        return render(request, 'index.html', context)
    else:
        print('SEC', sec)
        if sec > 60:
            request.session['count'] = 0
            val = datetime.time(datetime.now()).__str__().split('.')[0]
            request.session['time'] = val
            print(request.session['time'])
            message = {'answers': [{'title': 'You got 5 new search limit for this minute please search again'}]}
            # return JsonResponse(data)
            return JsonResponse(message)
        else:
            message = {'message': 'search limit over Please try after one min or start a new session', 'is_answered':'Day Count Left='+str(100-request.session['count_day']),'tags':'you can retry after: '+str(60-sec)+' seconds'}
    return JsonResponse(message)



# restapi to fetch data from stackoverflow
def questionApi(question):
    url = 'https://api.stackexchange.com/2.3/search/advanced'
    params = {
        # 'q': request.GET['title'],
        'q': question,
        'site': 'stackoverflow',
        'order': 'desc',
        'sort': 'activity'
    }
    # print(request.session)
    # print(request.GET['title'])

    data = requests.get(url, params).json()['items']
    # print('POST',request)
    # page = request.POST['page']
    # title = request.POST['title']
    # print(page)
    # print(title)
    # print(request)
    # stackof = Stackoverflow(page=page, title=title)
    # print(stackof)
    # stackof.save()
    # context = {'success':True, 'data':data.json(), 'page':page, 'title':title}
    # print(request.GET)
    # return render(request, "search.html", context)
    return data

def delsession(request):
    del request.session['count']
    del request.session['day_count']
    return redirect('/')