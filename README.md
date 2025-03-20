# PrestaShop Local Environment Setup Script

A Python automation tool to simplify local PrestaShop instance configuration for development/migration.

## 📥 Features
- **Database Import**: Restore SQL dumps with automatic database creation
- **File Configuration**: Auto-update `.htaccess` and `parameters.php`
- **URL Management**: Update shop domains in database tables
- **Cache Cleanup**: Clear PrestaShop cache directories
- **Cross-Platform**: Works on Windows, Linux, and macOS

## ⚙️ Requirements
- Python 3.6+
- MySQL/MariaDB server
- Command-line access
- Existing PrestaShop installation (1.6+ recommended)

### Python Dependencies
```bash
pip install mysql-connector-python

## Quick Start
1. Clone repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run script:
   ```bash
   python prestashop_setup.py
   ```

## Interactive Setup
The script will prompt for these parameters:
```
PrestaShop directory path (e.g., C:/xampp/htdocs/myshop): 
Local database name (e.g., presta_dev): 
MySQL username (e.g., root): 
MySQL password (leave empty if none): 
Local domain (e.g., localhost/myshop): 
Table prefix (e.g., ps_): 
SQL dump path (e.g., C:/backup.sql): 
```

## Technical Overview
### Script Workflow
1. **Database Import**  
   - Creates database if missing
   - Imports provided SQL dump

2. **File Configuration**  
   - Updates `.htaccess` RewriteBase
   - Modifies `app/config/parameters.php` DB credentials

3. **Database Updates**  
   - Updates `ps_shop_url` domain entries
   - Modifies `ps_configuration` shop URLs

4. **Cache Cleanup**  
   - Clears Smarty cache
   - Removes compiled templates

## Important Notes
- **Backup First**: Always backup existing data before running
- **Path Formats**:
  - Windows: `C:/path/to/folder` (forward slashes)
  - Linux/macOS: `/var/www/path`
- **MySQL Credentials**: Default XAMPP/WAMP users often have empty passwords
- **Permissions**: Ensure write access to PrestaShop directory

## Troubleshooting
### Common Issues
1. **MySQL Connection Errors**:
   - Verify MySQL service is running
   - Check user privileges:
     ```sql
     GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
     FLUSH PRIVILEGES;
     ```

2. **File Not Found Errors**:
   - Confirm PrestaShop path contains:
     - `.htaccess` file
     - `app/config/parameters.php`
     - Valid cache directory structure

3. **URL Mismatch Issues**:
   - Ensure `local_domain` matches your server configuration
   - Verify virtual host settings if using Apache/NGINX

## Customization
Modify these script sections for advanced use:
- **Regex Patterns**: Adjust in `configure_htaccess()` and `configure_parameters_php()`
- **Cache Directories**: Edit `cache_dirs` list in `clear_cache()`
- **Database Queries**: Customize SQL in `update_database_tables()`

## Contributing
1. Fork the repository
2. Create feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:
   ```bash
   git commit -m "Add awesome feature"
   ```
4. Push to branch:
   ```bash
   git push origin feature/your-feature
   ```
