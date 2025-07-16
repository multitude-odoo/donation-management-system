from odoo import http
from odoo.http import request

class DonorWebsiteController(http.Controller):

    @http.route('/donors', type='http', auth='public', website=True)
    def list_donors(self, **kw):
        donors = request.env['donation.donor'].sudo().search([])
        return request.render('donation_system.donor_list_template', {
            'donors': donors
        })

    @http.route('/donor/<int:donor_id>', type='http', auth='public', website=True)
    def donor_detail(self, donor_id, **kw):
        donor = request.env['donation.donor'].sudo().browse(donor_id)
        return request.render('donation_system.donor_detail_template', {
            'donor': donor
        })



class DonationPortal(http.Controller):

    @http.route('/donate', type='http', auth='public', website=True, csrf=False)
    def donation_home(self, **kwargs):
        return request.render("donation_system.donation_selection_template", {})


    @http.route('/donate/form', type='http', auth='public', website=True)
    def donation_form(self, **kwargs):
        return request.render("donation_system.donation_form_template", {})