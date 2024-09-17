import odoorpc

from typing import List, Optional

from app.schemas.V1.config_scheme import settings_env




def odoo_conn() -> Optional[odoorpc.ODOO]:
    try:

        odoo = odoorpc.ODOO(
            settings_env.ODOO_HOST, port=settings_env.ODOO_PORT, protocol=settings_env.ODOO_PROTOCOL
        )

        odoo.login(settings_env.ODOO_DB, settings_env.ODOO_USER, settings_env.ODOO_PASS)

        return odoo
    except odoorpc.error.RPCError as e:
        print("Error al conectar:", e)

    return None


def get_data(
    str_model: str, columns: List[str], odoo: odoorpc.ODOO, date: Optional[str] = None
) -> List[dict]:
    """Obteniedo data

    Args:
        str_model (str): modelo de la app ODOO
        columns (list): atributos requeridos
        odoo (odoorpc): conexion
        date (str, optional): fecha apartir de

    Returns:
        list: lista de datos
    """

    Model = odoo.env[str_model]

    domain = [("write_date", ">", date)] if date else []

    ids = Model.search(domain)
    data = odoo.execute(str_model, "read", ids, columns)

    return data
