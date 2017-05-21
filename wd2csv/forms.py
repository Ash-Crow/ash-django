from django import forms


class QueryForm(forms.Form):
    qids = forms.CharField(widget=forms.Textarea,
                           label="Qids (one per line)")
    pids = forms.CharField(widget=forms.Textarea,
                           required=False,
                           label="Pids (optional, one per line)")
    languages = forms.CharField(max_length=200,
                                initial="en, fr",
                                required=False)
    return_labels_for_values = forms.BooleanField(required=False)
    return_labels_for_properties = forms.BooleanField(required=False)
