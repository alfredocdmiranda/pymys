import unittest
from unittest import mock

from mysensors import mysensors as mys


class TestSerialGateway(unittest.TestCase):
    def setUp(self):
        port = "/dev/ttyUSB0"
        self.gw = mys.SerialGateway(port)

    @mock.patch('serial.Serial')
    def testConnectionSucess(self, mock_readline):
        msg_1 = b"0;0;3;0;9;gateway started, id=0, parent=0, distance=0"
        msg_2 = b"0;0;3;0;14;Gateway startup complete."
        msg_3 = b"0;0;3;0;2;1.5"
        mock_readline.return_value.readline.side_effect = [msg_1, msg_2, msg_3]

        self.assertTrue(self.gw.connect())
        self.assertIsInstance(self.gw.serial, mock.MagicMock)
        self.assertEqual(self.gw.protocol_version, "1.5")

    @mock.patch('serial.Serial')
    def testConnectionFailure(self, mock_readline):
        msg_1 = b""
        mock_readline.return_value.readline.side_effect = [msg_1]

        with self.assertRaises(ValueError):
            self.gw.connect()

if __name__ == '__main__':
    unittest.main()
