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

    @http.route(['/donate/individual-auth-choice'], type='http', auth="public", website=True)
    def individual_auth_choice(self):
        return request.render("donation_system.individual_auth_choice_page")

    @http.route(['/donate/signup-choice'], type='http', auth="public", website=True)
    def signup_choice(self):
        return request.render("donation_system.signup_choice_page")

    @http.route(['/singpass/login'], type='http', auth="public", website=True)
    def singpass_login(self):
        return request.render("donation_system.singpass_login")

    @http.route('/signup/info', type='http', auth='public', website=True)
    def signup_info(self, **kw):
        # If data is coming from SingPass, pre-fill
        user_data = request.session.get('singpass_user_data', {})
        return request.render('donation_system.signup_info_form', user_data)

    @http.route('/signup/save', type='http', auth='public', website=True, csrf=False)
    def signup_save(self, **post):
        # Save to CRM or Contact model (example uses res.partner)
        request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('contact'),
            'x_nric': post.get('nric'),
            'x_dob': post.get('dob'),
            'x_sex': post.get('sex'),
        })

        return request.redirect('/thank-you')

    @http.route('/thank-you', type='http', auth='public', website=True)
    def thank_you(self):
        return "<h2>Thank you for signing up!</h2>"