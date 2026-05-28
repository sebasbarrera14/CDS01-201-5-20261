import logging

logger = logging.getLogger(__name__)


def enviar_notificacion(correo: str, asunto: str, mensaje: str) -> bool:
    """
    RF-022: Simula el envío de una notificación por correo al cliente.
    En producción se integraría con un servicio de correo (SendGrid, SES, etc).
    """
    logger.info("📧 Correo enviado a %s | Asunto: %s | Mensaje: %s", correo, asunto, mensaje)
    print(f"📧 Notificación → {correo} | {asunto}: {mensaje}")
    return True


def notificar_cambio_estado(correo: str, nombre: str, id_pedido: int, nuevo_estado: str) -> bool:
    """RF-021 / RF-022: Notifica al cliente sobre un cambio de estado en su pedido."""
    estados_legibles = {
        "pendiente":      "Pendiente de pago",
        "pagado":         "Pago confirmado",
        "en_preparacion": "En preparación",
        "enviado":        "Enviado",
        "entregado":      "Entregado",
        "cancelado":      "Cancelado"
    }
    estado_texto = estados_legibles.get(nuevo_estado, nuevo_estado)
    asunto  = f"Actualización de tu pedido #{id_pedido}"
    mensaje = (f"Hola {nombre}, tu pedido #{id_pedido} "
               f"ahora está en estado: {estado_texto}.")
    return enviar_notificacion(correo, asunto, mensaje)


def notificar_pago_aprobado(correo: str, nombre: str, id_pedido: int,
                             referencia: str, total: float) -> bool:
    """RF-013: Envía el comprobante de pago al cliente."""
    asunto  = f"Comprobante de pago — Pedido #{id_pedido}"
    mensaje = (f"Hola {nombre}, tu pago de ${total:,.0f} COP "
               f"para el pedido #{id_pedido} fue aprobado. "
               f"Referencia: {referencia}.")
    return enviar_notificacion(correo, asunto, mensaje)


def notificar_pago_rechazado(correo: str, nombre: str, id_pedido: int) -> bool:
    """RF-012: Notifica al cliente que su pago fue rechazado."""
    asunto  = f"Pago rechazado — Pedido #{id_pedido}"
    mensaje = (f"Hola {nombre}, tu pago para el pedido #{id_pedido} "
               f"fue rechazado. Por favor intenta nuevamente.")
    return enviar_notificacion(correo, asunto, mensaje)
  
