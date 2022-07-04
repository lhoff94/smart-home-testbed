from marvis import ArgumentParser, Network, DockerNode,SwitchNode, Scenario, SimulationServer


def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")
    net.block_ip_address("10.0.0.1")

    bridge = SwitchNode('br-1')

    hass = DockerNode(
        'hass',
        docker_image='ghcr.io/home-assistant/home-assistant:stable',
        volumes={'/home/lhoff/masterarbeit/smart-home-testbed/docker/hass/config': {'bind': '/config', 'mode': 'rw'}},
        exposed_ports={'8123':'8123'}
    )
    channel_sub = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_sub.connect(hass)
    channel_sub.connect(bridge)

    mosquittoserver = DockerNode('mosquittoserver', docker_build_dir='./docker/mosquitto')
    channel_server = net.create_channel(data_rate="1000Mbps")
    channel_server.connect(mosquittoserver)
    channel_server.connect(bridge)

    mpymqttclient = DockerNode('mpymqttclient', docker_build_dir='./docker/micropython/mpy-client')
    channel_client = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_client.connect(mpymqttclient)
    channel_client.connect(bridge)

    bash = DockerNode('bash-attach', docker_build_dir='./docker/bash-attach')
    channel_sub = net.create_channel(delay="50ms", data_rate="100Mbps")
    channel_sub.connect(bash)
    channel_sub.connect(bridge)

    scenario.add_network(net)
    driver = SimulationServer(8080)
    scenario.add_simulation_driver(driver)


    with scenario as sim:
        # To simulate forever, do not specify the simulation_time parameter.
        sim.simulate()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
