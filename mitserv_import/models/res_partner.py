
import logging
import threading

from odoo.tools.misc import split_every

from odoo import _, api, fields, models, registry, SUPERUSER_ID
from odoo.osv import expression

_logger = logging.getLogger(__name__)



class Partner(models.Model):
    """ Update partner to add a field about notification preferences. Add a generic opt-out field that can be used
       to restrict usage of automatic email templates. """
    _name = "res.partner"
    _inherit = ['res.partner', 'mail.thread', 'mail.activity.mixin']
    _mail_flat_thread = False

    @api.model
    def _notify_send(self, body, subject, recipients, **mail_values):
        emails = self.env['mail.mail']
        recipients_nbr = len(recipients)
        for email_chunk in split_every(50, recipients.ids):
            # TDE FIXME: missing message parameter. So we will find mail_message_id
            # in the mail_values and browse it. It should already be in the
            # cache so should not impact performances.
            mail_message_id = mail_values.get('mail_message_id')
            message = self.env['mail.message'].browse(mail_message_id) if mail_message_id else None
            if message and message.model and message.res_id and message.model in self.env and hasattr(
                    self.env[message.model], 'message_get_recipient_values'):
                tig = self.env[message.model].browse(message.res_id)
                recipient_values = tig.message_get_recipient_values(notif_message=message, recipient_ids=email_chunk)
            else:
                recipient_values = self.env['mail.thread'].message_get_recipient_values(notif_message=None,
                                                                                        recipient_ids=email_chunk)
            if message.model == "helpdesk.support":
                history_messages = self.env['mail.message'].search([("res_id","=",message.res_id),("message_type","in",('email','comment'))])
                if history_messages:
                    history_body = ""
                    message_nr = 1
                    for message in history_messages:
                        if message_nr == 2:
                            history_body += "<br><br>From: " + str(message.email_from) + '<br><br><div style="padding-left:50px;width:100%">' + str(message.body) + "</div>"
                        message_nr = message_nr + 1
                body += "<div>" + history_body + "</div>"

            create_values = {
                'body_html': body,
                'subject': subject,
            }
            create_values.update(mail_values)
            create_values.update(recipient_values)

            emails |= self.env['mail.mail'].create(create_values)
        return emails, recipients_nbr