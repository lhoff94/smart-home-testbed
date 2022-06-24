import os

from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    bridge = SwitchNode('br-1')

    zigbee_data_directory = '/home/lhoff/masterarbeit/smart-home-testbed/docker/zigbee2mqtt/data'
    print(zigbee_data_directory)
    print(os.path.dirname(os.path.realpath(__file__)))
    zigbee2mqtt = DockerNode('zigbee2mqtt', docker_image='koenkk/zigbee2mqtt', volumes={zigbee_data_directory:{'bind':'/app/data','mode':'rw'},'/run/udev':{'bind':'/run/udev','mode':'ro'}} , devices="/dev/ttyUSB0:/dev/ttyUSB0", exposed_ports={'8080':'8080'})
    channel_server = net.create_channel(data_rate="1000Mbps")
    channel_server.connect(zigbee2mqtt)
    channel_server.connect(bridge)

    scenario.add_network(net)

    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
