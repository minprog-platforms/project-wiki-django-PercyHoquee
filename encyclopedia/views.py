from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django import forms
from random import randint

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title:")

    content = forms.CharField(label="Content:", widget=forms.Textarea)

class EditEntryForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    result = util.get_entry(title)

    if result == None:
        return render(request, "encyclopedia/non_exist_error.html")
    else:
        html = markdown2.markdown(result)

        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "title": title
        })


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            existing = util.list_entries()

            if title in existing:
                return render(request, "encyclopedia/already_exist_error.html")
            else:
                util.save_entry(title, content)

                return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/new_entry.html", {
                "form": form 
            })

    return render(request, "encyclopedia/new_entry.html", {
        "form": NewEntryForm()
    })


def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form 
            })
    else:
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "form": EditEntryForm(initial={'content': content}),
            "title": title
        })


def search(request):
    query = request.GET.get("q")

    all = util.list_entries()

    subs = []

    for entry in all:
        if entry.lower() == query.lower():
            return HttpResponseRedirect(f"{entry}")
        
        if query.lower() in entry.lower():
            subs.append(entry)

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": subs
    })


def random(request):
    entries = util.list_entries()

    index = randint(0, len(entries) - 1)

    random_entry = entries[index]

    return HttpResponseRedirect(f"{random_entry}")
