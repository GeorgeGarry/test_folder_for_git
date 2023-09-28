from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class HighScore(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_player")
    score = models.IntegerField()

    def __str__(self):
        return {
            "player": self.player,
            "score": self.score
        }

class Word(models.Model):
    word_text = models.CharField()
    word_length = models.PositiveIntegerField()

    def __str__(self):
        return {
            "word": self.word_text,
            "length": self.word_length
        }

