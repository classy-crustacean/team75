import yaml

def getConfig(BP, file = 'config.yml'):
    BPPorts = {'A': BP.PORT_A,
               'B': BP.PORT_B,
               'C': BP.PORT_C,
               'D': BP.PORT_D,
               '1': BP.PORT_1,
               '2': BP.PORT_2,
               '3': BP.PORT_3,
               '4': BP.PORT_4}
    with open(file ,'r') as stream:
        ports = yaml.safe_load(stream)
    ports['right drive motor'] =  BPPorts[ports['right drive motor']]
    ports['left drive motor'] =  BPPorts[ports['left drive motor']]
    ports['front drive motor'] =  BPPorts[ports['front drive motor']]
    ports['latch motor'] =  BPPorts[ports['latch motor']]
    ports['touch sensor'] = BPPorts[str(ports['touch sensor'])]
    ports['hall effect sensor'] = BPPorts[str(ports['hall effect sensor'])]
    ports['ultrasonic sensor'] = BPPorts[str(ports['ultrasonic sensor'])]
    return ports
