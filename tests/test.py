import unittest
from unittest import mock

from pymys import mysensors as mys


class TestGateway(unittest.TestCase):
    def setUp(self):
        self.gw = mys.Gateway()

    def testChangeProtocolVersion(self):
        self.gw.protocol_version = 1.4
        self.assertEqual(self.gw.protocol_version, 1.4)
        self.assertIs(self.gw.const, mys.mys_14)

        self.gw.protocol_version = 1.6
        self.assertEqual(self.gw.protocol_version, 1.6)
        self.assertIs(self.gw.const, mys.mys_16)

    def testAcessNotPresentNode(self):
        pass

    def testNotSupportedProtocol(self):
        pass

    def testNotSupportedMessageType(self):
        pass

    def testNotSupportedSubtype(self):
        pass

    def testGetFreeId(self):
        self.gw.nodes = {1: mys.Node(1), 2: mys.Node(2), 4: mys.Node(4), 10: mys.Node(10)}
        self.assertEqual(self.gw.get_free_id(), 3)

    def testNoneFreeId(self):
        self.gw.nodes = {i: mys.Node(i) for i in range(1,255)}
        with self.assertRaises(IndexError):
            self.gw.get_free_id()


class TestSerialGateway(unittest.TestCase):
    def setUp(self):
        port = "/dev/ttyUSB0"
        self.gw = mys.SerialGateway(port)

    @mock.patch('serial.Serial')
    def testConnectionSucess(self, mock_readline):
        msg_1 = b"0;0;3;0;9;gateway started, id=0, parent=0, distance=0"
        msg_2 = b"0;0;3;0;14;Gateway startup complete."
        msg_3 = b"0;0;3;0;2;1.6"
        mock_readline.return_value.readline.side_effect = [msg_1, msg_2, msg_3]

        self.assertTrue(self.gw.connect())
        self.assertIsInstance(self.gw.serial, mock.MagicMock)
        self.assertEqual(self.gw.protocol_version, 1.6)

    @mock.patch('serial.Serial')
    def testGatewayFailure(self, mock_readline):
        msg_1 = b""
        mock_readline.return_value.readline.side_effect = [msg_1]
        with self.assertRaises(mys.GatewayError):
            self.gw.connect()


class TestNode(unittest.TestCase):
    pass


class TestMessage(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
