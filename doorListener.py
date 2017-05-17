from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os
import json
import door


class ShadowCallbackContainer:
    def __init__(self, client):
        self.client = client
        self.currentStatus = ''

    def call_back_delta(self, payload, responseStatus, token):
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"]['status'])
        deltaMessage = self.handle(deltaMessage)
        newPayload = '{"state":{"reported":{"status":' + deltaMessage + '}}}'
        self.client.shadowUpdate(newPayload, None, 5)

    def handle(self, deltaMessage):
        try:
            if deltaMessage == '"open"':
                # door.open()
                print('Door Opened')
                self.currentStatus = '"open"'
            elif deltaMessage == '"lock"':
                # door.lock()
                print('Door Locked')
                self.currentStatus = '"lock"'
            else:
                raise RuntimeError('Wrong action')
            return self.currentStatus
        except RuntimeError:
            return self.currentStatus

    def initializeDoor(self, payload, responseStatus, token):
        payloadDict = json.loads(payload)
        status = json.dumps(payloadDict["state"]['reported']['status'])
        self.currentStatus = status
        status = self.handle(status)
        newPayload = '{"state":{"reported":{"status":' + status + '}}}'
        self.client.shadowUpdate(newPayload, None, 5)
        print('initialized!')

def customCallback(client, userdata, message):
    deltaMessage = message.payload
    if deltaMessage == 'open':
        # door.open()
        print('Door Opened')

    elif deltaMessage == 'lock':
        # door.lock()
        print('Door Locked')


host = "a108by5cx6oj8b.iot.us-west-2.amazonaws.com"
keyPath = os.path.dirname(os.path.abspath(__file__)) + '/../keys'
rootCAPath = keyPath + '/root-CA.crt'
privateKeyPath = keyPath + '/door.private.key'
certificatePath = keyPath + '/door.cert.pem'

myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("door/status", 1, customCallback)

# Loop forever
while True:
    pass
