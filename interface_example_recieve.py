from marvis import ArgumentParser, Network, DockerNode, InterfaceNode, Scenario


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0", base="0.0.0.2")
    net.block_ip_address("10.0.0.1")

    node1 = InterfaceNode('ping','enx000ec6fe5586')
    node2 = DockerNode('pong', docker_build_dir='./docker/pong')
    channel = net.create_channel(delay="200ms")
    channel.connect(node1)
    channel.connect(node2, "10.0.0.17")

    scenario.add_network(net)

    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
