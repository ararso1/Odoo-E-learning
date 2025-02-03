{
    "name": "Damiina Theme",
    "author": "Ararso",
    "depends": ["base",  "web", "web_editor","website"],
    "data": [
        "views/brand_promotion.xml",
        "views/webclient_templates.xml",
        "views/damiinaLoginPageView.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "damiinathemes/static/src/js/web_window_title.js",
            "damiinathemes/static/src/js/user_menu_items.js",
        ]
    },
    "installable": True,
    "auto_install": True
}
