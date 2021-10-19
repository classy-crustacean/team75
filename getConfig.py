import yaml

portsFile = "ports.yml"

def getPorts(BP):
    BPPorts = {'A': BP.PORT_A,
               'B': BP.PORT_B,
               'C': BP.PORT_C,
               'D': BP.PORT_D,
               '1': BP.PORT_1,
               '2': BP.PORT_2,
               '3': BP.PORT_3,
               '4': BP.PORT_4}
    with open(portsFile,'r') as stream:
        ports = yaml.safe_load(stream)
    ports['right drive motor'] =  BPPorts[ports['right drive motor']]
    ports['left drive motor'] =  BPPorts[ports['left drive motor']]
    ports['latch motor'] =  BPPorts[ports['latch motor']]
    ports['cable motor'] =  BPPorts[ports['cable motor']]
    ports['touch'] = BPPorts[str(ports['touch'])]
    return ports
