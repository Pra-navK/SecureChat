from django.db import models

class user(models.Model):
    name = models.CharField(max_length=100)
    uniqueid=models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', db_index=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', db_index=True)

    encrypted_message = models.TextField()   # instead of content
    encrypted_key = models.TextField(null=True, blank=True)  # for hybrid encryption

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'receiver']),  # conversation queries
            models.Index(fields=['receiver', 'timestamp']),  # inbox queries
            models.Index(fields=['sender', 'timestamp']),  # sent messages
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message from {self.sender.name} to {self.receiver.name}'