pyMYS
=======

It is a module to make easier communication with MySensor's network.

Documentation
=============

Currently, all documentation can be accessed in project's GitHub page.

Dependencies
============

You can find all dependencies in requirements.txt and
install them using pip.

Installation
============

    python setup.py install

or

    pip pymys

Support
=======

This project should support all Python 3 versions. However, it was onlye tested with Python 3.4.

Examples
========

If you just want to print all messages that your Gateway send to you.

::

    from pymys import mysensors as mys


    def show_msg(msg):
        print(msg)

    gw = mys.SerialGateway("/dev/ttyACM0", message_callback=show_msg)
    print("Trying to connect...")
    gw.connect()
    print("Connected!")

    while True:
        gw.process()

Creating an application with threads which allow you write raw messages and send to your network over your Gateway

::

    import threading

    from pymys import mysensors as mys


    def run_gateway():
        while True:
            gw.process()


    def show_msg(msg):
        print("Read: {}".format(msg))

    gw = mys.SerialGateway("/dev/ttyACM0", message_callback=show_msg)
    print("Trying to connect...")
    gw.connect()
    print("Connected!")

    t = threading.Thread(target=run_gateway)
    t.start()

    while True:
        data = input("")
        msg = mys.Message(data)
        gw.send(msg)

What's new
===========
- Base structure for Gateway
- Support to Serial Gateway
- Support to protocol 1.4
- Support to protocol 1.5
- Support to protocol 1.6
- Support to change callback functions
- Support to get dinamically the protocol version from the Gateway
