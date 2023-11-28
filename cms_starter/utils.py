# Description: Utility functions for CMS
from django.utils.text import slugify

# Used by the CKEditor Uploader
def get_filename(filename):
    return filename.lower()

def to_slug(text):
    return slugify(text, allow_unicode=True)
