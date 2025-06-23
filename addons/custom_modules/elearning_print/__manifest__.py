{
    "name":"Elearning Printout Course",
    "depends": ["base", "survey", "web"],
    "data":[
        "report/survey_template_direct.xml"
    ],
    'assets': {
        'web.report_assets_common': [  # ✅ use correct bundle name
            ('remove', 'survey/static/src/scss/survey_reports.scss'),
            'elearning_print/static/src/scss/survey_reports.scss',
        ],
    },
}
