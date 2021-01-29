# Templates, Django and Bootstrap

This folder contains all of the current pages of the website.

They are designed using the Bootstrap library, and are being served up with Django. You should not have to download anything related to Bootstrap in order to correct view these pages.

The basic template for each page is in the basic_template folder, and it primarily consists of the navigation bar at the top and the sidebar. People can feel free to edit either of these elements, but editing should be done in the basic_template.html page rather than in the subpages in order to preserve consistency across the pages.

If you want to create a new page, you should take advantage of Django templates to use the existing navigation bar and sidebar. The order_place, order_view and index pages show examples on how to do that. Contact Brandon if there are any questions, or consult the links below. The HTML you put in the 'content' block will appear in the main section of the page. You will likely also need to add your page to the views.py and urls.py files.

One of the primary advantages of Bootstrap is its predefined styles, and its automatic handling of adjustable UI based on window size. Ideally if you are adding elements, you should use the CSS classes Bootstrap provides (everything should still work if you just use normal HTML/CSS though). Look at the linked documentation below if you want to see the available styles and guides on how to use them.

Using Bootstrap also adds jQuery, which you can use when writing JavaScript if you want (you should still be able to write normal JavaScript though).

# Links

Bootstrap Documentation: https://getbootstrap.com/docs/4.5/getting-started/introduction/
jQuery Documentation: https://api.jquery.com/

Some Links from Ragav:
- Django template inheritance: https://docs.djangoproject.com/en/3.1/ref/templates/language/#id1
- Django template variables: https://docs.djangoproject.com/en/3.1/ref/templates/language/#variables
- Simple example to send data from backend to frontend: https://stackoverflow.com/questions/53057621/django-pass-variable-into-template/53059318
- User authentication: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication
- A quick start to sending data from frontend to backend: https://docs.djangoproject.com/en/3.1/intro/tutorial04/#write-a-minimal-form