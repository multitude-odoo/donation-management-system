from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re
from datetime import datetime


class Donor(models.Model):
    _name = 'donation.donor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Donor'



    name = fields.Char(string="Donor",required=True)
    email = fields.Char(string="Email",required=True,tracking=True)
    phone = fields.Char(string="Phone",required=True,tracking=True)
    address = fields.Text(string="Address")
    donor_type = fields.Selection([
        ('individual', 'Individual'),
        ('corporate', 'Corporate')
    ], default='individual')
    sequence = fields.Integer(index=True, help="Gives the sequence order when displaying records.", default=1)
    image = fields.Image(string="Image")
    campaign_id = fields.Many2one('donation.campaign', string="Campaign")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid Email Format")

    @api.constrains('phone')
    def _check_phone_format(self):
        for record in self:
            if record.phone and not re.match(r'^[0-9]{10,15}$', record.phone):
                raise ValidationError("Phone number must be 10–15 digits.")

    @api.constrains('email', 'phone')
    def _check_unique_email_phone(self):
        for record in self:
            if record.email:
                existing_email = self.env['donation.donor'].search([
                    ('email', '=', record.email),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_email:
                    raise ValidationError("Email already exists.")
            if record.phone:
                existing_phone = self.env['donation.donor'].search([
                    ('phone', '=', record.phone),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_phone:
                    raise ValidationError("Phone number already exists.")




# models/res_partner.py


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_donor = fields.Boolean(string="Is Donor", default=False)
    donor_type = fields.Selection([
        ('personal', 'Personal'),
        ('corporate', 'Corporate'),
        ('anonymous', 'Anonymous'),
    ], string="Donor Type")

    donor_account_id = fields.Char(string="Donor Account ID")
    identification_type = fields.Selection([
        ('nric', 'NRIC'),
        ('passport', 'Passport'),
        ('fin', 'FIN'),
        ('uen', 'UEN'),
        ('email', 'Email'),
    ], string="Identification Type",required=True)

    identification_number = fields.Char(string="Identification Number")
    contact_number = fields.Char(string="Contact Number")
    designation = fields.Char(string="Designation")
    postal_code = fields.Char(string="Postal Code")
    street_2 = fields.Char(string="Unit No.")
    sex = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ], string="Sex")
    dob = fields.Date(string="Date of Birth")

    def _generate_donor_account_id(self, donor_type):
        year = datetime.now().year
        prefix = {'individual': 'P', 'corporate': 'C', 'anonymous': 'A'}.get(donor_type, 'P')
        sequence = self.env['ir.sequence'].next_by_code('donor.account')
        return f"{prefix}{year}{sequence}"

    @api.model
    def create(self, vals):
        if not vals.get('donor_account_id') and vals.get('donor_type'):
            vals['donor_account_id'] = self._generate_donor_account_id(vals['donor_type'])
        return super(ResPartner, self).create(vals)
