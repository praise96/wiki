import random
import markdown2
from django.shortcuts import render, redirect
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
#justmy entry
def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    else:
      
        content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
#oki we search hehe

def search(request):
    if request.method == "POST":
        query = request.POST.get('q', '').strip()
        content = util.get_entry(query)
        
        if content is not None:
            return redirect("entry", title=query)
            
        else:
            all_entries = util.list_entries()
            recommendation = []

            for entry in all_entries:
                if query.lower() in entry.lower():
                    recommendation.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })
        
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "Page already exists!"
            })

        util.save_entry(title, content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")

# uhm random funncction here 

def random_page(request):
    entries = util.list_entries()

    selected_page = random.choice(entries)
    return redirect("entry", title=selected_page)

#the hardest part yet QQ

def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    else:
        
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })