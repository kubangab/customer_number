# Odoo Customer Number Module

## Overview

The Customer Number module is an extension for Odoo that adds a customer number field to partner records. This module allows businesses to assign unique customer numbers to their clients, making it easier to track and identify customers in various business processes.

## Features

- Adds a "Customer Number" field to company partner records
- Displays the customer number on invoice reports
- Supports multi-language functionality
- Only visible and editable for company contacts, not individuals

## Installation

1. Clone this repository into your Odoo addons directory:# customer_number
   git@github.com:kubangab/customer_number.git
2. Update your Odoo addons path to include this module
3. Restart your Odoo server
4. Go to Apps in your Odoo instance and search for "Customer Number"
5. Install the module

## Usage

After installation:

1. Go to Contacts
2. Open or create a company contact
3. You will see a new "Customer Number" field where you can enter the customer's unique number
4. This number will automatically appear on invoices generated for this customer

## Translation

This module supports multi-language functionality. To add a new language:

1. Copy the `i18n/customer_number.pot` file
2. Rename it to `[language_code].po` (e.g., `fr.po` for French)
3. Translate the strings in the new .po file
4. Place the file in the `i18n` directory
5. Restart your Odoo server and update the module

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your-username/customer_number/issues).

## License

This project is licensed under the LGPL-3 License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

## Author

[Lasse Larsson, Kubang AB, https://www.kubang.eu/]
