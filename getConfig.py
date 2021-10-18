import yaml

portsFile = "ports.yml"

def getPorts(BP):
    BPPorts = {'A': BP.Port_A,
               'B': BP.Port_B,
               'C': BP.Port_C,
               'D': BP.Port_D,
               '1': BP.Port_1,
               '2': BP.Port_2,
               '3': BP.Port_3,
               '4': BP.Port_4}
    with open(portsFile,'r') as stream:
        ports = yaml.safe_load(stream)
    ports['right drive motor'] =  BPPorts[ports['right drive motor']]
    ports['left drive motor'] =  BPPorts[ports['left drive motor']]
    ports['latch motor'] =  BPPorts[ports['latch motor']]
    ports['cable motor'] =  BPPorts[ports['cable motor']]
    ports['touch'] = BPPorts[ports['touch']]
    return ports
