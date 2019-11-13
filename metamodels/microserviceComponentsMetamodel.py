from codeableModels import CClass, CMetaclass, CBundle, CStereotype
from metamodels.componentMetamodel import *

# Component types
service = CStereotype("Service", superclasses = componentType)
database = CStereotype("Database", superclasses = componentType)
pubSubComponent = CStereotype("Pub/Sub Component", superclasses = componentType)
messageBroker = CStereotype("Message Broker", superclasses = componentType)
# a component that provides event sourcing, could be e.g. on a pub/sub component as an additional function
# or on a component listening to events
eventSourcing = CStereotype("Event Sourcing", superclasses = componentType)
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
redisDB = CStereotype("RedisDB", superclasses = database)

monitoringComponent = CStereotype("Monitoring", superclasses = componentType)
tracingComponent = CStereotype("Tracing", superclasses = componentType)
loggingComponent = CStereotype("Logging", superclasses = componentType)

orchestrator = CStereotype("Orchestrator", superclasses = componentType)
sagaOrchestrator = CStereotype("Saga Orchestrator", superclasses = orchestrator)

# Connector types
directed = CStereotype("Directed", superclasses = connectorType)

# use synchronousConnector especially if connector implies asynchronous communication (as in messaging), but is used synchronously
synchronousConnector = CStereotype("Synchronous", superclasses = connectorType) 
# use asynchronousConnector especially if connector implies synchronous communication (as in restfulHTTP), but is used asynchronously
asynchronousConnector = CStereotype("Asynchronous", superclasses = connectorType) 
# use both syncAsyncConnector, if both forms are mixed (or leave unspecified)
syncAsyncConnector = CStereotype("Synchronous + Asynchronous", superclasses = [synchronousConnector, asynchronousConnector]) 

callback = CStereotype("Callback", superclasses = asynchronousConnector)
polling = CStereotype("Polling", superclasses = asynchronousConnector)
oneway = CStereotype("One Way", superclasses = asynchronousConnector)

indirectRelationViaAPI = CStereotype("Indirect Relation via API", superclasses = connectorType)

inMemoryConnector = CStereotype("In-Memory Connector", superclasses = connectorType)
databaseConnector = CStereotype("Database Connector", superclasses = connectorType)
serviceConnector = CStereotype("Service Connector", superclasses = connectorType)
webConnector = CStereotype("Web Connector", superclasses = connectorType)
looselyCoupledConnector = CStereotype("Loosely Coupled Connector", superclasses = connectorType)
ldap = CStereotype("LDAP", superclasses = connectorType)
memcachedConnector = CStereotype("Memcached Connector", superclasses = connectorType)
messaging = CStereotype("Messaging", superclasses = connectorType)
eventBasedConnector = CStereotype("Event-Based Connector", superclasses = looselyCoupledConnector)

publisher = CStereotype("Publisher", superclasses = eventBasedConnector,
    attributes = {"publishedTopics": []})
subscriber = CStereotype("Subscriber", superclasses = eventBasedConnector,
    attributes = {"subscribedTopics": []})

messageProducer = CStereotype("Message Producer", superclasses = messaging, attributes = {"outChannels": []})
messageConsumer = CStereotype("Message Consumer", superclasses = messaging, attributes = {"inChannels": []})

jdbc = CStereotype("JDBC", superclasses = databaseConnector)
odbc = CStereotype("ODBC", superclasses = databaseConnector)
mongoWire = CStereotype("MongoWire", superclasses = databaseConnector)
hdfs = CStereotype("HDFS", superclasses = databaseConnector)
resp = CStereotype("RESP", superclasses = databaseConnector)
mySQLProtocol = CStereotype("MySQL Protocol", superclasses = databaseConnector)

restfulHTTP = CStereotype("RESTful HTTP", superclasses = serviceConnector)
soap = CStereotype("SOAP", superclasses = serviceConnector)
avro = CStereotype("AVRO", superclasses = serviceConnector)
grpc = CStereotype("GRPC", superclasses = serviceConnector)

jms = CStereotype("JMS", superclasses = messaging)
stomp = CStereotype("STOMP", superclasses = messaging)

http = CStereotype("HTTP", superclasses = webConnector)
https = CStereotype("HTTPS", superclasses = webConnector)
http2 = CStereotype("HTTP/2", superclasses = webConnector)

_all = CBundle("_all", 
    elements = component.getConnectedElements(addStereotypes = True) + connectorType.getConnectedElements(addStereotypes = True))

componentStereotypes = CBundle("Component Stereotypes", elements = componentType.getConnectedElements(addStereotypes = True))
connectorStereotypes = CBundle("Connector Stereotypes", elements = [component] + connectorType.getConnectedElements(addStereotypes = True))

componentMetamodelViews = [
    _all, {},
    componentStereotypes, {},
    connectorStereotypes, {}]
