from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Query
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def aboutus(request):
    return render(request, 'aboutus.html')
    
def query(request):
    if request.method == 'GET':
        return render(request, 'query.html')
    else:
        if request.POST['name'] and request.POST['email'] and request.POST['querybody']:
            new_query = Query()
            new_query.name = request.POST['name']
            new_query.email = request.POST['email']
            new_query.body = request.POST['querybody']
            new_query.date_and_time_of_submission = timezone.datetime.now()
            new_query.save()
            return render(request, 'query.html', {'query_success': True})
        else:
            return render(request, 'query.html', {'query_error': 'Error, some fields have not been filled'})

@login_required
def viewqueries(request):
    if request.method == 'GET':
        if request.user.is_staff:
            queries = Query.objects.filter(is_deleted=False)
            return render(request, 'queries.html', {'queries': queries})
        else:
            return redirect('unauthorized')
    
@login_required
def replyquery(request, query_id):
    if request.method == 'POST':
        if request.user.is_staff:
            query = get_object_or_404(Query, pk=query_id)
            query.is_answered = True
            query.moderation_reply = request.POST['query_response']
            query.save()
            queries = Query.objects.filter(is_deleted=False)
            return render(request, 'queries.html', {'queries': queries, 'query_response': query})
        else:
            return redirect('unauthorized')
@login_required
def deletequery(request, query_id):
    if request.method == 'POST':
        if request.user.is_staff:
            query = get_object_or_404(Query, pk=query_id)
            query.is_deleted = True
            query.moderation_reply = request.POST['query_response']
            query.save()
            queries = Query.objects.filter(is_deleted=False)
            return render(request, 'queries.html', {'queries': queries, 'query_deletion': query})
        else:
            return redirect('unauthorized')
        
def unauthorized(request):
    return render(request, 'unauthorized.html')