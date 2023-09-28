from django.http import request
from django.views import View
from django.shortcuts import render, redirect
from .models import Word, HighScore
from .forms import WordGuessForm
from .scripts.count_restrictions import is_user_input_valid
from django.db.models import Sum
import random

host_word = {
    "shuffled": "",
    "word_text": ""}
is_first_try = True
guesses_number = 3

score = 0


class CountdownGameView(View):

    def get(self, request):

        global is_first_try
        global host_word
        global score
        if is_first_try:
            word = Word.objects.filter(word_length__gte=6).order_by('?').first()
            shuffled = ''.join(random.sample(word.word_text, len(word.word_text)))
            host_word = {
                "word_text": word.word_text,
                "shuffled": shuffled,
            }
            is_first_try = False

        form = WordGuessForm

        print("the host word is: ", host_word)
        return render(request, 'countdown/game.html', {
            'shuffled_word': host_word["shuffled"],
            'form': form,
            'guesses_number': guesses_number,
            'total_score': score

        })

    def post(self, request):
        global host_word
        global is_first_try
        global guesses_number
        global score

        is_first_try = False
        user = request.user


        def score_count(user_word):
            print("score_count func:")
            print(user_word)
            print(host_word["word_text"])
            if len(user_word) == len(host_word["word_text"]):
                if user_word == host_word["word_text"]:
                    return 10
                return 8
            elif len(host_word["word_text"]) - len(user_word) == 1:
                return 5
            elif len(host_word["word_text"]) - len(user_word) == 2:
                return 3
            return 0

        print("POST host word:", host_word)

        form = WordGuessForm(request.POST)

        if form.is_valid():

            guess = form.cleaned_data['guess'].upper()
            if not is_user_input_valid(host_word["word_text"], guess):
                print("USER INPUT INCORRECT")
                return redirect('countdown_game')

            user_word_valid = Word.objects.filter(word_text=guess).first()
            if user_word_valid:
                print("the score is: ", score)
                score += score_count(user_word_valid.word_text)
                print(score_count(user_word_valid.word_text))
                print("Word Text:", user_word_valid.word_text)
            else:
                print("No matching word found.")

            guesses_number -= 1
            if guesses_number == 0:
                print("Game Over")
                guesses_number = 3
                is_first_try = True
                total_score = HighScore.objects.filter(player=user).aggregate(Sum('score'))['score__sum']
                if total_score is None:
                    total_score = 0
                game_over = {
                    "score": score,
                    "host_word": host_word["word_text"],
                    "total_scrore": total_score

                }
                score = 0
                word = Word.objects.filter(word_length__gte=6).order_by('?').first()
                shuffled = ''.join(random.sample(word.word_text, len(word.word_text)))
                host_word = {
                    "word_text": word.word_text,
                    "shuffled": shuffled,
                }

                return render(request, 'countdown/game.html', {
                    'shuffled_word': host_word["shuffled"],
                    'form': form,
                    'guesses_number': guesses_number,
                    'total_score': score,
                    'game_over': game_over

                })

            # Save the score
            HighScore.objects.create(player=user, score=score)

            return redirect('countdown_game')

        # If form is invalid, render the form with errors
        return render(request, 'countdown/game.html', {'form': form})
