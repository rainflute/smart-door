import json
#import door


class ShadowCallbackContainer:
    def __init__(self, client):
        self.client = client

    def call_back_delta(self, payload, responseStatus, token):
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"])
        deltaMessage = self.handle(deltaMessage)
        newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        self.client.shadowUpdate(newPayload, None, 5)

    def handle(self, deltaMessage):
        try:
            if deltaMessage == 'open':
                # door.open()
                print('open')
            elif deltaMessage == 'lock':
                # door.lock()
                print('closed')
            return deltaMessage
        except RuntimeError:
            if deltaMessage == 'open':
                return 'lock'
            elif deltaMessage == 'lock':
                return 'open'

    def initializeDoor(self, payload):
        payloadDict = json.loads(payload)
        status = json.dumps(payloadDict["state"]['reported']['status'])
        status = self.handle(status)
        newPayload = '{"state":{"reported":' + status + '}}'
        self.client.shadowUpdate(newPayload, None, 5)
