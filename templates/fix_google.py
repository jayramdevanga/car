import os
import sys
import django

# Tell Python to look one folder up so it can see your 'projrct' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projrct.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
# ... keep the rest of the code exactly the same below ...