
from odoo import models, api, fields

class HelpdeskSupport(models.Model):
    _inherit = 'helpdesk.support'

    @api.model
    def create(self, vals):
        record = super(HelpdeskSupport, self).create(vals)

        if not vals.get('partner_id', False) and vals.get('email', ''):
            partner = self.env['res.partner'].sudo().search([('email', '=', vals['email'])], limit=1)
        if vals.get('partner_id', False):
            partner = self.env['res.partner'].sudo().browse(vals.get('partner_id', False))

        if self._context.get('from_fetchmail'):
            email_context = self.env.context.copy()
            email_context.update({
                'email_to': vals["email"],
                'ticket': record["name"],
                'subject': vals["subject"],
                'sender_name': self._context.get('sender_name'),
                'lang': 'nl_NL'
            })

            if partner:
                email_context.update({
                    'lang': partner.lang
                })

            template = self.env.ref('mitserv_import.email_template_helpdesk_confirmation')
            self.env['mail.template'].browse(template.id).with_context(email_context).send_mail(self.id)

        return record