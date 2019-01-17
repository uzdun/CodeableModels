from codeableModels import CClass, CMetaclass, CBundle, CStereotype

# node types
activityNode = CMetaclass("ActivityNode") 
controlNode = CMetaclass("ControlNode", superclasses = activityNode) 
initialNode = CMetaclass("InitialNode", superclasses = controlNode) 
finalNode = CMetaclass("FinalNode", superclasses = controlNode) 
activityFinalNode = CMetaclass("ActivityFinalNode", superclasses = finalNode) 
forkNode = CMetaclass("ForkNode", superclasses = controlNode) 
joinNode = CMetaclass("JoinNode", superclasses = controlNode) 
decisionNode = CMetaclass("DecisionNode", superclasses = controlNode, attributes = {"decision": str}) 
mergeNode = CMetaclass("MergeNode", superclasses = controlNode) 
action = CMetaclass("Action", superclasses = activityNode) 
acceptEventAction = CMetaclass("AcceptEventAction", superclasses = action)
acceptTimeEventAction = CMetaclass("AcceptTimeEventAction", superclasses = action, attributes = {"description": str})
sendSignalAction = CMetaclass("SendSignalAction", superclasses = action) 

# edges
edgeRelation = activityNode.association(activityNode, "next: [source] * -> [target] *")

_all = CBundle("_all", 
    elements = activityNode.getConnectedElements(addStereotypes = True))

activityMetamodelViews = [
    _all, {}]