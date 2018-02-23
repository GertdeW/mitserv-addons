import logging
import io
from datetime import date, datetime
from odoo.exceptions import Warning
from odoo import models, fields, exceptions, api, _

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

class MitservImport(models.TransientModel):
    _name = "mitserv.import.wizard"
    _description = "Import sale orders for mitserv"

    file = fields.Binary('File')
    import_option = fields.Selection([('update', 'Update SO'), ('create', 'Create SO')], string='Select', default='create')

    @api.multi
    def make_sale(self, values):
        for code in values:
            sale_obj = self.env['sale.order']
            analytic_account_obj = self.env['account.analytic.account']
            analytic_account_search = analytic_account_obj.search([('code', '=', code)])

            if not analytic_account_search:
                raise Warning(_('Analytic account "%s" is missing!') % code)
            else:
                sale_search = sale_obj.search([('analytic_account_id', '=', analytic_account_search.id),('creation_month','=',str(values[code].get('Maand'))),('creation_year','=',str(values[code].get('Jaar'))),('state','=','draft')])
                if sale_search and self.import_option == 'update':
                    sale_id = sale_search[0]
                else:
                    user_id = self.find_user("Administrator")
                    order_date = self.make_order_date(
                        str(values[code].get('Jaar')) + "-" + str(values[code].get('Maand')) + "-01")
                    sale_id = sale_obj.create({
                        'partner_id': analytic_account_search.partner_id.id,
                        'user_id': user_id.id,
                        'date_order': order_date,
                        'analytic_account_id': analytic_account_search.id
                    })
                self.make_order_line(values[code], sale_id)
        return True

    @api.multi
    def make_order_line(self, values, sale_id):
        for product in values:
            if product not in ['Omschrijving', 'Jaar', 'Projectcode', 'Maand']:
                product_obj = self.env['product.product']
                order_line_obj = self.env['sale.order.line']
                product_search = product_obj.search([('default_code', '=', str(product))])
                product_uom = self.env['product.uom'].search([('name', '=', "Unit(s)")])

                if product_search:
                    product_id = product_search
                else:
                    product_id = product_obj.search([('name', '=', str(product))])
                    if product_id and int(values[product]) > 0:
                        res = order_line_obj.create({
                            'product_id': product_id.id,
                            'product_uom_qty': values[product],
                            'price_unit': product_id.list_price,
                            'name': str(product),
                            'product_uom': product_uom.id,
                            'order_id': sale_id.id
                        })
        return True

    @api.multi
    def make_order_date(self, date):
        DATETIME_FORMAT = "%Y-%m-%d"
        i_date = datetime.strptime(date, DATETIME_FORMAT)
        return i_date

    @api.multi
    def find_user(self, name):
        user_obj = self.env['res.users']
        user_search = user_obj.search([('name', '=', name)])
        if user_search:
            return user_search
        else:
            raise Warning(_(' "%s" User is not available.') % name)

    @api.multi
    def find_partner(self, name):
        partner_obj = self.env['res.partner']
        partner_search = partner_obj.search([('name', '=', name)])
        if partner_search:
            return partner_search
        else:
            partner_id = partner_obj.create({
                'name': name})
            return partner_id

    @api.multi
    def import_sale(self):

        """Load Inventory data from the CSV file."""
        keys = []
        data = base64.b64decode(self.file)
        file_input = io.StringIO(data.decode("utf-8"))
        file_input.seek(0)
        reader_info = []
        reader = csv.reader(file_input, delimiter=',')

        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))
        values = {}
        order_values = {}

        for i in range(len(reader_info)):
            field = map(str, reader_info[i])
            if i == 0:
                keys = reader_info[i]
            else:
                values = dict(zip(keys, field))
                if values:
                    values.update({'option': self.import_option})
                    if values.get('Projectcode'):
                        if values.get('Projectcode') not in order_values:
                            order_values[values.get('Projectcode')] = {}
                        for i in keys:
                            if i not in order_values[values.get('Projectcode')]:
                                order_values[values.get('Projectcode')][i] = values.get(i)
                            else:
                                if values.get(i).isdigit() and i != 'Jaar' and i != 'Maand':
                                    order_values[values.get('Projectcode')][i] = int(
                                        order_values[values.get('Projectcode')][i]) + int(values.get(i))

        res = self.make_sale(order_values)

        return res