from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re


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