# created by: sshnuke333/Nikhil
# created on: 27-08-2020

import os
import random
import ansa
from ansa import *


@ansa.session.defbutton("Elements", "Counter")
def Counter():
    '''
Name: Counter
Description: Renames the PIDs of the F.E. with the ANSA filename/part name and thickness.
corrects thickness to two decimal places.
Changes Elements and Grid Ids according to user entered counter value.
Checks and fixes geometry errors and
duplicate materials.
    '''

# Create PID change format push buttons
    window1 = guitk.BCWindowCreate(
        "Select PID Format", guitk.constants.BCOnExitDestroy)
    guitk.BCWindowShowTitleBarButtons(
        window1, guitk.constants.BCMinimizeButton | guitk.constants.BCMaximizeButton)
    button1 = guitk.BCPushButtonCreate(
        window1, "Partname to PID", PPID, window1)
    button2 = guitk.BCPushButtonCreate(
        window1, "Filename to PID", FPID, window1)
    guitk.BCShow(window1)
    return 1

# Partname to PID


def PPID(b, window1):

    name = PPID
    main(name)
    return 1

# Filename to PID


def FPID(b, window1):

    name = FPID
    main(name)
    return 1

# Ask for Counter Value. set default counter value as 1000


def main(name):
    window2 = guitk.BCWindowCreate("Counter", guitk.constants.BCOnExitDestroy)
    BCBoxLayout_1 = guitk.BCBoxLayoutCreate(
        window2, guitk.constants.BCHorizontal)
    BCLabel_1 = guitk.BCLabelCreate(BCBoxLayout_1, "Enter Counter Value")
    BCLineEdit = []
    count_val = guitk.BCLineEditCreateInt(BCBoxLayout_1, 1000)
    name = name
    BCLineEdit.append(count_val)
    BCLineEdit.append(name)
    BCDialogButtonBox_1 = guitk.BCDialogButtonBoxCreate(window2)
    guitk.BCWindowSetAcceptFunction(window2, _OK, BCLineEdit)
    guitk.BCWindowSetRejectFunction(window2, _Cancel, None)
    guitk.BCShow(window2)
    return 1


def _Cancel(window2, data):
    print("The process has been canceled.")
    return 1


