from odoo import models, fields, exceptions, api, _
from datetime import date, datetime

class sale_order(models.Model):
    _inherit = 'sale.order'

    creation_month = fields.Char('Creation Month',compute="_compute_yearmonth",store=True)
    creation_year = fields.Char('Creation Year',compute="_compute_yearmonth",store=True)

    @api.depends('date_order')
    def _compute_yearmonth(self):
        for line in self:
            date = datetime.strptime(line.date_order, "%Y-%m-%d %H:%M:%S")
            line.creation_month = date.month
            line.creation_year = date.year