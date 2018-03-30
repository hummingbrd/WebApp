import datetime
import pandas as pd
import xlrd
from xlsxwriter.utility import xl_rowcol_to_cell
from azure.mgmt.monitor import MonitorManagementClient
from azure.common.credentials import ServicePrincipalCredentials


# Get the ARM id of your resource. You might chose to do a "get"
# using the according management or to build the URL directly
# Example for a ARM VM
credentials = ServicePrincipalCredentials(
    client_id='b812b1dd-e25e-492d-8b0d-b828f1048d54',
    secret='PUbNxuHi7ovFWoiGGSWQ/ffBdXI5sbonyV52Mdalnrs=',
    tenant='2cc639d3-af51-4877-9056-5b92bafdf00d'
)

resource_group_name = 'mitiscctest'
app_name = 'mitiscctest'
subscription_id = '312c8cd6-c19b-48f1-9004-ee9e83fd18ef'
resource_id_web = (
    "subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.Web/sites/{}"
).format(subscription_id, resource_group_name, app_name)
resource_id_serverfarms = "/subscriptions/312c8cd6-c19b-48f1-9004-ee9e83fd18ef/resourceGroups/mitiscctest/providers/Microsoft.Web/serverFarms/mititestserviceplan"
resource_id_databases = "/resourceGroups/mitiscctest/providers/Microsoft.Sql/servers/mititestserver/databases/minitestdatabases"
# create client
client = MonitorManagementClient(
    credentials,
    subscription_id
)

# create client
client = MonitorManagementClient(
    credentials,
    subscription_id
)


today = datetime.datetime.now().date()
todays = str(today)+'T00:00:00Z'
yesterday = today - datetime.timedelta(hours=12)
week = str(today - datetime.timedelta(hours=336))+'T00:00:00Z'
timespan = week + '/' + todays
print(timespan)

metrics_AverageCpuPercentage = client.metrics.list(
    resource_id_serverfarms,
    timespan=timespan,
    interval='PT24H',
    metric='CpuPercentage',
    aggregation='Average'
)

metrics_DataIn = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT24H',
    metric='BytesReceived',
    aggregation='Total'
)


def TakeMetricTotal(metric, sheet, num):
    with open('test.txt', 'w') as f:
        for item in metric.value:
            # print("{} ({})".format(item.name.localized_value, item.unit.name), file=f)
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    count = 0
                    print("{}: {}".format(data.time_stamp, data.total), file=f)
                #    if str(data.total) > str(num):
                #        count += 1
                #print(count)
                #print("Total times: {}".format(count), file=f)
    data = pd.read_csv('test.txt', sep=" ", header=None, names=["Date", "Timestamp", sheet])
    df0 = pd.DataFrame(data)
    return df0


df1 = TakeMetricTotal(metrics_AverageCpuPercentage, 'AverageCpuPercentage', 1)
df2 = TakeMetricTotal(metrics_DataIn, 'DataIn', 1)


# dfs_tabs create excel file with multiple sheet with metric accordingly
def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, index=None, startrow=0, startcol=0)
    writer.save()


# list of dataframes and sheet names
dfs = [df1, df2]
sheets = ['AverageCpuPercentage', 'DataIn']

# run function dfs_tabs
dfs_tabs(dfs, sheets, 'pandas_positioning.xlsx')


setup_dict = {'AverageCpuPercentage': df1, 'DataIn': df2}
ws_dict = pd.read_excel('pandas_positioning.xlsx', sheet_name=None)
ws_dict['DataIn'] = pd.concat([ws_dict['DataIn'][['Date', 'Timestamp', 'DataIn']],
                                ws_dict['AverageCpuPercentage'][['AverageCpuPercentage']]],
                                axis=1)

with pd.ExcelWriter('pandas_positioning.xlsx', engine='xlsxwriter') as writer:
    for ws_name, df_sheet in setup_dict.items():
        df_sheet.to_excel(writer, sheet_name=ws_name, index=None)
    ws_dict['DataIn'].to_excel(writer, sheet_name='Sheet3', index=None, startrow=0, startcol=0)
    writer.save()

