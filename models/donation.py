from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Donation(models.Model):
    _name = 'donation.donation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Donation'

    name = fields.Char(string="Donation Reference", required=True, copy=False, readonly=True, default=lambda self: ('New'))
    donor_id = fields.Many2one('donation.donor', string="Donor", required=True, tracking=True)
    campaign_id = fields.Many2one('donation.campaign', string="Campaign", tracking=True)
    amount = fields.Float(string="Amount", required=True)
    donation_type = fields.Selection([
        ('one_time', 'One-Time'),
        ('recurring', 'Recurring'),
        ('pledge', 'Pledge')
    ], default='one_time', string="Donation Type", required=True)
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    notes = fields.Text(string="Notes")
    # payment_status = fields.Selection([
    #     ('pending', 'Pending'),
    #     ('done', 'Done'),
    #     ('failed', 'Failed')
    # ], default='pending', string="Payment Status")
    # payment_method = fields.Selection([
    #     ('cash', 'Cash'),
    #     ('card', 'Card'),
    #     ('upi', 'UPI'),
    #     ('bank', 'Bank Transfer')
    # ], string="Payment Method")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('donation.donation') or 'New'
        return super(Donation, self).create(vals)

    @api.constrains('amount')
    def _check_amount_positive(self):
        for record in self:
            if record.amount <= 0:
                raise ValidationError("Donation amount must be greater than zero.")
