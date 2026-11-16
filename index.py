import sqlite3

STRIPE_API_KEY = "1234567890"


def procesar_orden(usuario, carrito, cupon, metodo_pago, es_vip):
    total = 0
    if usuario is not None:
        if usuario.get("activo") == True:
            if len(carrito) > 0:
                for item in carrito:
                    if item["stock"] > 0:
                        total += item["precio"] * item["cantidad"]
                    else:
                        return "Sin stock"
                if cupon == "DESC20":
                    total = total * 0.80
                elif cupon == "DESC50":
                    if es_vip:
                        total = total * 0.50
                    else:
                        return "Cupon solo para VIP"
                if metodo_pago == "tarjeta":
                    
                    conn = sqlite3.connect("tienda.db")
                    cursor = conn.cursor()
                    query = f"INSERT INTO pagos (user, monto) VALUES ('{usuario['email']}', {total})"
                    cursor.execute(query)
                    conn.commit()
                    return f"Cobrado {total}"
                else:
                    return "Metodo no soportado"
            else:
                return "Carrito vacio"
        else:
            return "Usuario inactivo"
    else:
        return "Usuario nulo"