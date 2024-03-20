from .models import SiteInfo

def site_info(request):
    # Add the SiteInfo instance to the context
    return {'site_info': SiteInfo.get_site_info()}

