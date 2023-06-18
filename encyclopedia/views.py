from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from . import util
from .forms import SearchForm, NewPageForm, EditPageForm
from random import choice
import markdown2


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": SearchForm()},
    )


def wiki_page(request, title):
    if util.get_entry(title) is None:
        return render(
            request,
            "encyclopedia\error_page.html",
            {"entry": title, "uri": request.build_absolute_uri(), "form": SearchForm()},
        )

    return render(
        request,
        "encyclopedia/wiki_page.html",
        {
            "entry": markdown2.markdown(util.get_entry(title)),
            "title": title,
            "form": SearchForm(),
        },
    )


def search_results(request):
    
    form = SearchForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest
    
    query = form.cleaned_data["query"]
    entries = util.list_entries()
    if query in entries:
        return wiki_page(request, query)
    
    search_result = []
    for entry in entries:
        if query in entry:
            search_result.append(entry)
    return render(
        request,
        "encyclopedia\search_results.html",
        {"form": form, "search_result": search_result},
    )


def make_new_page(request):
    return render(
        request,
        "encyclopedia\\new_page.html",
        {
            "form": SearchForm(),
            "new_page_form": NewPageForm(),
        },
    )


def save_page(request):
    new_page_form = NewPageForm(request.POST)
    if not new_page_form.is_valid():
        return HttpResponseBadRequest
    
    title = new_page_form.cleaned_data["title"]
    if title in util.list_entries():
        return render(
            request,
            "encyclopedia\\new_error_page.html",
            {"title": title, "form": SearchForm()},
        )
    else:
        content = new_page_form.cleaned_data["content"]
        util.save_entry(title, content)
        return wiki_page(request, title)


def edit_page(request, title):
    content = util.get_entry(title)

    edit_form = EditPageForm(initial={'content': content})
    return render(
        request,
        "encyclopedia\edit_page.html",
        {
            "edit_form": edit_form,
            "form": SearchForm(),
            "title": title,
        },
    )


def save_changes(request, title):
    changes_form = EditPageForm(request.POST)
    if not changes_form.is_valid():
        return HttpResponseBadRequest
    
    util.save_entry(title, changes_form.cleaned_data["content"])
    return redirect('wiki_page', title = title)


def random_view(request):
    return redirect('wiki_page', title = choice(util.list_entries()))
