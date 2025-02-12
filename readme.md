# Introduction:
This repository is for odoo project for self learning
## Some important command: 
### Create a configuration file for Odoo: 
- If you want to create a configuration file in odoo then use this command: ```python3 odoo-bin -s -c aditya.conf --addons-path addons,odoo/addons```
- How to override configuration file 
    - You can edit commands directly from the config file and you can also add a new command at the end of the config file.
    - Your default config file for odoo reside in this directory ```OODOO_version_18/odoo/debian/odoo.conf```
- Starting oddo using the config file that you created here in this case its called aditya.conf
    - Command to start odoo using this config file is : ```python3 odoo-bin -c aditya.conf```
- This command will start odoo after upgrading all the installed module in an odoo project ```python3 odoo-bin -c aditya.conf -u all```
### Disable database manager or selector options in odoo:
Odoo gives you an option to disable http://localhost:8069/web/database/manager and http://localhost:8069/web/database/selector links because these two links can pose a security threat.

<br>

Use this command to disable database management and database list links : ```python3 odoo-bin -c aditya.conf --no-database-list```

<br>

If you want to use a specific database then you can use this command : ```python3 odoo-bin -r aditya -w ilovemymom -d odoo_test_db```
### Activate develoepr mode in odoo
Activate developer mode in odoo from settings → Go to Settings ‣ General Settings ‣ Developer Tools and click on Activate the developer mode.
