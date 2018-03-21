__author__ = 'Hieu Nguyen hieu.nguyen@scc.com'
__copyright__ = 'Copyright (c) 2017-2018 Hieu Nguyen'
__version__ = '1.0.0'

# Version 1.0.0

import datetime
import pandas as pd
from azure.mgmt.monitor import MonitorManagementClient
from azure.common.credentials import ServicePrincipalCredentials


# Get the ARM id of your resource. You might chose to do a "get"
# using the according management or to build the URL directly
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


# Get Data Out for Application by hour
today = datetime.datetime.now().date()
todays = str(today)+'T00:00:00Z'
yesterday = today - datetime.timedelta(hours=12)
week = str(today - datetime.timedelta(hours=336))+'T00:00:00Z'
timespan = week + '/' + todays
print(timespan)


# Define function to take metric average and total
def takemetrictotal(metric, sheet):
    with open('test.txt', 'w') as f:
        for item in metric.value:
            # print("{} ({})".format(item.name.localized_value, item.unit.name), file=f)
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    print("{}: {}".format(data.time_stamp, data.total), file=f)
    data = pd.read_csv('test.txt', sep=" ", header=None, names=["Date", "Timestamp", sheet])
    df0 = pd.DataFrame(data)
    return df0


def takemetricaverage(metric, sheet):
    with open('test.txt', 'w') as f:
        for item in metric.value:
            # print("{} ({})".format(item.name.localized_value, item.unit.name), file=f)
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    print("{}: {}".format(data.time_stamp, data.average), file=f)
    data = pd.read_csv('test.txt', sep=" ", header=None, names=["Date", "Timestamp", sheet])
    df0 = pd.DataFrame(data)
    return df0

###########################################################
# Capacity report ###
# Metric : Data In, Data Out
# Microsoft.Web/sites/
# Web app: MiJobsAdmin , wastematch
# Api app: mijobliveservicebiztalk, mijobliveservicemobile


metrics_DataIn = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='BytesReceived',
    aggregation='Total'
)

metrics_DataOut = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='BytesSent',
    aggregation='Total'
)

# TakeMetricTotal(metrics_DataIn)
# dfs_tabs(dfs1, sheets1, 'Capacity report.xlsx')

###########################################################


####################################################################################
# Performance report
# Metric : Avarage CPU Percentage,Avarage Memory Percentage
# Microsoft.Web/serverFarms
# Type: App service plan
# Web app: MiJobs, MiJobsLiveServiceAdmin, MiJobsLiveServiceBizTalk, WasteMatch

metrics_AverageCpuPercentage = client.metrics.list(
    resource_id_serverfarms,
    timespan=timespan,
    interval='PT1H',
    metric='CpuPercentage',
    aggregation='Average'
)

metrics_AverageMemoryPercentage = client.metrics.list(
    resource_id_serverfarms,
    timespan=timespan,
    interval='PT1H',
    metric='MemoryPercentage',
    aggregation='Average'
)

# TakeMetricAverage(metrics_AverageMemoryPercentage)
# TakeMetricAverage(metrics_AverageCpuPercentage)
####################################################################################


####################################################################################
# Monitoring report App services
# Metric :
#   Average Memory Working Set
#   Memory Percentage
#   Average Response Time
#   CPU Time
#   CPU Percentage
#   Data In
#   Data Out
#   HTTP 5xx
#   HTTP 2xx
#   HTTP 3xx
#   Http 401
#   Http 403
#   Http 404
#   Http 406
# Microsoft.Web/serverFarms
# Type: App service
# Web app: MiJobs, MiJobsLiveServiceAdmin, MiJobsLiveServiceBizTalk, WasteMatch
metrics_AverageMemoryWorkingSet = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='AverageMemoryWorkingSet',
    aggregation='Average'
)

metrics_MemoryPercentage = client.metrics.list(
    resource_id_serverfarms,
    timespan=timespan,
    interval='PT1H',
    metric='MemoryPercentage',
    aggregation='Average'
)

