import requests

from django import forms

from molo.core.api import constants


class MainImportForm(forms.Form):
    url = forms.CharField(
        required=True,
        max_length=100,
    )

    content_type = forms.ChoiceField(
        choices=constants.CONTENT_TYPES,
        required=True,
        widget=forms.RadioSelect
    )

    def clean_url(self):
        url = self.cleaned_data["url"]
        response = requests.get(
            url="http://localhost:8000/api/v1/pages/"
        )

        if not (response.status_code == 200):
            self.add_error("url", forms.ValidationError(
                "Please enter a valid URL."
            ))

        return url


class ArticleImportForm(forms.Form):
    """
    Form to be used for importing articles.
    The list of available articles will be rendered dynamically
    """

    def __init__(self, *args, **kwargs):
        # generate fields dynamically for each article found in the response
        self.importer = kwargs.pop("importer")
        self.parent_id = kwargs.pop("parent")
        super(ArticleImportForm, self).__init__(*args, **kwargs)
        if self.importer and self.importer.articles():
            for i, article in enumerate(self.importer.articles()):
                self.fields["%s" %i] = forms.BooleanField(
                    label=article["title"]
                )
                self.fields["%s" % i].required = False

    def save(self):
        # soe articles were selected, save them
        selected_choices = [int(k) for k, v in self.cleaned_data.items() if v]
        self.importer.save_articles(
            ids=selected_choices, parent_id=self.parent_id
        )
        return self.importer
