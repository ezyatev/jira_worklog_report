import os

# Basic auth credentias. See environment variables.
BASIC_AUTH = (os.environ['JIRA_USER'], os.environ['JIRA_PASSWORD'])

# JIRA issues query.
BASE_JQL = 'project = WWW'

# JIRA custom fields used to group issues.
#
# To identify the custom field ID:
# 1. Go to Administration/Custom Fields.
# 2. Click on the "Configure" link for the custom field you're interested in
# in the URL of the Configure Custom Field page, note the number after "customFieldId=" and
# append it to "customfield_" to build the custom field ID.
JIRA_FIELDS = {
    'customfield_11102': 'Инициатор',
    'customfield_11106': 'Класс',
}

# JIRA server URL.
SERVER = 'http://jira.example.com:8080'

# Limit issues returned by JIRA API.
MAX_RESULTS = 10000

# Base columns labels.
LABELS = {
    'key': 'Задача',
    'hours': 'Часы',
    'money': 'Деньги',
    'totals': 'Итого',
}
