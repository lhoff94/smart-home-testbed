from marvis import ArgumentParser, Scenario, Network, SwitchNode, DockerNode, SSHNode


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.set_delay(delay="200ms")

    node1 = DockerNode('pong', docker_build_dir='./docker/pong')
    node2 = SwitchNode('bridge-1')
    node3 = SSHNode('ping', ip='192.168.178.200', username='pi', password='pi-passwd')

    channel1 = net.create_channel("channel1")
    channel1.connect(node1)
    channel1.connect(node2)
    channel2 = net.create_channel("channel2")
    channel2.connect(node2)
    channel2.connect(node3)

    scenario.add_network(net)
    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate(simulation_time=60)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
