from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    bridge = SwitchNode('br-1')

    fail = DockerNode('fail', docker_build_dir='./docker/fail')
    channel_sub = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_sub.connect(fail)
    channel_sub.connect(bridge)

    scenario.add_network(net)

    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate(simulation_time=60)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
