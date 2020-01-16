from codeable_models import CClass, CMetaclass, CBundle, CStereotype
from metamodels.componentMetamodel import *

# Component types
service = CStereotype("Service", superclasses = component_type)
database = CStereotype("Database", superclasses = component_type)
pubSubComponent = CStereotype("Pub/Sub Component", superclasses = component_type)
messageBroker = CStereotype("Message Broker", superclasses = component_type)
# a component that provides event sourcing, could be e.g. on a pub/sub component as an additional function
# or on a component listening to events
eventSourcing = CStereotype("Event Sourcing", superclasses = component_type)
# stream-processing platforms like Kafka process events and messages, and keep a persistent distributed
# log of those, which can be used for eventSourcing; thus they combine abilities of all of those
streamProcessing = CStereotype("Stream Processing", superclasses = [pubSubComponent, messageBroker, eventSourcing])

externalComponent = CStereotype("External Component", superclasses = component_type)
facade = CStereotype("Facade", superclasses = component_type)

client = CStereotype("Client", superclasses = externalComponent)
webUI = CStereotype("Web UI", superclasses = facade)

inMemoryDataStore = CStereotype("In-Memory Data Store", superclasses = database)
postgreSQLDB = CStereotype("PostgreSQLDB", superclasses = database)
mySQLDB = CStereotype("MySQLDB", superclasses = database)
sqlServer = CStereotype("SQL Server", superclasses = database)
mongoDB = CStereotype("MongoDB", superclasses = database)
lDAPStore = CStereotype("LDAPStore", superclasses = database)
elasticSearchStore = CStereotype("ElasticSearchStore", superclasses = database)
memcachedDB = CStereotype("MemcachedDB", superclasses = database)
redisDB = CStereotype("RedisDB", superclasses = database)
eventStore = CStereotype("Event Store", superclasses = database)

monitoringComponent = CStereotype("Monitoring", superclasses = component_type)
tracingComponent = CStereotype("Tracing", superclasses = component_type)
loggingComponent = CStereotype("Logging", superclasses = component_type)

orchestrator = CStereotype("Orchestrator", superclasses = component_type)
sagaOrchestrator = CStereotype("Saga Orchestrator", superclasses = orchestrator,
                               attributes = {"sagas": list})

# Connector types
directed = CStereotype("Directed", superclasses = connector_type)

# use synchronousConnector especially if connector implies asynchronous communication (as in messaging), but is used synchronously
synchronousConnector = CStereotype("Synchronous", superclasses = connector_type)
# use asynchronousConnector especially if connector implies synchronous communication (as in restfulHTTP), but is used asynchronously
asynchronousConnector = CStereotype("Asynchronous", superclasses = connector_type)
# use both syncAsyncConnector, if both forms are mixed (or leave unspecified)
syncAsyncConnector = CStereotype("Synchronous + Asynchronous", superclasses = [synchronousConnector, asynchronousConnector]) 

callback = CStereotype("Callback", superclasses = asynchronousConnector)
polling = CStereotype("Polling", superclasses = asynchronousConnector)
oneway = CStereotype("One Way", superclasses = asynchronousConnector)

indirectRelationViaAPI = CStereotype("Indirect Relation via API", superclasses = connector_type)

inMemoryConnector = CStereotype("In-Memory Connector", superclasses = connector_type)
databaseConnector = CStereotype("Database Connector", superclasses = connector_type,
                                attributes = {"read": list, "write": list, "read + write": list})
serviceConnector = CStereotype("Service Connector", superclasses = connector_type)
webConnector = CStereotype("Web Connector", superclasses = connector_type)
looselyCoupledConnector = CStereotype("Loosely Coupled Connector", superclasses = connector_type)
ldap = CStereotype("LDAP", superclasses = connector_type)
memcachedConnector = CStereotype("Memcached Connector", superclasses = connector_type)
messaging = CStereotype("Messaging", superclasses = connector_type)
eventBasedConnector = CStereotype("Event-Based Connector", superclasses = looselyCoupledConnector)

publisher = CStereotype("Publisher", superclasses = eventBasedConnector,
    attributes = {"publishes": list})
subscriber = CStereotype("Subscriber", superclasses = eventBasedConnector,
    attributes = {"subscribesTo": list})

messageProducer = CStereotype("Message Producer", superclasses = messaging, attributes = {"outChannels": list})
messageConsumer = CStereotype("Message Consumer", superclasses = messaging, attributes = {"inChannels": list})

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
thrift = CStereotype("Thrift", superclasses = serviceConnector)

jms = CStereotype("JMS", superclasses = messaging)
stomp = CStereotype("STOMP", superclasses = messaging)

http = CStereotype("HTTP", superclasses = webConnector)
https = CStereotype("HTTPS", superclasses = webConnector)
http2 = CStereotype("HTTP/2", superclasses = webConnector)

linkedToMiddlewareHandler = CStereotype("Linked to Middleware Handler", superclasses = connector_type,
                                        attributes = {"handler": str})

_all = CBundle("_all",
               elements =component.get_connected_elements(add_stereotypes = True) + connector_type.get_connected_elements(add_stereotypes = True))

componentStereotypes = CBundle("Component Stereotypes", elements = component_type.get_connected_elements(add_stereotypes = True))
connectorStereotypes = CBundle("Connector Stereotypes", elements =[component] + connector_type.get_connected_elements(add_stereotypes = True))

componentMetamodelViews = [
    _all, {},
    componentStereotypes, {},
    connectorStereotypes, {}]
