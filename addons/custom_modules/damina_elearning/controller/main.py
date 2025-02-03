import requests
from odoo.http import request

from odoo.addons.website_slides.controllers.main import WebsiteSlides
class DeminaSearchCertificate(WebsiteSlides):
    def _get_slide_channel_search_options(self, my=None, slug_tags=None, slide_category=None, **post):
            try:
                 if slug_tags in ['deploma','certificate']:
                    tagg=request.env['slide.channel.tag'].sudo().search([('name','=',slug_tags.capitalize())])
                    slug_tags=f"{slug_tags}-{tagg.id}"
            except:
                pass
            return {
                'displayDescription': True,
                'displayDetail': False,
                'displayExtraDetail': False,
                'displayExtraLink': False,
                'displayImage': False,
                'allowFuzzy': not post.get('noFuzzy'),
                'my': my,
                'tag': slug_tags or post.get('tag'),
                'slide_category': slide_category,
            }