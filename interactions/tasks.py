# interactions/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Comment, Share


# ------------test task---------------------
@shared_task
def add(x, y):
    return x + y

# ---------------------- Notifications ----------------------
@shared_task
def send_like_notification(liker_username, author_email, post_excerpt):
    """
    Notify post author when their post is liked.
    """
    send_mail(
        subject="📌 New Like on Your Post",
        message=f"{liker_username} liked your post:\n\n“{post_excerpt}...”",
        from_email="noreply@nexus.com",
        recipient_list=[author_email],
        fail_silently=True,
    )
    return f"✅ Sent like notification to {author_email}"


@shared_task
def send_comment_notification(commenter_username, author_email, post_excerpt, comment_content):
    """
    Notify post author when someone comments.
    """
    send_mail(
        subject="💬 New Comment on Your Post",
        message=(
            f"{commenter_username} commented on your post:\n\n"
            f"Post: “{post_excerpt}...”\n"
            f"Comment: “{comment_content}”"
        ),
        from_email="noreply@nexus.com",
        recipient_list=[author_email],
        fail_silently=True,
    )
    return f"✅ Sent comment notification to {author_email}"


@shared_task
def send_share_notification(sharer_username, author_email, post_excerpt):
    """
    Notify post author when their post is shared.
    """
    send_mail(
        subject="🔗 Your Post Was Shared",
        message=f"{sharer_username} shared your post:\n\n“{post_excerpt}...”",
        from_email="noreply@nexus.com",
        recipient_list=[author_email],
        fail_silently=True,
    )
    return f"✅ Sent share notification to {author_email}"


# ---------------------- Maintenance Tasks ----------------------
@shared_task
def cleanup_old_comments(days=30):
    """
    Delete comments older than X days.
    """
    cutoff = timezone.now() - timezone.timedelta(days=days)
    deleted, _ = Comment.objects.filter(created_at__lt=cutoff).delete()
    return f"🗑 Deleted {deleted} old comments"


@shared_task
def count_total_shares():
    """
    Return total shares count.
    (You can expose this via GraphQL if you want analytics.)
    """
    return Share.objects.count()
