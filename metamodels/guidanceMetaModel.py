

from codeableModels import CMetaclass, CBundle, CException, CStereotype
from metamodels.domainMetaModel import domainMetaclass, domainMetaModel

modelElement = CMetaclass("Model Element", attributes = {"aka": str, "description": str})
category = CMetaclass("Category", superclasses = modelElement)

designSolution = CMetaclass("Design Solution", superclasses = modelElement, 
        attributes = {"background reading": str})

designSolutionDomainMetaclass = CMetaclass("Design Solution / Domain Class", superclasses = [designSolution, domainMetaclass])

practice = CMetaclass("Practice", superclasses = designSolution)
pattern = CMetaclass("Pattern", superclasses = practice)

knownUse = CMetaclass("Known Use", superclasses = modelElement,
        attributes = {"reference": str})
solutionsKnownUsesRelation = designSolution.association(knownUse, "used in: [solutions] * -> [knownUses] *")

decision = CMetaclass("Decision", superclasses = designSolution, attributes = {"recommendation": str})
categoryDecisionsRelation = category.association(decision, "[category] 1 <>- [decisions] *")

decisionType = CStereotype("Decision Type", extended = decision)
singleAnswer = CStereotype("Single Answers", superclasses = decisionType)
multipleAnswers = CStereotype("Multiple Answers", superclasses = decisionType)

force = CMetaclass("Force", superclasses = modelElement)
forceImpactRelation = designSolution.association(force, "has force: [solutions] * -> [forces] *")

forceImpactType = CStereotype("Force Impact Type", extended = forceImpactRelation)
veryPositive = CStereotype("++", superclasses = forceImpactType)
positive = CStereotype("+", superclasses = forceImpactType)
neutral = CStereotype("o", superclasses = forceImpactType)
negative = CStereotype("-", superclasses = forceImpactType)
veryNegative = CStereotype("--", superclasses = forceImpactType)
positiveAndNegative = CStereotype("+/-", superclasses = forceImpactType)

categoryHierarchyRelation = category.association(category, "has sub-category: [parent category] 1 <*>- [sub category] *")

designSolutionDependencies = designSolution.association(designSolution, "is dependent on: [from] * -> [to] *")
designSolutionDependencyType = CStereotype("Design Solution Dependency Type", extended = designSolutionDependencies,
        attributes = {"how": str, "role": str})
requires = CStereotype("Requires", superclasses = designSolutionDependencyType)
uses = CStereotype("Uses", superclasses = designSolutionDependencyType)
canUse = CStereotype("Can Use", superclasses = designSolutionDependencyType)
canBeCombinedWith = CStereotype("Can Be Combined With", superclasses = designSolutionDependencyType)
canBeRealizedWith = CStereotype("Can be Realized With", superclasses = designSolutionDependencyType)
variant = CStereotype("Variant", superclasses = designSolutionDependencyType)
isA = CStereotype("Is-a", superclasses = designSolutionDependencyType)
realizes = CStereotype("Realizes", superclasses = designSolutionDependencyType)
includes = CStereotype("Includes", superclasses = designSolutionDependencyType)
alternativeTo = CStereotype("Alternative To", superclasses = designSolutionDependencyType)
rulesOut = CStereotype("Rules Out", superclasses = designSolutionDependencyType)
influences = CStereotype("Influences", superclasses = designSolutionDependencyType)
leadsTo = CStereotype("Leads To", superclasses = designSolutionDependencyType)


solutionsToNextDecisionsRelation = designSolution.association(decision, "is next: [prior solution] * -> [next decision] *")

solutionsToNextDecisionsRelationType = CStereotype("Solutions To Decisions Relation Type", 
        extended = solutionsToNextDecisionsRelation)
mandatoryNext = CStereotype("Mandatory Next", superclasses = solutionsToNextDecisionsRelationType)
optionalNext = CStereotype("Optional Next", superclasses = solutionsToNextDecisionsRelationType)
considerIfNotDecidedYet = CStereotype("Consider If Not Decided Yet", superclasses = solutionsToNextDecisionsRelationType)

decisionSolutionRelation = decision.association(designSolution, "has: *->*")
option = CStereotype("Option", extended = decisionSolutionRelation, 
        attributes = {"name":str})

decisionCategoryToContextsRelation = category.association(domainMetaclass, "has context: [category] * -> [context] *")

