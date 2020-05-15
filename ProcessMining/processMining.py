'''
Created on 12 Apr 2020

@author: Daten Master
'''

#####################################################################################################################
# GRAPHVIZ als PATH-Systemvariable setzen
#####################################################################################################################
import os
os.environ["PATH"] += os.pathsep + "/usr/local/bin"

#####################################################################################################################
# Bibliotheken importieren
#####################################################################################################################
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.visualization.dfg import factory as dfg_vis_factory
from pm4py.util import constants

#####################################################################################################################
# PROCESS DATEN [.CSV-File] einlesen
#####################################################################################################################
dataframe = csv_import_adapter.import_dataframe_from_path("/Users/datenMaster/Desktop/ProzessDaten.csv", sep=";")
#print(dataframe)

#####################################################################################################################
# Ueberblick ueber die PROCESS DATEN
#####################################################################################################################

#####################################################################################################################
# Datentransformation
#####################################################################################################################
# datetime64[Y]=year, datetime64[M]=month, datetime64[D]=day, datetime64[h]=hour, datetime64[m]=minute, datetime64[s]=second 
dataframe['Time'] = dataframe['Time'].astype('datetime64[D]')
# Attribute benennen
dataframe = dataframe.rename(columns={'CaseID':'case:concept:name', 'Time':'time:timestamp', 'Activity':'concept:name', 'Resource':'org:resource'})
#print(dataframe)

# Dataframe als log 
log = conversion_factory.apply(dataframe)
#print(log)

#####################################################################################################################
# Directly-Follows Graphs (DFG) erstellen
#####################################################################################################################
# AKCTIVITIES: ACTIVITY_KEY = "concept:name"
# RESOURCE: ACTIVITY_KEY = "org:resource"
parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name"}

# frequency = Haeufigkeiten der Activity / Resource
# performance = durchschnittliche Dauer der Activity / Resource
variant='frequency'

dfg = dfg_factory.apply(log, variant=variant, parameters=parameters)

#####################################################################################################################
# Datenvisualisierung: Directly-Follows Graphs (DFG) mit GRAPHVIZ visualisieren
#####################################################################################################################
gviz = dfg_vis_factory.apply(dfg, log=log, variant=variant, parameters=parameters)
dfg_vis_factory.view(gviz)