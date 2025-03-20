import csv
import json
import xmlrpc.client

# Configuración
url = "https://odoo-dev.inplast.es/"
db = "DEV"
# Solicitar credenciales al usuario
username = "usuario"
password = "contraseña"

output_csv = "sale_order_lines_filtered.csv"
output_json = "sale_order_lines_filtered.json"
datetime_filter = '2025-01-15 00:00:00'

# Autenticación
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    print("Error de autenticación. Verifica tus credenciales.")
    exit()

# Conexión al modelo de Odoo
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

try:
    # Filtrar órdenes de venta por estado 'sale' y fecha 'date_order'
    domain = [('state', '=', 'sale'), ('date_order', '>=', datetime_filter)]
    sale_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [domain],
                                    {'fields': ['id', 'name', 'partner_id', 'date_order', 'state', 'tag_ids']})

    # Obtener IDs de las órdenes de venta filtradas
    sale_order_ids = [order['id'] for order in sale_orders]

    if not sale_order_ids:
        print("No se encontraron órdenes de venta para el filtro especificado.")
        exit()

    # Obtener las líneas de pedido de las órdenes filtradas
    sale_order_line_ids = models.execute_kw(db, uid, password, 'sale.order.line', 'search',
                                            [[('order_id', 'in', sale_order_ids)]])
    sale_order_lines = models.execute_kw(db, uid, password, 'sale.order.line', 'read', [sale_order_line_ids],
                                         {'fields': ['order_id', 'product_id', 'product_uom_qty', 'price_unit',
                                                     'price_subtotal', 'old_default_code', 'commitment_date',
                                                     'customer_arrival_date']})

    # Obtener IDs de productos y socios (partner_id)
    product_ids = list(set(line['product_id'][0] for line in sale_order_lines if line.get('product_id')))
    partner_ids = list(set(order['partner_id'][0] for order in sale_orders if order.get('partner_id')))

    # Recopilar todos los tag_ids únicos
    all_tag_ids = []
    for order in sale_orders:
        if order.get('tag_ids'):
            all_tag_ids.extend(order['tag_ids'])
    all_tag_ids = list(set(all_tag_ids))

    # Consultar productos, socios y tags
    products = models.execute_kw(db, uid, password, 'product.product', 'read', [product_ids],
                                 {'fields': ['id', 'name', 'default_code']})
    partners = models.execute_kw(db, uid, password, 'res.partner', 'read', [partner_ids], {'fields': ['id', 'ref']})

    # Obtener información de los tags
    tags = []
    if all_tag_ids:
        tags = models.execute_kw(db, uid, password, 'crm.tag', 'read', [all_tag_ids], {'fields': ['id', 'name']})

    # Diccionarios para acceso rápido
    product_dict = {product['id']: product for product in products}
    partner_dict = {partner['id']: partner for partner in partners}
    order_dict = {order['id']: order for order in sale_orders}
    tag_dict = {tag['id']: tag for tag in tags}

except Exception as e:
    print(f"Error al obtener los datos: {e}")
    exit()

# Escribir en un archivo CSV
try:
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribir encabezados
        writer.writerow(['Order Name', 'Customer', 'Customer Reference', 'Product', 'Product Code', 'Product old Code',
                         'Quantity', 'Unit Price', 'Subtotal', 'Commitment Date', 'Customer Arrival Date',
                         'Order Date', 'Tags'])

        # Escribir datos
        for line in sale_order_lines:
            order = order_dict.get(line['order_id'][0]) if line.get('order_id') else {}
            product = product_dict.get(line['product_id'][0]) if line.get('product_id') else {}
            partner = partner_dict.get(order.get('partner_id')[0]) if order.get('partner_id') else {}

            # Obtener nombres de tags
            tag_names = []
            if order.get('tag_ids'):
                tag_names = [tag_dict.get(tag_id, {}).get('name', '') for tag_id in order['tag_ids']]

            writer.writerow([
                order.get('name', ''),
                order.get('partner_id', [''])[1] if order.get('partner_id') else '',
                partner.get('ref', '') if partner else '',
                product.get('name', ''),
                product.get('default_code', ''),
                line.get('old_default_code', ''),
                line.get('product_uom_qty'),
                line.get('price_unit'),
                line.get('price_subtotal'),
                line.get('commitment_date', ''),
                line.get('customer_arrival_date', ''),
                order.get('date_order', ''),
                ', '.join(tag_names)  # Añadimos los tags como string separado por comas
            ])
    print(f"Exportación completada. Archivo CSV guardado como {output_csv}.")
except Exception as e:
    print(f"Error al escribir el archivo CSV: {e}")

# Escribir en un archivo JSON
try:
    json_data = []
    for line in sale_order_lines:
        order = order_dict.get(line['order_id'][0]) if line.get('order_id') else {}
        product = product_dict.get(line['product_id'][0]) if line.get('product_id') else {}
        partner = partner_dict.get(order.get('partner_id')[0]) if order.get('partner_id') else {}

        # Obtener nombres de tags
        tag_names = []
        if order.get('tag_ids'):
            tag_names = [tag_dict.get(tag_id, {}).get('name', '') for tag_id in order['tag_ids']]

        json_data.append({
            'Order Name': order.get('name', ''),
            'Customer': order.get('partner_id', [''])[1] if order.get('partner_id') else '',
            'Customer Reference': partner.get('ref', '') if partner else '',
            'Product': product.get('name', ''),
            'Product Code': product.get('default_code', ''),
            'Product old Code': line.get('old_default_code', ''),
            'Quantity': line.get('product_uom_qty'),
            'Unit Price': line.get('price_unit'),
            'Subtotal': line.get('price_subtotal'),
            'Commitment Date': line.get('commitment_date', ''),
            'Customer Arrival Date': line.get('customer_arrival_date', ''),
            'Order Date': order.get('date_order', ''),
            'Tags': tag_names  # Añadimos los tags como array
        })

    with open(output_json, mode='w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)
    print(f"Exportación completada. Archivo JSON guardado como {output_json}.")
except Exception as e:
    print(f"Error al escribir el archivo JSON: {e}")