metrics_AverageResponseTime = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='AverageResponseTime',
    aggregation='Average'
)

metrics_CpuTime = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='CpuTime',
    aggregation='Total'
)

metrics_Http5xx = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='Http5xx',
    aggregation='Total'
)

metrics_Http2xx = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='Http2xx',
    aggregation='Total'
)

metrics_Http3xx = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='Http3xx',
    aggregation='Total'
)

metrics_Http401 = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='Http401',
    aggregation='Total'
)

metrics_Http403 = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='Http403',
    aggregation='Total'
)

metrics_Http404 = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='Http404',
    aggregation='Total'
)

metrics_Http406 = client.metrics.list(
    resource_id_web,
    timespan=timespan,
    interval='PT1H',
    metric='Http406',
    aggregation='Total'
)

'''
def count_metric_average(metric):
        for item in metric.value:
            print("{} ({})".format(item.name.localized_value, item.unit.name))
            for timeserie in item.timeseries:
                count = 0
                for data in timeserie.data:
                    print("{}: {}".format(data.time_stamp, data.average))
                    if data.average > 209715200 and metric == metrics_AverageMemoryWorkingSet:
                        count += 1
                    elif data.average > 10485760 and metric == metrics_MemoryPercentage:
                        count += 1
                    elif data.average > 8 and metric == metrics_AverageResponseTime:
                        count += 1
                print("Total times :", count)
'''


def count_metric_average(metric, sheet, threshold):
    with open('test.txt', 'w') as f:
        for item in metric.value:
            # print("{} ({})".format(item.name.localized_value, item.unit.name), file=f)
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    print("{}: {}".format(data.time_stamp, data.average), file=f)
    data = pd.read_csv('test.txt', sep=" ", header=None, names=["Date", "Timestamp", sheet])
    df0 = pd.DataFrame(data)
    return df0


def count_metric_total(metric, sheet, threshold):
    with open('test.txt', 'w') as f:
        for item in metric.value:
            # print("{} ({})".format(item.name.localized_value, item.unit.name), file=f)
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    print("{}: {}".format(data.time_stamp, data.total), file=f)
    data = pd.read_csv('test.txt', sep=" ", header=None, names=["Date", "Timestamp", sheet])
    df0 = pd.DataFrame(data)
    return df0


####################################################################################
# Create report#

# DataFrame for Monitoring report
df1 = count_metric_total(metrics_DataIn, 'DataIn', 209715200)
df2 = count_metric_total(metrics_DataOut, 'DataOut', 209715200)
df3 = count_metric_total(metrics_CpuTime, 'metrics_CpuTime', 1)
df4 = count_metric_total(metrics_Http5xx, 'metrics_Http5xx', 20)
df5 = count_metric_total(metrics_Http2xx, 'metrics_Http2xx', 0)
df6 = count_metric_total(metrics_Http3xx, 'metrics_Http3xx', 50)
df7 = count_metric_total(metrics_Http401, 'metrics_Http401', 50)
df8 = count_metric_total(metrics_Http403, 'metrics_Http403', 50)
df9 = count_metric_total(metrics_Http404, 'metrics_Http404', 50)
df10 = count_metric_total(metrics_Http406, 'metrics_Http406', 50)
df11 = count_metric_average(metrics_AverageMemoryWorkingSet, 'metrics_AverageMemoryWorkingSet', 209715200)
df12 = count_metric_average(metrics_MemoryPercentage, 'metrics_MemoryPercentage', 10485760)
df13 = count_metric_average(metrics_AverageResponseTime, 'metrics_AverageResponseTime', 8)

# DataFrame for Monitoring report
df100 = takemetrictotal(metrics_DataIn, 'metrics_DataIn')
df101 = takemetrictotal(metrics_DataOut, 'metrics_DataOut')


# dfs_tabs create excel file with multiple sheet with metric accordingly
def dfs_tabs(df_list, sheet_list, file_name):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, index=None, startrow=0, startcol=0)
    writer.save()


