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

    @api.multi
    def ean_process(self):
        cr = self.env.cr
        packid = 0
        tmp_ean128 = ""
        seg_lote_id = 0
        seg_fecha_id = 0
        seg_peso_id = 0
        tmp_partner_id = 0
        tmp_product_id = 0
        tmp_lot_id = 0
        tmp_struct_id = 0
        tmp_peso = 0
        query = """SELECT T3.product_id, T3.partner_id, T0.lot_id FROM public.stock_quant T0
        INNER JOIN
        (SELECT T11.quant_id, T11.move_id FROM public.stock_quant_move_rel T11) T1 ON T0.id=T1.quant_id
        INNER JOIN
        (SELECT T22.id, T22.purchase_line_id FROM public.stock_move T22) T2 ON T1.move_id=T2.id
        INNER JOIN
        (SELECT T33.id, T33.partner_id, T33.product_id FROM public.purchase_order_line T33) T3
        ON T2.purchase_line_id=T3.id
        WHERE T0.package_id = %packid%
        LIMIT 1
        """
        tmpquery = ""

        #Traer los id de cada segmento a trabajar (lote, fecha, peso)
        segments = self.env['ean.segments'].search([('segment', 'in', ['lote', 'fecha', 'peso'])])

        for seg in segments:
            if seg.segment == 'lote':
                seg_lote_id = seg.id
            if seg.segment == 'fecha':
                seg_fecha_id = seg.id
            if seg.segment == 'peso':
                seg_peso_id = seg.id

        #Buscar los paquetes que no se hayan analizado y tengan ean128
        packages = self.env['stock.quant.package'].search(['&', ('ean_checked', '=', False), ('ean128', '!=', False)])
        #ciclo para actualizar los paquetes
        for pack in packages:
            packid = pack.id
            tmp_ean128 = pack.ean128
            tmpquery = query.replace("%packid%", str(packid))
            cr.execute(tmpquery)
            resultQuery = cr.fetchall()
            tmp_product_id = resultQuery[0][0]
            tmp_partner_id = resultQuery[0][1]
            tmp_lot_id = resultQuery[0][2]
            #Consulta para filtrar las estructuras de ean segun proveedor y/o artículo
            structure = self.env['ean.structure'].search(['|', ('BP_id', '=', tmp_partner_id), '&', ('BP_id', '=', tmp_partner_id), ('Item_id', '=', tmp_product_id)])
            tmp_struc_id = structure[0].id
            #traer la informacion de los segmentos
            structure_lin = self.env['ean.structure.lin'].search_read(['&', ('Ean_Structure_id', '=', tmp_struc_id), ('segment_name', '=', seg_lote_id)],     ['segment_start', 'segment_end'])
            seg_lote_start = structure_lin[0]['segment_start']
            seg_lote_end = structure_lin[0]['segment_end']
            structure_lin = self.env['ean.structure.lin'].search_read(['&', ('Ean_Structure_id', '=', tmp_struc_id), ('segment_name', '=', seg_fecha_id)], ['segment_start', 'segment_end'])
            seg_fecha_start = structure_lin[0]['segment_start']
            seg_fecha_end = structure_lin[0]['segment_end']
            structure_lin = self.env['ean.structure.lin'].search_read(['&', ('Ean_Structure_id', '=', tmp_struc_id), ('segment_name', '=', seg_peso_id)], ['segment_start', 'segment_end'])
            seg_peso_start = structure_lin[0]['segment_start']
            seg_peso_end = structure_lin[0]['segment_end']
            tmp_peso = float(tmp_ean128[seg_peso_start:seg_peso_end])
            pack.write({'ean_checked': True})
            pack.write({'package_weight': tmp_peso})
        return True


class Ean_Segments(models.Model):
    _name = 'ean.segments'

    segment = fields.Char('Segment Name', size=30, required=True)

    @api.multi
    def afun(self):
        len(self)

    def name_get(self, cr, uid, ids, context=None):
        res = []
        segments = self.browse(cr, uid, ids, context)
        for segment in segments:
            res.append((segment.id, segment.segment))
        return res

    _sql_constraints = [('field_unique', 'unique(segment)', 'Choose another value - it has to be unique!')]


class Ean_Stc_Lin(models.Model):
    _name = 'ean.structure.lin'

    Ean_Structure_id = fields.Many2one('ean.structure', string='Parent structure')
    segment_name = fields.Many2one('ean.segments', 'segment', required=True)
    segment_start = fields.Integer('Start', help="Start of de segment in the barcode", required=True)
    segment_end = fields.Integer('End', help="End of the segment in the barcode", required=True)
    segment_map = fields.Char('Mapping Field', size=30, required=False)

    @api.multi
    def afun(self):
        len(self)
