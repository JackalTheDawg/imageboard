from django.http import HttpResponse
from django.shortcuts import render
import os

def render_content(request, content_path):
    if "mime" in request.data == "image":
        return render('image.html', {"picture_path": content_path})
    if "mime" in request.data == "video":
        return render("video.html", {"video_path": content_path})


def save_content(request):

    location = request.POST['location'].split("=")

    path = f"static/media/{location[0]}/{location[1]}/{request.POST['mime']}"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/{request.POST['filename']}", "wb") as f:
        f.write(request.FILES['file'].file.getvalue())
        f.close()

    return HttpResponse(path)