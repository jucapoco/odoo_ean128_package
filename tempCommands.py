#Comandos necesarios para tarea automatica
linea = self.env['ean.structure.lin'].search([])
linea.segment_name
linea.segment_end
self.env['ean.structure.lin'].search_read([], ['segment_name'])
self.env['stock.quant.package'].search_read([], [])
paquetesPendientes = self.env['stock.quant.package'].search_read([('ean_checked', '=', False)], [])

#Para recorrer el recordset
packages = self.env['stock.quant.package'].search([('ean_checked', '=', False)])
for pack in packages:
    print pack.create_date


#Buscar los paquetes que no se hayan analizado y tengan ean128
packages = self.env['stock.quant.package'].search(['&', ('ean_checked', '=', False), ('ean128', '!=', False)])


#ciclo para actualizar los paquetes
for pack in packages:
    pack.write({'ean_checked': True})



# segment_name = fields.Char('Segment Name', size=30, required=True)
