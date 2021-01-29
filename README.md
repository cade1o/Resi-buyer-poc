# Resi-Buyer (TPRB2)

# Getting Started
* A Python Environment:<br>
This project requires Python environment.<br> 
If you don't already have one or looking for a good one then Anaconda does a great job at managing it. https://docs.anaconda.com/anaconda/install/ will tell you how to install.

* Install pip on your Python environment
* Install Requirements using the requirements.txt:<br>
```
pip install -R requirements.txt
```
* Run server using:
```
python manage.py runserver
```

### Database Issues
So far we've had a lot of issues gettng the databases for this project to work 100% of the time. If you see an error saying "unapplied migrations", or the website crashes when you try to visit the order placing/viewing pages, then here are a few things you can try.

The first thing to try is just deleting your ```TPRB2``` branch and then recloning it from GitHub. Through the process of committing/pulling different files, sometimes the database/migration files within Django become unsynced. Recloning the entire repository will help prevent this from happening locally on your machine. Make sure you have committed all changes you want to save before doing this though, as they will be lost otherwise.

If this didn't work, the second thing to try is to get Django to migrate the databases. To do this, run the following steps in order.
1. Run ```python manage.py makemigrations ResiBuyer```
2. Run ```python manage.py migrate```
3. Run ```python manage.py migrate --run-syncdb``` (optional)
4. Now run the server again (using ```python manage.py runserver```) and see if it works

If this didn't work, try deleting all the contents of the ```ResiBuyer/migrations``` folder, as well as all the contents of any ```__pycache__``` folders (eg. ```ResiBuyer/__pycache___``` and ```ResiBuyer/utils/__pycache__```). Then you can try the 4 steps above, which should (hopefully) now work correctly.

If you are still running into problems then let the group know as early as possible, as these issues can take some time to solve.

### Basics of using HTML Templates in dJango
1. Create Your HTML template
2. Place it in the templates folder within the dJango app, somewhere that makes sense
3. Create a view within views.py<br>
For example: the following code will render "index.html" from UI/index/ within templates/
```
def index(request):
    return render(request, 'UI/index/index.html')
```
4. Create an appropriate URL route within urls.py.<br>
For example: the following code will call the "index" function from views when the base URL or http://127.0.0.1:8000/ is accessed.
```
urlpatterns = [
    path('', views.index),
]
```
5. Load up the your browser and access the URL you created\
Note: If you wish to include any static files like css, js or images in your template please refer to guide to static files below.<br>
See https://docs.djangoproject.com/en/3.1/intro/tutorial03/ for more information<br>

### Static Files
Static files are any files included in your HTML templates that do not change, i.e Javascript, CSS or image files to name a few.\
To include static files in your HTML:
1. Create your static file
2. Store the static file in the "static" folder within the dJango app, somewhere that makes sense
3. Within your HTML template place the following code
```
{% load static %}
```
Note: this is only require once per HTML document<br>

4. In the element that includes a static file make ```src="{% static path/to/static/your_static.js %}```<br>
For example in index.html:
```
{% load static %}
<link href="{% static 'UI/css/main.css' %}" rel="stylesheet">
```
See https://docs.djangoproject.com/en/3.1/howto/static-files/ for more information

### Setting Up Decentralisation Simulation
Decentralisation is the process where the blockchain aspect of the software is distributed and maintained by a network of peers. To use a smaller scale demonstration, four different instances of the software will be set up to listen on four different ports. However they still communicate with each other via HTTP, thus it is entirely possible to connect a computer running the software halfway across the world.
The current peers listed on the network are the following:
```
127.0.0.1:8000
127.0.0.1:8001
127.0.0.1:8002
127.0.0.1:8003
```
To set up these different instances follow these steps
1. Open four terminal tabs in the TPRB2 folder. Make sure you have the same virtual environment for each of them if you are use virtual environments
2. With all the relevant packages installed ("pip install -R requirements.txt) run the command ```python manage.py runserver 8000```. This will start an instance of the software on 127.0.0.1:8000.
3. Repeat in the other 3 tabs changing the number at the end to 8001, 8002 and 8003 respectively.
4. You are done

### Interacting with the Blockchain
It is possible to see the current blockchain in the blockchain section of the website. It also possible to add another "peer" to the decentralised network through the "Join P2P network" section. All peers that part of the network will be listed here too.<br>
To add an unconfirmed transaction to the the blockchain Simply add a new order and generate tracking items in the main section. This will automatically be broadcast out to all peers currently on the network.<br>
To mine a new block ANY PEER simply has to call the ```/mine/``` endpoint. For Example ```127.0.0.1:8001/mine/```. This will automatically broadcast the block out to the rest of the peers
