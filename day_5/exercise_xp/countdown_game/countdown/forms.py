from django import forms


class WordGuessForm(forms.Form):
    guess = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'}),
        label='Your Guess'
    )

    def clean_guess(self):
        guess = self.cleaned_data.get('guess')
        if guess == "some_invalid_value":
            raise forms.ValidationError('Invalid guess. Please try again.')
        return guess
