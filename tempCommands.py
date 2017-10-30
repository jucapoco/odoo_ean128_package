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
    tmp_partner_id = resultQuery[0].partner_id
    tmp_product_id = resultQuery[0].product_id
    tmp_lot_id = resultQuery[0].lot_id
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

#Hasta acá
#cr.dictfetchall()

#Código anterior


def ean_process(self):
        packages = self.env['stock.quant.package'].search(['&', ('ean_checked', '=', False), ('ean128', '!=', False)])
        for pack in packages:
            pack.write({'ean_checked': True})
        return True