def _OK(window2, data):
    COUNTER = ansa.guitk.BCLineEditGetInt(data[0])
    name = data[1]
    list_of_files = utils.SelectOpenFileIn('', 1)
    i = 0
    j = 0
    elem_counter = COUNTER
    grid_counter = COUNTER

    # Check the opening file type
    for file in list_of_files:
        if file.endswith('.ansa'):
            elem = 'SHELL'
            point = 'GRID'
            session.New('discard')
            print('Opening file:'+file)
            base.Open(file)
            default_deck = base.CurrentDeck()
            base.SetCurrentDeck(constants.NASTRAN)
            deck = constants.NASTRAN
            prop = 'PSHELL'
            actual_name = file.split(".ansa")

            # turn off cad visibilty
            base.SetViewButton({"SHADOW": 'on', "MACROs": 'off'})
            pids = base.CollectEntities(
                deck, None, prop, filter_visible=True, prop_from_entities=True)

            # collect thickness values and correct them to two decimal places
            t_list = []
            for i in range(0, len(pids)):
                ent = pids[i]
                ret_vals = ent.get_entity_values(deck, {'T'})
                t = str(ret_vals['T'])
                split_t = t.split(".")
                decimal = split_t[1][:2]
                new_t = (float(split_t[0]+"."+decimal))
                t_list.append(new_t)
                i += 1

            # collect PIDs to edit based on ascending thikness values
            t_ascend = sorted(t_list)
            for j in range(0, len(t_ascend)):
                index = t_list.index(t_ascend[j])
                t_list[index] = 'Done'
                ent = pids[index]
                thickness = t_ascend[j]
                ent.set_entity_values(deck, {"FROZEN_ID": 'NO'})
                ent.set_entity_values(deck, {"T": thickness})
                pidn = ent.get_entity_values(deck, {'PID'})

                # change PID name based on user selection
                # set random PID number to avoid error
                # set random PID number to counter value
                if name == FPID:
                    number = actual_name[0].count("/")
                    temp_name = actual_name[0].split("/")
                    clean_name = temp_name[number]
                    ent.set_entity_values(
                        deck, {'PID': random.randint(10E9, 10E10)})
                    ent.set_entity_values(
                        deck, {"Name": clean_name + '_'+str(thickness)+'mm', 'PID': COUNTER})
                elif name == PPID:
                    k = 0
                    parts = base.CollectEntities(
                        deck, None, "ANSAPART", filter_visible=True)
                    for parts[k] in parts:
                        part = parts[k].get_entity_values(deck, {'PID'})
                        a = list(part.values())[0].split(', ')
                        b = str(pidn['PID'])
                        if a.__contains__(b) == True:
                            part_name = parts[k]._name
                            ent.set_entity_values(
                                deck, {"Name": part_name+'_'+str(thickness)+'mm', 'PID': random.randint(10E9, 10E10)})
                            ent.set_entity_values(deck, {'PID': COUNTER})
                            break
                        else:
                            k += 1
                COUNTER += 1
                j += 1

            elems(deck, elem_counter, elem)
            grids(deck, grid_counter, point)
            Checks(deck, prop)
            base.SetViewButton({"SHADOW": 'on', "MACROs": 'on'})
            base.SetCurrentDeck(default_deck)
            base.Compress('')
            base.SaveAs(actual_name[0]+"_result.ansa")

        elif file.endswith('.key'):
            elem = 'ELEMENT_SHELL'
            point = 'NODE'
            session.New('discard')
            print(file+'has been input')
            base.InputLSDyna(file)
            base.SetCurrentDeck(constants.LSDYNA)
            deck = constants.LSDYNA
            prop = 'SECTION_SHELL'
            actual_name = file.split(".key")

            # turn of cad visibility
            base.SetViewButton({"SHADOW": 'on', "MACROs": 'off'})
            pids = base.CollectEntities(
                deck, None, prop, filter_visible=True, prop_from_entities=True)

            # collect thickness values and correct them to two decimal places
            t_list = []
            for i in range(0, len(pids)):
                ent = pids[i]
                ret_vals = ent.get_entity_values(deck, {'T1'})
                t = str(ret_vals['T1'])
                split_t = t.split(".")
                decimal = split_t[1][:2]
                new_t = (float(split_t[0]+"."+decimal))
                t_list.append(new_t)
                i += 1

            # Collect and edit PIDs according to ascending thickness values
            t_ascend = sorted(t_list)
            for j in range(0, len(t_ascend)):
                index = t_list.index(t_ascend[j])
                ent = pids[index]
                t_list[index] = 'Done'
                thickness = t_ascend[j]
                ent.set_entity_values(deck, {"FROZEN_ID": 'NO'})
                ent.set_entity_values(deck, {"T1": thickness})
                pidn = ent.get_entity_values(deck, {'PID'})
                if name == FPID:
                    number = actual_name[0].count("/")
                    temp_name = actual_name[0].split("/")
                    clean_name = temp_name[number]
                    ent.set_entity_values(
                        deck, {'PID': random.randint(10E9, 10E10)})
                    ent.set_entity_values(
                        deck, {"Name": clean_name + '_'+str(thickness)+'mm', 'PID': COUNTER})
                elif name == PPID:
                    k = 0
                    parts = base.CollectEntities(
                        deck, None, "ANSAPART", filter_visible=True)
                    for parts[k] in parts:
                        part = parts[k].get_entity_values(deck, {'PID'})
                        a = list(part.values())[0].split(', ')
                        b = str(pidn['PID'])
                        if a.__contains__(b) == True:
                            part_name = parts[k]._name
                            ent.set_entity_values(
                                deck, {"Name": part_name+'_'+str(thickness)+'mm', 'PID': random.randint(10E9, 10E10)})
                            ent.set_entity_values(deck, {'PID': COUNTER})
                            break
                        else:
                            k += 1
                COUNTER += 1
                j += 1

            elems(deck, elem_counter, elem)
            grids(deck, grid_counter, point)
            Checks(deck, prop)
            base.SetViewButton({"SHADOW": 'on', "MACROs": 'on'})
            base.Compress('')
            base.SaveAs(actual_name[0]+"_result.ansa")
    print("File saved!")

    return 1

# change elements numbering according to counter value


def elems(deck, elem_counter, elem):
    elems = base.CollectEntities(deck, None, elem)
    for i in range(0, len(elems)):
        base.SetEntityId(elems[i], elem_counter, True, False)
        elem_counter += 1
        i += 1
    return 1

# change grid numbering according to counter value


def grids(deck, grid_counter, point):
    grids = base.CollectEntities(deck, None, point)
    for i in range(0, len(grids)):
        base.SetEntityId(grids[i], grid_counter, True, False)
        grid_counter += 1
        i += 1
    return 1

# check and fix errors


def Checks(deck, prop):

    # check for intersections
    intersections = base.CheckAndFixPenetrations(
        type=1, fast_run=False, fix=False)

    # check for penetrarion error for user thickness value of 0.6
    user_thic = base.CheckAndFixPenetrations(
        type=3, fast_run=False, fix=False, user_thic=0.6)

    if intersections == -1:
        print("Error in input file. Please Check your input file")
    elif intersections == 1:
        print("Intersections found:", len(intersections))
        print(intersections)
    else:
        print('No intersections found!!')

    if user_thic == -1:
        print('Error in input file. Please check your Input file')
    elif user_thic == 1:
        print("Pentrations for 0.6 thickness found!")
        print("Errors:", len(user_thic))
    else:
        print('No pentrations found!')
    base.Compress('')

    # remove duplicate materials
    base.CompressMaterials(deck, None, 1, 1, 1)
    base.DeleteCurves('all', True)
    base.PointsDelete('all')
    return 1
