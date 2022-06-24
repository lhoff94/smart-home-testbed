from marvis import ArgumentParser, Network, DockerNode, InterfaceNode, SSHNode, SwitchNode, Scenario
#from pycrunch_trace.client.api import trace


#@trace
def main():
    #tracer = trace()
    #tracer.start('recording_name')
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    bridge = SwitchNode('br-1')

    mosquittoserver = DockerNode('mosquittoserver', docker_build_dir='./docker/mosquitto')
    channel_server = net.create_channel(data_rate="1000Mbps")
    channel_server.connect(mosquittoserver)
    channel_server.connect(bridge)
    
    
    mqttclient = DockerNode('mqttclient', docker_build_dir='./docker/mqtt-client')
    channel_client = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_client.connect(mqttclient)
    channel_client.connect(bridge)


    mqttsubscriber = DockerNode('mqttsubscriber', docker_build_dir='./docker/mqtt-subscriber')
    channel_sub = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_sub.connect(mqttsubscriber)
    channel_sub.connect(bridge)

    externalnode = InterfaceNode('externalNode','enp8s0')
    channel_ext = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_ext.connect(externalnode)
    channel_ext.connect(bridge)


    bash = DockerNode('bash-attach', docker_build_dir='./docker/bash-attach')
    channel_bash = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_bash.connect(bash)
    channel_bash.connect(bridge)

    #raspi = SSHNode('raspi', ip='192.168.178.200', username='pi', password='pi-passwd')
    #channel_bash = net.create_channel(delay="50ms", data_rate="100Mbps")
    #channel_bash.connect(raspi)
    #channel_bash.connect(bridge)


    scenario.add_network(net)

    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate()
    #tracer.stop()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
