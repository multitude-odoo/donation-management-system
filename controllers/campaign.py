from odoo import http
from odoo.http import request
import base64

class CampaignWebsiteController(http.Controller):

    @http.route('/campaigns', type='http', auth='public', website=True)
    def campaign_list(self, **kw):
        campaigns = request.env['donation.campaign'].sudo().search([])
        return request.render('donation_system.campaign_list_template', {
            'campaigns': campaigns
        })

    @http.route('/campaign/<int:campaign_id>', type='http', auth='public', website=True)
    def campaign_detail(self, campaign_id, **kw):
        campaign = request.env['donation.campaign'].sudo().browse(campaign_id)
        return request.render('donation_system.campaign_detail_template', {
            'campaign': campaign
        })

    @http.route('/create-campaign', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=False)
    def create_campaign(self, **post):
        if http.request.httprequest.method == 'POST':
            image_file = post.get('image')
            image_data = False
            if image_file and hasattr(image_file, 'read'):
                image_data = base64.b64encode(image_file.read())
            request.env['donation.campaign'].sudo().create({
                'title': post.get('title'),
                'description': post.get('description'),
                'goal_amount': float(post.get('goal_amount') or 0),
                'start_date': post.get('start_date'),
                'end_date': post.get('end_date'),
                'image': image_data,
            })
            return request.redirect('/campaigns')
        return request.render('donation_system.campaign_create_form_template')