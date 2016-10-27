from django.shortcuts import render
from .forms import PostForm
from result import Result

resultObj = Result("./index/frwiki.xml")

# Create your views here.
def index(request):
	print "Request", request.method, "sended by", request.get_host()
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			mots_cles = post.mots_cles
			code, pages = resultObj.getResultForRequest(mots_cles)
			form = PostForm()
			#print code, "/", pages
			return render(request, 'index/index.html', {'form': form, 'mots_cles': mots_cles, 'code': code, 'pages': pages})
		else:
			form = PostForm()
			return render(request, 'index/index.html', {'form': form})
	else:
		form = PostForm()
		return render(request, 'index/index.html', {'form': form})
