# -*- coding: utf-8 -*-

{
    "name": "M0C0 - Contabilidad Financiera y Analítica",
    "version": "0.1.13",
    "author": "MOROPO S.U.R.L.",
    "website": "https://www.moropo.cu",
    "contact": "contacto@moropo.cu",
    "category": "Accounting",
    "depends": ["account", "web_tour"],
    "data": [
        "security/accounting_security.xml",
        "wizard/account_change_lock_date.xml",
        "views/hook_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "uninstall_hook": "uninstall_hook",
}
