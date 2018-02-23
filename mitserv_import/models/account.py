from odoo import models, fields, api, _, SUPERUSER_ID

class HrTimesheetSheet(models.Model):
    _inherit = 'account.analytic.line'


    @api.multi
    def _default_billable(self):
        print(self.project_id.billable)
        print(self)
        return self.project_id.billable

    billable = fields.Boolean(
        string='Billable',
        default=_default_billable,
    )