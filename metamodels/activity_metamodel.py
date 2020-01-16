from codeable_models import CMetaclass, CBundle

# node types
activity_node = CMetaclass("Activity Node")
control_node = CMetaclass("Control Node", superclasses=activity_node)
initial_node = CMetaclass("Initial Node", superclasses=control_node)
final_node = CMetaclass("Final Node", superclasses=control_node)
activity_final_node = CMetaclass("Activity Final Node", superclasses=final_node)
fork_node = CMetaclass("Fork Node", superclasses=control_node)
join_node = CMetaclass("Join Node", superclasses=control_node)
decision_node = CMetaclass("Decision Node", superclasses=control_node, attributes={"decision": str})
merge_node = CMetaclass("Merge Node", superclasses=control_node)
action = CMetaclass("Action", superclasses=activity_node)
accept_event_action = CMetaclass("Accept Event Action", superclasses=action)
accept_time_event_action = CMetaclass("Accept Time Event Action", superclasses=accept_event_action,
                                      attributes={"description": str})
send_signal_action = CMetaclass("Send Signal Action", superclasses=action)

# edges
edge_relation = activity_node.association(activity_node, "next: [source] * -> [target] *")

_all = CBundle("_all",
               elements=activity_node.get_connected_elements(add_stereotypes=True))

activityMetamodelViews = [
    _all, {}]
