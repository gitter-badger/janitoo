#!/usr/bin/python
#From https://gist.github.com/svdgraaf/198e2c0cf4cf0a031c84
import pygraphviz as pgv
import threading

from janitoo.options import JNTOptions
from janitoo.dhcp import JNTNetwork
from janitoo.node import JNTNodeMan

class MachineGraph(object):
    def get_graph(self, machine=None, title=None):
        """Generate a DOT graph with pygraphviz."""

        state_attrs = {
            'shape': 'circle',
            'height': '1.2',
        }

        machine_attrs = {
            'directed': True,
            'strict': False,
            'rankdir': 'LR',
            'ratio': '0.3'
        }
        if machine is not None:
            fsm = machine
        else:
            fsm = self.machine

        if title is None:
            title = self.__class__.__name__
        elif title is False:
            title = ''

        fsm_graph = pgv.AGraph(title=title, **machine_attrs)
        fsm_graph.node_attr.update(state_attrs)

        # for each state, draw a circle
        for state in fsm.states.items():
            shape = state_attrs['shape']

            # we want the first state to be a double circle (UML style)
            if state == fsm.states.items()[0]:
                shape = 'doublecircle'
            else:
                shape = state_attrs['shape']

            state = state[0]
            fsm_graph.add_node(n=state, shape=shape)

        fsm_graph.add_node('null', shape='plaintext', label='')
        fsm_graph.add_edge('null', 'new')

        # For each event, add the transitions
        for event in fsm.events.items():
            event = event[1]
            label = str(event.name)

            for transition in event.transitions.items():
                src = transition[0]
                dst = transition[1][0].dest

                fsm_graph.add_edge(src, dst, label=label)

        return fsm_graph

class NetworkDoc(JNTNetwork, MachineGraph):
    pass

class NodeManDoc(JNTNodeMan, MachineGraph):
    pass

network = NetworkDoc(threading.Event(), JNTOptions({}))
network.fsm_network = network.create_fsm()
network.get_graph(network.fsm_network, 'Network state machine').draw('rst/images/fsm_network.png', prog='dot')
nodeman = NodeManDoc(JNTOptions({}), None, None)
nodeman.fsm_state = nodeman.create_fsm()
nodeman.get_graph(nodeman.fsm_state, 'NodeMan state machine').draw('rst/images/fsm_nodeman.png', prog='dot')
