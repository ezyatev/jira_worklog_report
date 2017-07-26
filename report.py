#!/usr/bin/env python3
import argparse

import pandas as pd
from jira import JIRA

import settings

LABELS = settings.LABELS  # shortcut


def set_pd_options():
    """
    Configure display output.
    """
    pd.options.display.float_format = '{:.2f}'.format


def load_issues(date1, date2):
    """
    Retrieve JIRA issues between two dates
    with fields to group and worklog.
    """
    jira = JIRA(settings.SERVER, basic_auth=settings.BASIC_AUTH)
    jql = '{base_jql} AND worklogDate >= {date1} AND worklogDate <= {date2}'.format(
        base_jql=settings.BASE_JQL,
        date1=date1,
        date2=date2
    )
    issues = jira.search_issues(
        jql, fields='{},{},worklog'.format(*settings.JIRA_FIELDS),
        maxResults=settings.MAX_RESULTS)
    return issues


def get_records(date1, date2):
    """
    Create record list to convert to dataframe.
    """
    records = []
    for issue in load_issues(date1, date2):
        fields = issue.raw['fields']
        custom_fields = [fields[k]['value'] for k in settings.JIRA_FIELDS]
        timespent_seconds = [x['timeSpentSeconds'] for x in fields['worklog']['worklogs']]
        timespent_hours = sum(timespent_seconds) / 3600
        records.append([issue.key, *custom_fields, timespent_hours])
    return records


def create_dataframe(date1, date2):
    """
    Create DataFrame from JIRA issues records.
    """
    records = get_records(date1, date2)
    columns = [LABELS['key'], *settings.JIRA_FIELDS.values(), LABELS['hours']]
    df = pd.DataFrame.from_records(
        records,
        columns=columns,
        index=[LABELS['key']]
    )
    return df


def add_totals(monthly_amount, grouped, df):
    """
    Add hours and money totals rows
    to the end of the dataframe.
    """
    hours_sum = df[LABELS['hours']].sum()
    cost_perhour = monthly_amount / hours_sum
    grouped.ix[LABELS['totals'], LABELS['hours']] = hours_sum
    grouped[LABELS['money']] = grouped[LABELS['hours']] * cost_perhour
    return grouped


def get_report(date1, date2, monthly_amount, groupby):
    """
    Return datafame with grouped series
    that could be rendered as final report.
    """
    df = create_dataframe(date1, date2)
    grouped = df.groupby(groupby, sort=False).sum()
    grouped.sort_values(LABELS['hours'], ascending=False, inplace=True)
    grouped = add_totals(monthly_amount, grouped, df)
    return grouped


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a consolidated expense report with grouping by JIRA custom fields.'
    )
    parser.add_argument("date1", help="Start date, use the format YYYY-MM-DD.")
    parser.add_argument("date2", help="End date, use the format YYYY-MM-DD.")
    parser.add_argument("monthly_amount", type=float, help="The salary payments sum of your employees.")
    parser.add_argument("groupby", help="JIRA field label to group by. Must be defined in JIRA_FIELDS mapping.")
    args = parser.parse_args()

    set_pd_options()

    report = get_report(
        date1=args.date1,
        date2=args.date2,
        monthly_amount=args.monthly_amount,
        groupby=args.groupby
    )
    print(report)
