# Intro
This is a Simple yet highly customisable CMS starter project, built with Django 4.2 and Python 3.10. Mainly focusing on making things easy enough to be extended, but also being able to provide an immediate CMS experience without the need for huge modification. Feel free to use it as a starting point.

# Live site demo
[Whatever Boardgame Note](https://whateverboardgame.com/)

# Features
* Build with the concept of Page, Post, Album and Writer
* Make use of Django's admin panel for content management
* Beautiful font with [Google Font](https://fonts.google.com/)
* CSS Styling with [Django Tailwind](https://django-tailwind.readthedocs.io/en/latest/index.html)
* Richtext Editor and image upload capability with [Django CKEditor](https://django-ckeditor.readthedocs.io/en/latest/)

# Setup
1. Clone this repo and switch to that directory in the terminal.
2. Create Python venv to avoid dependency conflict.
```code
python -m venv .venv
```
3. Start the python venv
```code
source .venv/bin/activate # If you are using Linux
.venv\scripts\activate # If you are using Windows
```
4. Install dependencies. In case you are having trouble installing mysqlclient, refer to https://pypi.org/project/mysqlclient/ for the required headers and libraries.
```code
pip install -r requirements.txt
```
5. Copy db.cnf.example and name it db.cnf. Modify this file with your DB connection info. Don't forget to create the desired database by yourself first.
6. Modify cms_starter/settings.py according to your environment and requirements, especially NPM_BIN_PATH and MEDIA_ROOT.
7. Execute the following command to create the necessary tailwind CSS assets
```code
python manage.py tailwind init
python manager.py tailwind install
```
8. Create DB Tables. Check your db setting in db.cnf if you encounter errors.
```code
python manager.py makemigrations
python manager.py migrate
```
9. Start the Tailwind auto build services
```code
python manager.py tailwind start
```

10. Open a new terminal, switch to repo, start the python venv (refer to step 3), and execute the following command to start the Django development server
```code
python manager.py runserver
```

# Data Preparation
1. Create an admin account
```code
python manager.py createsuperuser
```
2. Use your admin account to login to the system. The default admin panel is located at http://localhost:8000/admin/

3. Create the pages with specific slugs. Remember to tick the 'published' checkbox.

|Page|Slug|Comment|
| -- | -- | -- |
| Home| home | Home page|
| About | about-us | About Us |
| Contact | contact-us | Contact Us |

If that is not what you need, feel free to modify the links in theme/templates/base.html

4. Create a group named 'Writer' for writers. You can grant every permissions that start with cms, except 'cms | pages', 'cms | page image' and 'cms | profile'. For 'cms | profile', you can grant 'cms | profile | Can change profile' and 'cms | profile | Can view profile'. A writer can only see and modify his profile in the admin panel.

5. Create accounts for the writers in the 'User' section of the admin panel. Don't forget to add them to the 'Writer' group. Also please check 'Staff status' in the panel or they woun't be able to login to the admin portal.

6. Writers can log in to the admin panel with their account and perform a limited number of actions. They can modify their profile and password in the admin panel as well.

# Deployment
Read and understand https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/ first.

In cms_starter/settings.py, remark the settings in "Env - Local" section. Un-remark the settings in "Path - Production" section. Change the values according to your environment.

You may need to change ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS and INTERNAL_IPS as well.

Transfer the code to the target machine.

Setup the python env(venv) just like how you did in the Setup procedures. 

Instead of starting the tailwind CSS building server, you now build the CSS by using the following command
```code
python manager.py tailwind build
```

Copy the static files to the STATIC_ROOT
```
python manager.py collectstatic
```

The compiled assets should be ready in the STATIC_ROOT that you have specified in cms_starter/settings.py.

Finally, instead of starting the development server in step 10, start the gunicorn production server in the project root.
```code
# If you want to see the output
gunicorn cms_starter.wsgi

# Or if you want to run it in daemon
gunicorn cms_starter.wsgi --daemon
```

# Settings
Please refer to cms_starter/settings.py

# Assets Directory
* Static Assets are located in the static folder
* Files are uploaded to the media folder by default

# Template
Templates files are located at theme/template

# Additional CSS
* Additional CSS rules are written in theme/static_src/styles.css
* Tailwind CSS config files are located at theme/static_src

# Admin Models
Please refer to cms/admin.py

# Views
* Refer to cms/views.py for CMS view
* HTTP 404 views are defined at cms_starter/views.py and cms_starter/urls.py

# Utils
Utils are stored at cms_starter/utils.py

# Models
All models are stored in cms/models.py
## Page
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|title|CharField|Y||
|content|TextField|Y||
|published|BooleanField|Y||
|slug|CharField|Y|Y|
|parent_page|FK('self')||Y|
|created_at|DateTimeField|Y||
|modified_at|DateTimeField|Y||
|child_pages|Ref('self')||
|images|M2M('Image')||

## ArticleCategory
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|name | CharField|Y||
|cover_image | ImageField|||
|description |TextField||||
|slug|CharField|Y|Y|
|articles|M2M('Article')|||

## Article
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|title|CharField|Y||
|cover_image|ImageField||
|summary|CharField||
|content|TextField||
|reference_url|CharField||
|youtube_video_id|CharFieldY|
|slug|CharField|Y|Y|
|created_by|FK(User)|Y||
|created_at|DateTimeField|Y|
|modified_at|DateTimeField|Y|
|published|BooleanField|Y|
|categories|Ref('ArticleCategory')||
|tags|Ref('Tag')||
|images|M2M('Image')||

## Tag
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|name|CharField|Y||
|articles|M2M('Article')|||


## Album
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|name|CharField|Y||
|slug|CharField|Y|Y|
|published|BooleanField|Y||
|created_at|DateTimeField|Y||
|created_by|FK('User')|Y||
|cover_image|ImageField||
|short_description|CharField|||
|description|TextField||
|album_images|Ref('AlbumImage')||

## Image
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|image |ImageField|Y||
|caption|CharField|Y||
|published|BooleanField|Y||
|articles|M2M('Article')||
|pages|M2M('Page')||

## AlbumImage (One Image to One AlbumImage)
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|image|O2O('Image')|Y|Y|
|album|FK('Album')|Y||
|display_order|IntegerField|Y||

## ArticleTag (Article <- M2M -> Tag)
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|article|FK('Article')|Y|*|
|tag|FK('Tag')|Y|*|

## ArticleImage (Article <- M2M -> Image)
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|article|FK('Article')|Y||
|image|FK('Image')|Y|Y|
|display_order|IntegerField|Y||

## PageImage (Page <- M2M -> Image)
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|page|FK('Page')|Y||
|image|FK('Image')|Y|Y|
|display_order|IntegerField|Y||

## Profile (One Profile to One User, accessed by user.profile)
| Field | Type | Required | Unique |
| ---   | ---  |  --      |      --|
|user|O2O('User')|Y|Y|
|nickname|CharField|Y|Y|
|title|CharField|||
|avatar|ImageField|||
|bio|TextField|||
|location|CharField|||

# URL Pattern
All url patterns are defined in cms/urls.py
| Pattern | View | Name | Filter / Select Options|
| --      | --   |  --  | --     |
| / | views.index|  index |Redirect to /page/home|
|/page/<str:slug>/| views.page | page||
|/articles/|views.articles|articles|q: keyword, wrtier: nickname, tag:slug, category: slug, page: n|
|/articles/<int:id>-<str:slug>|views.article|article||
|/albums/|views.albums|albums|page: n|
|/albums/<int:id>-<str:slug>|views.album|album||
|/writers|views.writers|writers||
|/writers/<int:id>-<str:nickname>|views.writer|writer||


# License
The MIT License
