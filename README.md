# JIRA Worklog Report

A Python script that creates a consolidated report by JIRA issues worklogs with grouping by custom fields.

## Installation

1. Copy the `settings-example.py` file and save the new file as `settings.py`.
2. Change module level variables. For details, see the comments.
3. Make the script executable:

        chmod a+x report.py


## Usage

    ./report.py [-h] date1 date2 monthly_amount groupby
    
    positional arguments:
      date1           Start date, use the format YYYY-MM-DD.
      date2           End date, use the format YYYY-MM-DD.
      monthly_amount  The salary payments sum of your employees.
      groupby         JIRA field label to group by. Must be defined in JIRA_FIELDS
                      mapping.

Example:

    ./report.py 2017-06-01 2017-06-30 1000000 'Класс'


## Author
Eugene Zyatev ([eu@zyatev.ru](mailto:eu@zyatev.ru))