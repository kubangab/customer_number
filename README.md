# Odoo Customer Number Module

## Overview
The Customer Number module is an extension for Odoo that adds a customer number field to partner records. This module allows businesses to assign unique customer numbers to their clients, making it easier to track and identify customers in various business processes.

## Features
- Adds a "Customer Number" field to company partner records
- Automatically generates unique customer numbers for new company contacts
- Displays the customer number on invoice reports
- Supports multi-language functionality
- Only visible and editable for company contacts, not individuals
- Configurable number of digits for customer numbers
- Option to use leading zeros for customer numbers
- Bulk update feature for existing customer numbers

## Installation
1. Clone this repository into your Odoo addons directory:
   git clone git@github.com:kubangab/customer_number.git
2. Update your Odoo addons path to include this module
3. Restart your Odoo server
4. Go to Apps in your Odoo instance and search for "Customer Number"
5. Install the module

## Usage
After installation:
1. Go to Settings > General Settings > Customer Numbers to configure:
- Number of digits for customer numbers
- Starting number for customer numbers
- Whether to use leading zeros
2. Go to Contacts
3. Create a new company contact, and a customer number will be automatically assigned
4. The customer number will automatically appear on invoices generated for this customer
5. To update existing customer numbers, go to Contacts, select the list view, and use the "Update Customer Numbers" action from the Action menu

## Translation
This module supports multi-language functionality. To add a new language:
1. Copy the `i18n/customer_number.pot` file
2. Rename it to `[language_code].po` (e.g., `fr.po` for French)
3. Translate the strings in the new .po file
4. Place the file in the `i18n` directory
5. Restart your Odoo server and update the module

## Security
The module includes security settings to ensure only authorized users can access and modify customer numbers. Make sure to assign the appropriate user groups for access to the customer number features.

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/kubangab/customer_number/issues).

## License
This project is licensed under the LGPL-3 License - see the [LICENSE](LICENSE) file for details.

## Support
If you encounter any problems or have any questions, please open an issue on the GitHub repository.

## Author
Lasse Larsson, Kubang AB, https://www.kubang.eu/
