from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Participation

def event_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    is_participating = False

    if user.is_authenticated:
        is_participating = Participation.objects.filter(event=event, user=user).exists()

        if request.method == 'POST':
            if 'confirm' in request.POST:
                Participation.objects.get_or_create(event=event, user=user)
            elif 'cancel' in request.POST:
                Participation.objects.filter(event=event, user=user).delete()
            return redirect('event_detail', event_id=event.id)

    participants_count = Participation.objects.filter(event=event).count()
    return render(request, 'event_detail.html', {
        'event': event,
        'is_participating': is_participating,
        'participants_count': participants_count,
    })
