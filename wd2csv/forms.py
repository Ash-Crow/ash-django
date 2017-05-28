import re
from django import forms


class MultiEntityField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split('\r\n')

    def validate(self, value):
        """Check if value consists only of valid Wikidata IDs."""
        # Use the parent's handling of required fields, etc.
        super(MultiEntityField, self).validate(value)
        for entity in value:
            if entity[0] not in ('L', 'P', 'Q') or not entity[1:].isdigit():
                raise forms.ValidationError("Please enter only valid IDs")


class MultiLanguagesField(forms.CharField):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid Wikidata IDs."""
        # Use the parent's handling of required fields, etc.
        super(MultiLanguagesField, self).validate(value)
        for tag in value:
            if not re.match("^[a-z-]+$", tag.strip()):
                raise forms.ValidationError("This language tag seems invalid: {}".format(tag))


class QueryForm(forms.Form):
    qids = MultiEntityField(widget=forms.Textarea,
                            label="Qids (one per line)")
    pids = MultiEntityField(widget=forms.Textarea,
                            required=False,
                            label="Pids (optional, one per line)")
    languages = MultiLanguagesField(max_length=200,
                                    initial="en, fr",
                                    required=False)
    return_labels_for_values = forms.BooleanField(required=False)
    return_labels_for_properties = forms.BooleanField(required=False)
