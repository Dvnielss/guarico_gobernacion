import os

def update_env_odoo_conn(ODOO_HOST: str,ODOO_PORT: int,ODOO_PROTOCOL: str,ODOO_DB: str,ODOO_USER: str,ODOO_PASS: str) -> bool:
    env_file_path = ".env"

    required_vars = {
        "ODOO_HOST": repr(ODOO_HOST),
        "ODOO_PORT": ODOO_PORT,
        "ODOO_PROTOCOL": repr(ODOO_PROTOCOL),
        "ODOO_DB": repr(ODOO_DB),
        "ODOO_USER": repr(ODOO_USER),
        "ODOO_PASS": repr(ODOO_PASS),
    }

    # Si el archivo .env no existe, crea uno nuevo y escribe las variables de entorno
    if not os.path.isfile(env_file_path):
        with open(env_file_path, "w") as env_file:
            for key, value in required_vars.items():
                env_file.write(f"{key}={value}\n")

    else:
        with open(env_file_path, "r") as env_file:
            lines = env_file.readlines()

        with open(env_file_path, "w") as env_file:
            # Actualiza las variables de entorno existentes
            for line in lines:
                env_var = line.strip().split("=")
                if env_var[0] in required_vars:
                    env_file.write(f"{env_var[0]}={required_vars[env_var[0]]}\n")
                    del required_vars[env_var[0]]
                else:
                    env_file.write(line)

            # si esta en blanco o no tiene  variables las agrega
            for key, value in required_vars.items():
                env_file.write(f"{key}={value}\n")

    return True