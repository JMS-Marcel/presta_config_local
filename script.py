import os
import subprocess
import mysql.connector
import re
import shutil

def main():
    # Paramètres personnalisables
    prestashop_path = input("Chemin vers le dossier PrestaShop (ex: C:/xampp/htdocs/mon_site): ")
    db_name = input("Nom de la base de données locale (ex: prestashop_local): ")
    db_user = input("Utilisateur MySQL (ex: root): ")
    db_password = input("Mot de passe MySQL (ex: 'vide' si root sans mot de passe): ")
    local_domain = input("Domaine local (ex: localhost/mon_site): ")
    table_prefix = input("Préfixe des tables (ex: ps_ par défaut): ")
    sql_dump_path = input("Chemin vers le dump SQL (ex: C:/dump.sql): ")

    # 1. Importer la base de données
    print("\n[1/5] Importation de la base de données...")
    import_database(db_name, db_user, db_password, sql_dump_path)

    # 2. Configuration du fichier .htaccess
    print("\n[2/5] Configuration du fichier .htaccess...")
    configure_htaccess(prestashop_path, local_domain)

    # 3. Configuration du fichier parameters.php
    print("\n[3/5] Configuration du fichier parameters.php...")
    configure_parameters_php(prestashop_path, db_name, db_user, db_password)

    # 4. Mettre à jour les tables de la base de données
    print("\n[4/5] Mise à jour des tables ps_shop_url et ps_configuration...")
    update_database_tables(db_name, db_user, db_password, table_prefix, local_domain)

    # 5. Vider le cache
    print("\n[5/5] Vider le cache...")
    clear_cache(prestashop_path)

    print("\nConfiguration terminée ! Accédez à http://localhost/mon_site pour tester.")


def import_database(db_name, db_user, db_password, sql_dump_path):
    try:
        # Créer la base de données si elle n'existe pas
        subprocess.run(
            f"mysql -u{db_user} -p{db_password} -e 'CREATE DATABASE IF NOT EXISTS {db_name}';",
            shell=True,
            check=True
        )
        # Importer le dump
        subprocess.run(
            f"mysql -u{db_user} -p{db_password} {db_name} < {sql_dump_path}",
            shell=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'importation: {e}")
        exit(1)


def configure_htaccess(prestashop_path, local_domain):
    htaccess_path = os.path.join(prestashop_path, ".htaccess")
    with open(htaccess_path, "r") as f:
        content = f.read()
    # Mettre à jour RewriteBase
    new_content = re.sub(
        r"(RewriteBase\s+).*",
        f"RewriteBase /{local_domain.split('/')[-1]}/",
        content
    )
    with open(htaccess_path, "w") as f:
        f.write(new_content)
    print(f"RewriteBase mis à jour pour {local_domain}")


def configure_parameters_php(prestashop_path, db_name, db_user, db_password):
    parameters_path = os.path.join(prestashop_path, "app/config/parameters.php")
    with open(parameters_path, "r") as f:
        content = f.read()
    # Remplacer les paramètres de la base de données
    content = re.sub(
        r"'database_host'\s*=>\s*'.*'",
        f"'database_host' => 'localhost'",
        content
    )
    content = re.sub(
        r"'database_name'\s*=>\s*'.*'",
        f"'database_name' => '{db_name}'",
        content
    )
    content = re.sub(
        r"'database_user'\s*=>\s*'.*'",
        f"'database_user' => '{db_user}'",
        content
    )
    content = re.sub(
        r"'database_password'\s*=>\s*'.*'",
        f"'database_password' => '{db_password}'",
        content
    )
    with open(parameters_path, "w") as f:
        f.write(content)
    print("Fichier parameters.php configuré.")


def update_database_tables(db_name, db_user, db_password, table_prefix, local_domain):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()
        # Mettre à jour ps_shop_url
        cursor.execute(
            f"UPDATE {table_prefix}shop_url SET domain = '{local_domain}', domain_ssl = '{local_domain}'"
        )
        # Mettre à jour ps_configuration
        cursor.execute(
            f"UPDATE {table_prefix}configuration SET value = '{local_domain}' WHERE name IN ('PS_SHOP_DOMAIN', 'PS_SHOP_DOMAIN_SSL')"
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Mises à jour de la base de données effectuées.")
    except mysql.connector.Error as e:
        print(f"Erreur lors de la mise à jour: {e}")
        exit(1)


def clear_cache(prestashop_path):
    cache_dirs = [
        "cache/",
        "cache/smarty/",
        "cache/Smarty/",
        "cache/compiled/"
    ]
    for dir_path in cache_dirs:
        full_path = os.path.join(prestashop_path, dir_path)
        if os.path.exists(full_path):
            for filename in os.listdir(full_path):
                file_path = os.path.join(full_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Erreur lors de la suppression de {file_path}: {e}")
            print(f"Cache {dir_path} vidé.")


if __name__ == "__main__":
    main()