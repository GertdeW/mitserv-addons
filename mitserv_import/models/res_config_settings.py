# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, SUPERUSER_ID

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    template_id = fields.Many2one(
        'mail.template', 'Email template')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            template_id=int(get_param('template_id'))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('template_id', self.template_id.id)