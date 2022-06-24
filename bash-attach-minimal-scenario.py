from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario
import os

def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    bridge = SwitchNode('br-1')

    zigbee_data_directory = os.path.join(os.getcwd(),'docker/zigbee2mqtt/data')

    bash = DockerNode('bash-attach', devices="/dev/ttyUSB0:/dev/ttyACM0", volumes={zigbee_data_directory:{'bind':'/app/data','mode':'rw'},'/run/udev':{'bind':'/run/udev','mode':'ro'}}, docker_build_dir='./docker/bash-attach')
    channel_sub = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_sub.connect(bash)
    channel_sub.connect(bridge)

    scenario.add_network(net)

    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
