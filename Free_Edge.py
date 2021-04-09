# created by: sshnuke333/Nikhil
# created on: 20-01-2020

import os
import random
import ansa
from ansa import base
from ansa import guitk
from ansa import constants


@ansa.session.defbutton("MISC", "FREE EDGE")
def Free_Edge():
    '''
    Name: Free_Edge
    Description: Creates a set of elements having more than 1 free edge
    '''

    deck = constants.NASTRAN
    set_check = base.CollectEntities(deck, None, "SET")
    for set in set_check:
        if set.get_entity_values(deck, {'Name'}) == {'Name': 'Free Edge'}:
            guitk.UserWarning("SET named Free Edge already exists")
            return 1
        else:
            continue
    parts = base.CollectEntities(deck, None, "ANSAPART", filter_visible=True)
    idlist = []
    element_list = []
    final = []

    # Collect node ids of first order boundary elements from visible parts
    for part in parts:
        nodes = base.CollectBoundaryNodes(part, False)
        ids = nodes.perimeters
        for id in ids:
            for x in id:
                idlist.append(x._id)

    # collect elements from node list
    for id in idlist:
        ans = base.NodesToElements(id)
        for key, data in ans.items():
            for x in data:
                element_list.append(x)

    # remove duplicate elements
    for element in sorted(element_list):
        while element_list.count(element) > 1:
            element_list.remove(element)

    # collect nodes of each element
    # collect all the elements attached to each node
    # create a list of no.of elements attached to each node
    for element in element_list:
        G1_elements = []
        G2_elements = []
        G3_elements = []
        G4_elements = []
        G_elements = []
        card = element.get_entity_values(deck, {'G1', 'G2', 'G3', 'G4'})
        for key, data in (base.NodesToElements(card['G1']._id)).items():
            for x in data:
                G1_elements.append(x)
        for key, data in (base.NodesToElements(card['G2']._id)).items():
            for x in data:
                G2_elements.append(x)
        for key, data in (base.NodesToElements(card['G3']._id)).items():
            for x in data:
                G3_elements.append(x)
        # element type 517 is tria, ignore fourth node
        if element._type == 517:
            pass
        else:
            for key, data in (base.NodesToElements(card['G4']._id)).items():
                for x in data:
                    G4_elements.append(x)
            G4_elements.remove(element)
            G_elements.append(len(G4_elements))
        G1_elements.remove(element)
        G_elements.append(len(G1_elements))
        G2_elements.remove(element)
        G_elements.append(len(G2_elements))
        G3_elements.remove(element)
        G_elements.append(len(G3_elements))

        # element has free edge if two adj nodes have no common elements
        # store elements with more than two free edges in final list
        result = []
        for val in G1_elements:
            if G2_elements.count(val) >= 1:
                Edge1 = 0
                break
            else:
                Edge1 = 1
        result.append(Edge1)
        for val in G2_elements:
            if G3_elements.count(val) >= 1:
                Edge2 = 0
                break
            else:
                Edge2 = 1
        result.append(Edge2)
        if element._type == 517:
            for val in G3_elements:
                if G1_elements.count(val) >= 1:
                    Edge3 = 0
                    break
                else:
                    Edge3 = 1
            result.append(Edge3)
        else:
            for val in G3_elements:
                if G4_elements.count(val) >= 1:
                    Edge3 = 0
                    break
                else:
                    Edge3 = 1
            result.append(Edge3)
            for val in G4_elements:
                if G1_elements.count(val) >= 1:
                    Edge4 = 0
                    break
                else:
                    Edge4 = 1
            result.append(Edge4)
        if result.count(1) >= 2:
            final.append(element)

        # no.of elements attached to a node is 0, then node has two free edges
        elif element._type == 513 and G_elements.count(0) >= 1:
            final.append(element)

        # Trias have G4 value as zero
        elif element._type == 517 and G_elements.count(0) >= 2:
            final.append(element)
        else:
            pass

    set = base.CreateEntity(deck, 'SET', {'Name': 'Free Edge'})
    base.AddToSet(set, final)
    return 1