# list of dataframes and sheet names
dfs_Monitoring = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13]
dfs_Capacity = [df100, df101]
sheets_Monitoring = ['DataIn', 'DataOut', 'metrics_CpuTime', 'metrics_Http5xx', 'metrics_Http2xx',
                     'metrics_Http3xx', 'metrics_Http401', 'metrics_Http403', 'metrics_Http404', 'metrics_Http406',
                     'metrics_AverageMemoryWorkingSet', 'metrics_MemoryPercentage', 'metrics_AverageResponseTime']
sheets_Capacity = ['metrics_DataIn', 'metrics_DataOut']

# run function dfs_tabs to generate raw data
# dfs_tabs(dfs_Monitoring, sheets_Monitoring, 'Monitoring report.xlsx')
# dfs_tabs(dfs_Capacity, sheets_Capacity, 'Capacity report.xlsx')


# merge all data for Monitoring report
dict_Monitoring = {'DataIn': df1,
                   'DataOut': df2,
                   'metrics_CpuTime': df3,
                   'metrics_Http5xx': df4,
                   'metrics_Http2xx': df5,
                   'metrics_Http3xx': df6,
                   'metrics_Http401': df7,
                   'metrics_Http403': df8,
                   'metrics_Http404': df9,
                   'metrics_Http406': df10,
                   'metrics_AverageMemoryWorkingSet': df11,
                   'metrics_MemoryPercentage': df12,
                   'metrics_AverageResponseTime': df13}

ws_dict_Monitoring = pd.read_excel('Monitoring report.xlsx', sheet_name=None)
ws_dict_Monitoring['DataIn'] = pd.concat([dict_Monitoring['DataIn'][['Date', 'Timestamp', 'DataIn']],
                                          dict_Monitoring['DataOut'][['DataOut']],
                                          dict_Monitoring['metrics_CpuTime'][['metrics_CpuTime']],
                                          dict_Monitoring['metrics_Http5xx'][['metrics_Http5xx']],
                                          dict_Monitoring['metrics_Http2xx'][['metrics_Http2xx']],
                                          dict_Monitoring['metrics_Http3xx'][['metrics_Http3xx']],
                                          dict_Monitoring['metrics_Http401'][['metrics_Http401']],
                                          dict_Monitoring['metrics_Http403'][['metrics_Http403']],
                                          dict_Monitoring['metrics_Http404'][['metrics_Http404']],
                                          dict_Monitoring['metrics_Http406'][['metrics_Http406']],
                                          dict_Monitoring['metrics_AverageMemoryWorkingSet'][['metrics_AverageMemoryWorkingSet']],
                                          dict_Monitoring['metrics_MemoryPercentage'][['metrics_MemoryPercentage']],
                                          dict_Monitoring['metrics_MemoryPercentage'][['metrics_MemoryPercentage']]],
                                          axis=1)

with pd.ExcelWriter('Monitoring report.xlsx', engine='xlsxwriter') as writer:
    for ws_name, df_sheet in dict_Monitoring.items():
        df_sheet.to_excel(writer, sheet_name=ws_name, index=None)
    ws_dict_Monitoring['DataIn'].to_excel(writer, sheet_name='Result', index=None, startrow=0, startcol=0)
    writer.save()

####################################################################################
# Monitoring report Databases
# Metric :
#  DB_PRI_CPU Usage
#  DB_PRI_Data IO Usage
#  DB_PRI_Size Percentage
#  DB_PRI_DTU Percentage
#  DB_PRI_Failed Connections
#  DB_PRI_Blocked By Firewall
#  DB_PRI_Deadlocks
#  DB_PRI_DTU limit
#  DB_PRI_DTU used
#  DB_PRI_Log IO percentage
#  DB_Session percentage
#  DB_PRI_Storage
#  DB_PRI_Successful Connections
#  DB_PRI_Workers percentage#
# Microsoft.Sql/servers/
# Type: SQL server
# Web app: MiJobs, MiJobsLiveServiceAdmin, MiJobsLiveServiceBizTalk, WasteMatch
