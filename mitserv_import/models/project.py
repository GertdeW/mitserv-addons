# -*- coding: utf-8 -*

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    billable = fields.Boolean(
        string='Billable'
    )

