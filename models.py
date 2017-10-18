# -*- coding: utf-8 -*-

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round, float_compare


# class ean128_package(models.Model):
#     _name = 'ean128_package.ean128_package'

#     name = fields.Char()


class Extend_package(models.Model):
    _inherit = "stock.quant.package"

    ean128 = fields.Char('EAN128', size=130)
    ean_checked = fields.Boolean('EAN Checked', default=False)
    package_weight = fields.Float('Peso en Kg', (8, 2), help="Peso del paquete en Kg")


# class Extend_Transfer_Details(models.Model):
#     _inherit = "stock.transfer_details"

#     ean128 = fields.Char('EAN128', size=130)


# class Extend_Transfer_Details_Items(models.Model):
#     _inherit = "stock.transfer_details_items"

#     ean128 = fields.Char('EAN128', size=130)


# class StockTransferDetailsInherit(models.Model):
#     _inherit = 'stock.transfer_details'
#
#     @api.one
#     def do_detailed_transfer(self, values):
#         res = super(StockTransferDetailsInherit, self).do_detailed_transfer(values)
#         return res


class Ean_Structure(models.Model):
    _name = 'ean.structure'

    BP_id = fields.Many2one('res.partner', 'BP', required=True)
    Item_id = fields.Many2one('product.template', 'Item', required=False)
    child_ids = fields.One2many('ean.structure.lin', 'Ean_Structure_id', 'Child Structure')

    @api.multi
    def afun(self):
        len(self)


class Ean_Stc_Lin(models.Model):
    _name = 'ean.structure.lin'

    Ean_Structure_id = fields.Many2one('ean.structure', string='Parent structure')
    segment_name = fields.Char('Segment Name', size=30, required=True)
    segment_start = fields.Integer('Start', help="Start of de segment in the barcode", required=True)
    segment_end = fields.Integer('End', help="End of the segment in the barcode", required=True)
    segment_map = fields.Char('Mapping Field', size=30, required=False)

    @api.multi
    def afun(self):
        len(self)
