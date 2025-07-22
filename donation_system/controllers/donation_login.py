from odoo import http
from odoo.http import request


class DonationPortal(http.Controller):

    @http.route('/donate', type='http', auth='public', website=True, csrf=False)
    def donation_home(self, **kwargs):
        return request.render("donation_system.donation_selection_template", {})

    @http.route('/donate/form', type='http', auth='public', website=True, csrf=False)
    def donation_form(self, **post):
        # Store donation data in session
        request.session['donation_data'] = {
            'donor_type': post.get('donor_type'),
            'frequency': post.get('frequency'),
            'amount': post.get('amount'),
            'other_amount': post.get('other_amount'),
        }

        donor_type = post.get('donor_type')
        user = request.env.user
        is_logged_in = user and user.id != request.env.ref('base.public_user').id
        print("###############",is_logged_in)

        # Redirect based on donor type and login status
        if donor_type == 'individual':
            return request.redirect('/donate/individual-auth-choice')

        elif donor_type == 'corporate':
            if not is_logged_in:
                return request.redirect('/corporate/login')  # or your custom route
            else:
                return request.redirect('/signup/info')  # or another route if needed

        elif donor_type == 'anonymous':
            return request.redirect('/donate/anonymous')  # if you have an anonymous flow

        # Fallback
        return request.redirect('/donate/individual-auth-choice')

    @http.route(['/donate/individual-auth-choice'], type='http', auth="public", website=True)
    def individual_auth_choice(self):
        return request.render("donation_system.individual_auth_choice_page")

    @http.route(['/donate/signup-choice'], type='http', auth="public", website=True)
    def signup_choice(self):
        return request.render("donation_system.signup_choice_page")

    @http.route(['/singpass/login'], type='http', auth="public", website=True)
    def singpass_login(self):
        return request.render("donation_system.singpass_login")



    @http.route('/signup/info', type='http', auth='public', website=True, csrf=False)
    def signup_info_form(self, **kwargs):
        # Pass donation data to template
        donation_data = request.session.get('donation_data', {})
        return request.render("donation_system.signup_info_form", {'data': donation_data})

    @http.route('/signup/save', type='http', auth='public', website=True, csrf=False)
    def signup_save(self, **post):
        # Store personal data in session
        # Retrieve existing donation data from session
        donation_data = request.session.get('donation_data', {})

        # Extract posted fields
        name = post.get('name')
        nric = post.get('nric')
        email = post.get('email')
        contact = post.get('contact')
        postal_code = post.get('postal_code')
        street = post.get('street')
        unit_no = post.get('unit_no')
        sex = post.get('sex')

        # Update session data
        donation_data.update({
            'name': name,
            'nric': nric,
            'email': email,
            'contact': contact,
            'postal_code': postal_code,
            'street': street,
            'unit_no': unit_no,
            'sex': sex,
        })
        request.session['donation_data'] = donation_data

        # ✅ Create partner record in res.partner
        partner = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': contact,
            'identification_type': 'nric',
            'identification_number': nric,
            'street': street,
            'zip': postal_code,
            'donor_type': 'personal',  # assumes custom field
            'is_donor': True,  # assumes custom field
            'sex': sex, # assumes custom field or existing
            # 'unit_no': unit_no,

        })

        # Optional: store created partner ID in session
        donation_data['partner_id'] = partner.id
        request.session['donation_data'] = donation_data

        return request.redirect('/donate/payment/step')

    @http.route('/donate/payment/step', type='http', auth='public', website=True, csrf=False)
    def donation_payment_step(self, **kwargs):
        data = request.session.get('donation_data', {})
        return request.render("donation_system.donation_payment_step", {'data': data})

    @http.route('/donate/payment/confirm', type='http', auth='public', website=True, csrf=False)
    def donation_payment_confirm(self, **post):
        donation_data = request.session.get('donation_data', {})
        donation_data['payment'] = post.get('payment')

        # Get donor_id from session-stored partner
        partner_id = donation_data.get('partner_id')

        if not partner_id:
            return request.redirect('/donate')  # fallback if something went wrong

        # Save the donation record
        request.env['donation.sale'].sudo().create({
            'donor_id': int(partner_id),
            'donation_amount': float(donation_data['other_amount']) if donation_data['amount'] == 'other' else float(
                donation_data['amount']),
            'frequency': donation_data['frequency'],
            'payment_method': donation_data['payment'],
        })

        # Clear session after saving
        request.session.pop('donation_data', None)

        return request.redirect('/thank-you')

    @http.route('/thank-you', type='http', auth='public', website=True)
    def thank_you(self):
        return "<h2>Thank you for signing up!</h2>"