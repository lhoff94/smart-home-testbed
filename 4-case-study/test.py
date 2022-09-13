from fabric import Connection
c = Connection('raspi', 'pi', connect_kwargs={"password": "pi-passwd",})
c.run('mkdir /tmp/marvis/')
c.put('servicenode/tasks.py', '/tmp/marvis/tasks.py')
c.put('servicenode/mhz19-mock', '/tmp/marvis/mhz19-mock')