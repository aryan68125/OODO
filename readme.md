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
