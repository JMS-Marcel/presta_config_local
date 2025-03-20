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
