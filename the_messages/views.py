from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import ONGOING, UPCOMING, Message, MessageGroup
from .forms import CommentForm
from django.db.models import Q
from push_notifications.models import WebPushDevice
from django.http import JsonResponse, HttpResponse, HttpRequest
import json
import os
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

STATUSES = {
    "uc": "UPCOMING",
    "og": "ONGOING",
    "c": "COMPLETED"
}

# Create your views here.
def home(request):
    # Return last 3 messages
    last_messages = Message.objects.all().order_by('-date')
    # Find featured message, if any
    featured_message = Message.objects.filter(is_featured=True).first()
    if featured_message:
        # Ensure it's not in the last messages
        last_messages = [msg for msg in last_messages if msg.id != featured_message.id]
        # last_messages.insert(0, featured_message)

    last_messages = last_messages[:3]  # Ensure we still only have 3 messages

    # Find and return date for the first Sunday of next month
    today = datetime.today()
    first_day_next_month = (today.replace(day=1) + timedelta(days=31)).replace(day=1)
    first_sunday_next_month = first_day_next_month + timedelta(days=(6 - first_day_next_month.weekday()))
    first_sunday_this_month = today.replace(day=1) + timedelta(days=(6 - today.replace(day=1).weekday()))
    sunday_passed = True if datetime.today().date() > first_sunday_this_month.date() else False

    # Also return the first Wednesday of next month
    first_wednesday_next_month = first_day_next_month + timedelta(days=(2 - first_day_next_month.weekday() + 7) % 7)
    first_wednesday_this_month = today.replace(day=1) + timedelta(days=(2 - today.replace(day=1).weekday()))
    wednesday_passed = True if datetime.today().date() > first_wednesday_this_month.date() else False

    # Finally return the last Friday of this month
    last_day_this_month = (today.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    last_friday_this_month = last_day_this_month - timedelta(days=(last_day_this_month.weekday() - 4) % 7)
    friday_passed = True if datetime.today().date() > last_friday_this_month.date() else False

    return render(request, "the_messages/home.html", {
        "last_messages": last_messages,
        "featured_message": featured_message,
        "first_sunday_next_month": first_sunday_next_month,
        "first_sunday_this_month": first_sunday_this_month,
        "sunday_passed": sunday_passed,
        "first_wednesday_next_month": first_wednesday_next_month,
        "first_wednesday_this_month": first_wednesday_this_month,
        "wednesday_passed": wednesday_passed,
        "last_friday_this_month": last_friday_this_month,
        "friday_passed": friday_passed,
    })

def messages(request):
    query = request.GET.get('q', '')
    # Make note of message type too
    message_type = request.GET.get('type', '')
    # Finally, make note of the sort order
    sort_order = request.GET.get('sort', 'date_desc')
    results = Message.objects.all().order_by('-date')
    if query:
        results = results.select_related('author').filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(author__name__icontains=query) |
            Q(category__icontains=query)
        ).order_by('-date').distinct()
        if message_type:
            if message_type == "conference":
                results = results.filter(part_of_group=True, message_group__is_conference=True)
            else:
                results = results.filter(message_group__is_conference=False)
        if sort_order == "date_asc":
            results = results.order_by('date')
    if message_type and not query:
        if message_type == "conference":
            results = results.filter(part_of_group=True, message_group__is_conference=True).order_by('-date').distinct()
        else:
            results = results.filter(message_group__is_conference=False).order_by('-date').distinct()
        if sort_order == "date_asc":
            results = results.order_by('date')
    if sort_order == "date_asc" and not query and not message_type:
        results = results.all().order_by('date')

    page = request.GET.get('page', 1)
    paginator = Paginator(results, 24)
    results = paginator.get_page(page)

    return render(request, "the_messages/messages.html", {
        "page_obj": results,
    })

def search_messages(request):
    query = request.GET.get('q', '')
    # Make note of message type too
    message_type = request.GET.get('type', '')
    # Finally, make note of the sort order
    sort_order = request.GET.get('sort', 'date_desc')
    results = []
    if query:
        results = Message.objects.select_related('author').filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(author__name__icontains=query) |
            Q(category__icontains=query)
        ).order_by('-date').distinct()
        if message_type:
            if message_type == "conference":
                results = results.filter(part_of_group=True, message_group__is_conference=True)
            else:
                results = results.filter(message_group__is_conference=False)
        if sort_order == "date_asc":
            results = results.order_by('date')
    else:
        results = Message.objects.all().order_by('-date')

    # Implement pagination, 25 per page
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 24)
    results = paginator.get_page(page)

    return render(request, "the_messages/messages.html", {
        "page_obj": results
    })

