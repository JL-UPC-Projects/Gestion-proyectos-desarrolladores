"""Cliente: entidad externa que contrata proyectos."""
from servicios.validaciones import texto


class Cliente:
    """Datos básicos del cliente: código, razón social y contacto."""

    def __init__(self, codigo, razon_social, contacto):
        self.codigo = texto(codigo)
        self.razon_social = texto(razon_social)
        self.contacto = texto(contacto)

    def validar_datos(self):
        """Mantener contrato: útil para la UI o el gestor de datos."""
        return all(str(v).strip() for v in (self.codigo, self.razon_social, self.contacto))

    def mostrar_resumen(self):
        return f'{self.codigo} | {self.razon_social} | {self.contacto}'