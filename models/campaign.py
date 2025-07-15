from odoo import models, fields,api
from odoo.exceptions import ValidationError

class Campaign(models.Model):
    _name = 'donation.campaign'
    _inherit = ['mail.thread', 'mail.activity.mixin','website.published.mixin']
    _description = 'Campaign'
    _rec_name = 'title'

    title = fields.Char(string='Name',required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    goal_amount = fields.Float(string='Amount')
    active = fields.Boolean(string='Active',default=True)
    sequence = fields.Integer(index=True, help="Gives the sequence order when displaying records.", default=1)
    image = fields.Binary("Image")
    # Relations
    donor_ids = fields.One2many('donation.donor', 'campaign_id', string='Donors')
    volunteer_ids = fields.One2many('donation.volunteer', 'campaign_id', string='Volunteers')

    # Count fields
    donor_count = fields.Integer(string="Donors", compute="_compute_counts", store=True)
    volunteer_count = fields.Integer(string="Volunteers", compute="_compute_counts", store=True)

    @api.depends('donor_ids', 'volunteer_ids')
    def _compute_counts(self):
        for record in self:
            record.donor_count = len(record.donor_ids)
            record.volunteer_count = len(record.volunteer_ids)



    def action_view_donors(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Donors',
            'res_model': 'donation.donor',
            'view_mode': 'list,form',
            'domain': [('campaign_id', '=', self.id)],
            'context': {'default_campaign_id': self.id},
        }

    def action_view_volunteers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Volunteers',
            'res_model': 'donation.volunteer',
            'view_mode': 'list,form',
            'domain': [('campaign_id', '=', self.id)],
            'context': {'default_campaign_id': self.id},
        }


    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError("Start Date must be before End Date.")

    @api.constrains('goal_amount')
    def _check_goal_amount(self):
        for record in self:
            if record.goal_amount <= 0:
                raise ValidationError("Goal amount must be greater than zero.")

    @api.constrains('title', 'start_date', 'end_date')
    def _check_duplicate_campaign(self):
        for record in self:
            domain = [
                ('id', '!=', record.id),
                ('title', '=', record.title)
            ]
            existing = self.search_count(domain)
            if existing:
                raise ValidationError("A name already exists.")