def message_details(request, message_id):
    message = Message.objects.get(id=message_id)
    # Also return related messages in the same group if any
    # related_messages = Message.objects.filter(message_group=message.message_group).exclude(id=message.id)
    related_messages = Message.objects.select_related('author').filter(message_group=message.message_group).exclude(id=message.id) if message.part_of_group else []
    # If none, just get messages by the same author, up to 3
    if not related_messages:
        related_messages = Message.objects.select_related('author').filter(author=message.author).exclude(id=message.id)[:3]

    # If still none, get latest 3 messages
    if not related_messages:
        related_messages = Message.objects.select_related('author').exclude(id=message.id).order_by('-date')[:3]

    # Get comments for the message
    comments = message.comments.all().order_by('-created_at') # type: ignore

    # Return attachments as well, if any
    attachments = message.attachments.all() # type: ignore

    # Return length of first attachment in seconds if audio
    audio_length = None
    if attachments and attachments[0].media_type.type_name.lower() == 'audio':
        length_parts = message.message_length.split(':')
        if len(length_parts) == 2:
            audio_length = int(length_parts[0]) * 60 + int(length_parts[1])
        elif len(length_parts) == 3:
            audio_length = int(length_parts[0]) * 3600 + int(length_parts[1]) * 60 + int(length_parts[2])

    is_subscribed = False
    if "device_id" in request.session:
        is_subscribed = True

    return render(request, "the_messages/message_details.html", {
        "message": message,
        "related_messages": related_messages,
        "comments": comments,
        "attachments": attachments,
        "audio_length": audio_length,
        "is_subscribed": is_subscribed,
    })

# View just for adding comments to message
def add_comment(request, message_id):
    message = Message.objects.get(id=message_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            message.comments.create(**form.cleaned_data) # type: ignore

    return redirect('message_details', message_id=message.id)

def conferences(request):
    # list all conferences
    # Also return nearest upcoming conference
    upcoming_conference = MessageGroup.objects.filter(status=UPCOMING, is_conference=True).first()
    if not upcoming_conference:
        upcoming_conference = MessageGroup.objects.filter(status=ONGOING, is_conference=True).first()
    return render(request, "the_messages/conferences.html", {
        "conferences": MessageGroup.objects.filter(is_conference=True).exclude(id=upcoming_conference.id).order_by('-start_date'), # type: ignore
        "upcoming_conference": upcoming_conference,
        "statuses": STATUSES
    })

def conference_details(request, conference_id):
    conference = MessageGroup.objects.get(id=conference_id)
    messages = Message.objects.select_related('author').filter(message_group=conference).order_by('-date')

    return render(request, "the_messages/conference_details.html", {
        "conference": conference,
        "messages": messages
    })

def message_groups(request):
    return render(request, "the_messages/message_groups.html", {
        "message_groups": MessageGroup.objects.all().order_by('-start_date'),
    })

def search_message_groups(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = MessageGroup.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-start_date').distinct()

    return render(request, "the_messages/message_groups.html", {
        "message_groups": results
    })

def message_group_details(request, group_id):
    group = MessageGroup.objects.get(id=group_id)
    messages = Message.objects.select_related('author').filter(message_group=group).order_by('-date')

    return render(request, "the_messages/message_group_details.html", {
        "group": group,
        "messages": messages
    })

def about(request):

    return render(request, "the_messages/about.html", {})

def register_notifications(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        group_name = post_data.get("group", "message_requests")
        device_id = post_data.get("registration_id")

        if device_id:
            request.session["device_id"] = device_id

        print(device_id)

        WebPushDevice.objects.create(
            name=group_name,
            **{k: v for k, v in post_data.items() if k != "group"}
        )
    return JsonResponse(data={"result": True})

def service_worker(request):
    """
    Serve the service worker from the root path with proper content type
    """
    sw_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR, 'the_messages/static/navigatorPush.service.js')

    try:
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw_content = f.read()
        return HttpResponse(sw_content, content_type='application/javascript')
    except FileNotFoundError:
        # Fallback to try in BASE_DIR/static
        try:
            sw_path = os.path.join(settings.BASE_DIR, 'the_messages/static/navigatorPush.service.js')
            with open(sw_path, 'r', encoding='utf-8') as f:
                sw_content = f.read()
            return HttpResponse(sw_content, content_type='application/javascript')
        except FileNotFoundError:
            return HttpResponse('Service Worker not found', status=404)

@login_required
def upload_audio(request: HttpRequest, message_id):
    message = Message.objects.get(id=message_id)

    # Also return length of message in minutes
    length_parts = message.message_length.split(':')
    message_length_minutes = 0
    if len(length_parts) == 2:
        message_length_minutes = int(length_parts[0])
    elif len(length_parts) == 3:
        message_length_minutes = int(length_parts[0]) * 60 + int(length_parts[1])

    message_length_minutes += 1 if int(length_parts[-1]) > 0 else 0

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        # Handle file upload
        uploaded_file = request.FILES.get('audio_file')
        # Media type is from message, so always audio
        media_type = "Audio"
        # media_type = request.POST.get('media_type')
        if uploaded_file and media_type:
            # Save the attachment
            from .models import Attachment, MediaType
            media_type_obj, created = MediaType.objects.get_or_create(type_name=media_type)
            Attachment.objects.create(
                message=message,
                file=uploaded_file,
                media_type=media_type_obj
            )
            # redirect to admin site showing all messages
            return JsonResponse({"success": True, "redirect_url": "/storm_rider_admin/the_messages/message/"})
            # return redirect('message_details', message_id=message.id)

    return render(request, "the_messages/upload_audio.html", {
        "message": message,
        "message_length_minutes": message_length_minutes
    })

def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out successfully.")
    return redirect(settings.LOGOUT_REDIRECT_URL)
