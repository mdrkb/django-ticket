from django import forms


class TicketResponseForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your response', 'class': 'form-control'}), required=True)
    response = forms.CharField(widget=forms.HiddenInput, required=True)