decisionToContextsRelation = decision.association(domainMetaclass, "has context: [decision] * -> [context] *")

contextRelationsType = CStereotype("Decision Category To Contexts Relation Type",
        extended = [decisionCategoryToContextsRelation, decisionToContextsRelation])
decideForAllInstancesOf = CStereotype("decide for all instances of", superclasses = contextRelationsType)
decideForSomeInstancesOf = CStereotype("decide for some instances of", superclasses = contextRelationsType)

doNothingDesignSolution = CMetaclass("Do Nothing", superclasses = designSolution)

# bundles

_all = CBundle("Guidance Meta Model", elements = modelElement.getConnectedElements())

guidanceMetaModelHierarchy = CBundle("Guidance Meta Model Hierarchy", 
        elements = modelElement.getConnectedElements(stopElementsExclusive = domainMetaclass))

guidanceMetaModelDetails = CBundle("Guidance Meta Model Details", 
        elements = designSolution.getConnectedElements(stopElementsInclusive = domainMetaclass, 
                stopElementsExclusive = [modelElement, doNothingDesignSolution, practice, pattern]))

forceImpactMetaclasses = [forceImpactRelation.source, forceImpactRelation.target]
forceImpactTypeBundle = CBundle("Force Impact Types", 
        elements = forceImpactMetaclasses + forceImpactType.getConnectedElements(addStereotypes = True, 
        stopElementsInclusive = forceImpactMetaclasses))

designSolutionDependenciesMetaclasses = [designSolutionDependencies.source, designSolutionDependencies.target]
designSolutionDependencyTypeBundle = CBundle("Design Solution Dependency Types", 
        elements = designSolutionDependenciesMetaclasses + designSolutionDependencyType.getConnectedElements(addStereotypes = True, 
        stopElementsInclusive = designSolutionDependenciesMetaclasses))

solutionsToNextDecisionsRelationMetaclasses = [solutionsToNextDecisionsRelation.source, solutionsToNextDecisionsRelation.target]
solutionToNextDecisionsRelationTypeBundle = CBundle("Solutions To Next Decisions Relation Types", 
        elements = solutionsToNextDecisionsRelationMetaclasses + solutionsToNextDecisionsRelationType.getConnectedElements(addStereotypes = True, 
        stopElementsInclusive = solutionsToNextDecisionsRelationMetaclasses))

decisionCategoryToContextsRelationMetaclasses = [decisionCategoryToContextsRelation.source, decisionCategoryToContextsRelation.target]
contextRelationsTypeBundle = CBundle("Decision Category To Contexts Relation Types", 
        elements = decisionCategoryToContextsRelationMetaclasses + contextRelationsType.getConnectedElements(addStereotypes = True, 
        stopElementsInclusive = decisionCategoryToContextsRelationMetaclasses))

guidanceMetaModelViews = [_all, {},
    guidanceMetaModelHierarchy, {"renderAssociations": False},
    guidanceMetaModelDetails, {},
    domainMetaModel, {},
    forceImpactTypeBundle, {},
    designSolutionDependencyTypeBundle, {},
    solutionToNextDecisionsRelationTypeBundle, {},
    contextRelationsTypeBundle, {}]

# helper functions
def addStereotypedLinkWithHowTaggedValue(linkFrom, linkTo, stereotypeInstance, tagValue):
    l = linkFrom.addLinks(linkTo, roleName = "to")[0]
    l.stereotypeInstances = [stereotypeInstance]
    l.setTaggedValue("how", tagValue)
    return l

def addStereotypedLinkWithRoleTaggedValue(linkFrom, linkTo, stereotypeInstance, tagValue):
    l = linkFrom.addLinks(linkTo, roleName = "to")[0]
    l.stereotypeInstances = [stereotypeInstance]
    l.setTaggedValue("role", tagValue)
    return l

def addDecisionOptionLink(decision, designSolution, optionName):
    l = decision.addLinks(designSolution, association = decisionSolutionRelation)[0]
    l.stereotypeInstances = [option]
    if optionName != None:
        l.setTaggedValue("name", optionName)
    return l

def addStereotypedDesignSolutionLink(fromDesignSolution, toDesignSolution, stereotypeInstance):
    fromDesignSolution.addLinks(toDesignSolution, roleName = "to")[0].stereotypeInstances = [stereotypeInstance]