import math

# Máximo de hojas para un solo anillado
MAX_HOJAS_ANILLADO_SIMPLE = 500


def _get_precio_impresion_unitario(tipo_color, tipo_faz, cantidad):
    """Obtiene el precio unitario de impresión según la tarifa por rangos."""
    if tipo_color == "bn":
        if tipo_faz == "simple":
            if 1 <= cantidad <= 10:
                return 115
            elif 11 <= cantidad <= 20:
                return 65
            elif cantidad >= 21:
                return 45
        else:  # doble
            if 1 <= cantidad <= 10:
                return 105
            elif 11 <= cantidad <= 20:
                return 55
            elif cantidad >= 21:
                return 30
    else:  # color
        if tipo_faz == "simple":
            if 1 <= cantidad <= 10:
                return 160
            elif 11 <= cantidad <= 20:
                return 145
            elif 21 <= cantidad <= 35:
                return 130
            elif 36 <= cantidad <= 50:
                return 115
            elif 51 <= cantidad <= 65:
                return 105
            elif 66 <= cantidad <= 80:
                return 95
            elif cantidad >= 81:
                return 85
        else:  # doble
            if 1 <= cantidad <= 10:
                return 155
            elif 11 <= cantidad <= 20:
                return 140
            elif 21 <= cantidad <= 35:
                return 125
            elif 36 <= cantidad <= 50:
                return 110
            elif 51 <= cantidad <= 65:
                return 95
            elif 66 <= cantidad <= 80:
                return 85
            elif cantidad >= 81:
                return 75
    return 0  # Fallback


def _get_precio_anillado(hojas):
    """Obtiene el precio de anillado según la tarifa por rangos."""
    if 1 <= hojas <= 100:
        return 1200
    elif 101 <= hojas <= 175:
        return 1500
    elif 176 <= hojas <= 220:
        return 2150
    elif 221 <= hojas <= 280:
        return 3000
    elif 281 <= hojas <= 300:
        return 3200
    elif 301 <= hojas <= 350:
        return 3500
    elif 351 <= hojas <= 400:
        return 4000
    elif 401 <= hojas <= 450:
        return 4500
    elif 451 <= hojas <= 500:
        return 4800
    return None  # Fuera de rango para anillado simple


def calcular_trabajo(paginas, tipo_color, tipo_faz, lleva_anillado):
    """
    Calcula el costo de un trabajo de impresión.
    """
    # Calcula hojas físicas (redondeo hacia arriba para impares en doble faz)
    if tipo_faz == "doble":
        hojas = math.ceil(paginas / 2)
    else:
        hojas = paginas

    # Calcula el precio de la impresión
    precio_unitario = _get_precio_impresion_unitario(tipo_color, tipo_faz, paginas)
    precio_impresion = paginas * precio_unitario
    # Gestiona el anillado
    precio_anillado = 0
    fuera_de_rango = False
    opciones_division = {}
    total = precio_impresion

    if lleva_anillado:
        if hojas > MAX_HOJAS_ANILLADO_SIMPLE:
            fuera_de_rango = True
            # Comprueba en cuántos tomos se puede dividir
            for tomos in range(2, 7):
                if (hojas / tomos) <= MAX_HOJAS_ANILLADO_SIMPLE:
                    opciones_division[tomos] = True
                else:
                    opciones_division[tomos] = False
        else:
            # Costo de anillado normal
            precio_anillado = _get_precio_anillado(hojas) or 0
            total += precio_anillado

    return {
        "hojas": hojas,
        "precio_impresion": precio_impresion,
        "precio_anillado": precio_anillado,
        "total": total,
        "fuera_de_rango": fuera_de_rango,
        "opciones_division": opciones_division
    }


def calcular_anillado_dividido(hojas_totales, tomos):
    """
    Calcula el costo para un anillado dividido en varios tomos.
    """
    if tomos <= 1:
        return None

    hojas_por_tomo = math.ceil(hojas_totales / tomos)

    precio_anillado_tomo = _get_precio_anillado(hojas_por_tomo)

    if precio_anillado_tomo is None:
        return None  # No se puede anillar un tomo con esa cantidad de hojas

    total_anillado = precio_anillado_tomo * tomos

    return {
        "hojas_por_tomo": f"Aproximadamente {hojas_por_tomo} por tomo",
        "total_anillado": total_anillado
    }