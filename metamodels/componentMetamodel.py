from codeableModels import CClass, CMetaclass, CBundle, CStereotype

# Component and component types
component = CMetaclass("Component")

componentType = CStereotype("Component Type", extended = component)

service = CStereotype("Service", superclasses = componentType)
database = CStereotype("Database", superclasses = componentType)
pubSubComponent = CStereotype("Pub/Sub Component", superclasses = componentType)
externalComponent = CStereotype("External Component", superclasses = componentType)
facade = CStereotype("Facade", superclasses = componentType)

client = CStereotype("Client", superclasses = externalComponent)
webUI = CStereotype("Web UI", superclasses = facade)

inMemoryDataStore = CStereotype("In-Memory Data Store", superclasses = database)
postgreSQLDB = CStereotype("PostgreSQLDB", superclasses = database)
mySQLDB = CStereotype("MySQLDB", superclasses = database)
mongoDB = CStereotype("MongoDB", superclasses = database)
lDAPStore = CStereotype("LDAPStore", superclasses = database)
elasticSearchStore = CStereotype("ElasticSearchStore", superclasses = database)
memcachedDB = CStereotype("MemcachedDB", superclasses = database)

# connector relation and connector types
connectorsRelation = component.association(component, "component connector: [source] * -> [target] *")

connectorType = CStereotype("Connector Type", extended = connectorsRelation)
directed = CStereotype("Directed", superclasses = connectorType)
callback = CStereotype("Callback", superclasses = connectorType)

inMemoryConnector = CStereotype("In-Memory Connector", superclasses = connectorType)
databaseConnector = CStereotype("Database Connector", superclasses = connectorType)
serviceConnector = CStereotype("Service Connector", superclasses = connectorType)
webConnector = CStereotype("Web Connector", superclasses = connectorType)
looselyCoupledConnector = CStereotype("Loosely Coupled Connector", superclasses = connectorType)
ldap = CStereotype("LDAP", superclasses = connectorType)
memcachedConnector = CStereotype("Memcached Connector", superclasses = connectorType)
messaging = CStereotype("Messaging", superclasses = connectorType)

eventBasedConnector = CStereotype("Event-Based Connector", superclasses = looselyCoupledConnector)
pubSubConnector = CStereotype("Pub/Sub Connector", superclasses = looselyCoupledConnector)

jdbc = CStereotype("JDBC", superclasses = databaseConnector)
odbc = CStereotype("ODBC", superclasses = databaseConnector)
mongoWire = CStereotype("MongoWire", superclasses = databaseConnector)
hdfs = CStereotype("HDFS", superclasses = databaseConnector)

restfulHTTP = CStereotype("RESTful HTTP", superclasses = serviceConnector)
soap = CStereotype("SOAP", superclasses = serviceConnector)
avro = CStereotype("AVRO", superclasses = serviceConnector)
grpc = CStereotype("GRPC", superclasses = serviceConnector)

jms = CStereotype("JMS", superclasses = messaging)
stomp = CStereotype("STOMP", superclasses = messaging)

http = CStereotype("HTTP", superclasses = webConnector)
https = CStereotype("HTTPS", superclasses = webConnector)

publisher = CStereotype("Publisher", superclasses = eventBasedConnector)
subscriber = CStereotype("Subscriber", superclasses = eventBasedConnector)

_all = CBundle("_all", 
    elements = component.getConnectedElements(addStereotypes = True) + connectorType.getConnectedElements(addStereotypes = True))

componentStereotypes = CBundle("Component Stereotypes", elements = componentType.getConnectedElements(addStereotypes = True))
connectorStereotypes = CBundle("Connector Stereotypes", elements = [component] + connectorType.getConnectedElements(addStereotypes = True))

componentMetamodelViews = [
    _all, {},
    componentStereotypes, {},
    connectorStereotypes, {}]
