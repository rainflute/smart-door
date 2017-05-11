from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
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
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
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
        newPayload = '{"state":{"reported":' + status + '}}'
        self.client.shadowUpdate(newPayload, None, 5)
        print('initialized!')
host = "a108by5cx6oj8b.iot.us-west-2.amazonaws.com"
keyPath = os.path.dirname(os.path.abspath(__file__)) + '/../keys'
rootCAPath = keyPath + '/root-CA.crt'
privateKeyPath = keyPath + '/door.private.key'
certificatePath = keyPath + '/door.cert.pem'

myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("door")
myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("door", True)

callbackContainer = ShadowCallbackContainer(Bot)
# Initialize door
Bot.shadowGet(callbackContainer.initializeDoor, 5)
# Listen on deltas
Bot.shadowRegisterDeltaCallback(callbackContainer.call_back_delta)

# Loop forever
while True:
    pass
