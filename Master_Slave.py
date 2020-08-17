# created by: sshnuke333/Nikhil
# created on: 16-12-2019																																									##

import os
import random
import ansa
from ansa import base
from ansa import guitk
from ansa import constants

@ansa.session.defbutton("MISC","MASTER_SLAVE")

def master_slave():
	'''
	Name: Master_Slave
	Description: Creates a table simliar to a spreadsheet with list of master and slave PIDs selected
	'''

	deck = constants.NASTRAN
	prop = '__PROPERTIES__'
	i = 0
	master_list = []
	slave_list = []
	mid = []
	sid = []

	# pick pid using entites
	base.SetPickMethod(base.constants.ENT_SELECTION)

	# collect entites and properties from visible
	# warn user if none selected using error()
	list = base.PickEntities(deck,prop,filter_visible=True,prop_from_entities=True)
	if list == None:
		error()
		return 1

	# set every even selection ito master list
	# set every odd selection to slave list
	for i in range(0,len(list)):
		if (i%2) == 0 or i == 0:
			master = list[i].get_entity_values(deck,{'PID'})
			master_list.append(master['PID'])
		elif (i%2) == 1 and i > 0:
			slave = list[i].get_entity_values(deck,{'PID'})
			slave_list.append(slave['PID'])
		i+=1
	table(master_list,slave_list)
	return 1

def error():
	window = guitk.BCMessageWindowCreate(guitk.constants.BCMessageBoxWarning,'No element selected',False)
	guitk.BCMessageWindowSetRejectButtonVisible(window, False)
	guitk.BCWindowFlash(window)
	guitk.BCShow(window)
	return 1

def table(master_list,slave_list):
	window = guitk.BCWindowCreate("Master Slave Table", guitk.constants.BCOnExitDestroy)
	table = guitk.BCTableCreate(window,2,2)
	guitk.BCTableSetNumRows(table,len(master_list))
	guitk.BCTableHeaderSetLabel(table,guitk.constants.BCHorizontal,0,'Master')
	guitk.BCTableHeaderSetLabel(table,guitk.constants.BCHorizontal,1,'Slave')
	i = 0
	for i in range(0,len(master_list)):
		guitk.BCTableSetText(table,i,0,str(master_list[i]))
		i+=1
	for i in range(0,len(slave_list)):
		guitk.BCTableSetText(table,i,1,str(slave_list[i]))
		i+=1
	guitk.BCTableSetColumnAlignment(table,0,guitk.constants.BCAlignRight)
	guitk.BCTableSetColumnAlignment(table,1,guitk.constants.BCAlignRight)
	guitk.BCTableSetReadOnly(table,True)
	guitk.BCShow(window)
	return 1
