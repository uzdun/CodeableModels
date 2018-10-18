from codeableModels import CClass, CMetaclass, CBundle, CStereotype

# node types
activityNode = CMetaclass("ActivityNode") 
controlNode = CMetaclass("ControlNode", superclasses = activityNode) 
finalNode = CMetaclass("FinalNode", superclasses = controlNode) 
activityFinalNode = CMetaclass("ActivityFinalNode", superclasses = finalNode) 
forkNode = CMetaclass("ForkNode", superclasses = controlNode) 
joinNode = CMetaclass("JoinNode", superclasses = controlNode) 
decisionNode = CMetaclass("DecisionNode", superclasses = controlNode, attributes = {"decision": str}) 
mergeNode = CMetaclass("MergeNode", superclasses = controlNode) 
initialNode = CMetaclass("InitialNode", superclasses = controlNode) 
action = CMetaclass("Action", superclasses = activityNode) 
acceptEventAction = CMetaclass("AcceptEventAction", superclasses = action) 

# edges
edgeRelation = activityNode.association(activityNode, "[source] * -> [target] *")

_all = CBundle("_all", 
    elements = activityNode.getConnectedElements(addStereotypes = True))

activityMetamodelViews = [
    _all, {}]