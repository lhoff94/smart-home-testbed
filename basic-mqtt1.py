from marvis import ArgumentParser, Network, DockerNode, Scenario


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    node1 = DockerNode('mosquitto_server', docker_build_dir='./docker/mosquitto')
    node2 = DockerNode('mqtt_client', docker_build_dir='./docker/mqtt-client')
    node3 = DockerNode('mqtt_subscriber', docker_build_dir='./docker/mqtt-subscriber')
    
    channel = net.create_channel(delay="50ms")
    channel.connect(node1)
    channel.connect(node2)
    channel.connect(node3)

    scenario.add_network(net)

    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate(simulation_time=60)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
