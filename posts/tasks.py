from celery import shared_task
from django.core.mail import send_mail
from .models import Post


@shared_task
def notify_followers_new_post(post_id):
    """Notify followers when a user creates a new post."""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return "Post not found"

    author = post.author
    followers = author.followers.all()

    # In production, you’d send push notifications instead
    for f in followers:
        send_mail(
            subject=f"{author.username} created a new post!",
            message=post.content[:100],
            from_email="no-reply@nexus.com",
            recipient_list=[f.follower.email],
            fail_silently=True,
        )

    return f"Notified {followers.count()} followers."


@shared_task
def cleanup_old_posts(days=365):
    """Delete posts older than X days (default: 1 year)."""
    from django.utils import timezone
    from datetime import timedelta

    cutoff = timezone.now() - timedelta(days=days)
    old_posts = Post.objects.filter(created_at__lt=cutoff)
    count = old_posts.count()
    old_posts.delete()
    return f"Deleted {count} old posts."


@shared_task
def log_post_metrics():
    """Basic analytics job to log post stats."""
    total = Post.objects.count()
    print(f"📊 Total posts in DB: {total}")
    return total
