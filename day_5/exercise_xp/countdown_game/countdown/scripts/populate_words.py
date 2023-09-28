import os
import sys
sys.path.append('/week_24/day_5/exercise_xp/countdown_game')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "countdown_game.settings")

# Now, you can safely import Django-related modules after setting the environment:
import django

django.setup()
from countdown.models import Word


def populate():
    with open('./scripts/all_words.txt', 'r') as f:
        words = f.readlines()

    word_instances = []  # Create a list to hold all the Word instances

    for word_text in words:
        word_text = word_text.strip()  # Remove any leading/trailing whitespace
        word_length = len(word_text)
        word_instance = Word(word_text=word_text, word_length=word_length)
        word_instances.append(word_instance)

    # Perform bulk insertion:
    Word.objects.bulk_create(word_instances)

    print(f"{len(word_instances)} words added to the database!")


if __name__ == '__main__':
    populate()
