from codeableModels import CMetaclass, CBundle, CException

domainMetaclass =  CMetaclass("Domain Class")
domainMetaclassGroup = CMetaclass("Domain Class Group", superclasses = domainMetaclass)
andCombinedGroup = CMetaclass("AND Combined Group", superclasses = domainMetaclassGroup)
orCombinedGroup = CMetaclass("OR Class Group", superclasses = domainMetaclassGroup)
domainMetaclassGroup.association(domainMetaclass, "[collection] * <>- [class] *")

domainMetaModel = CBundle("Domain Meta Model", elements = domainMetaclass.getConnectedElements())
