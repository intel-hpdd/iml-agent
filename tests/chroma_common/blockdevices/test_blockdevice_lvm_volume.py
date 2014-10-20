from chroma_agent.chroma_common.blockdevices.blockdevice_lvm_volume import BlockDeviceLvmVolume
from tests.command_capture_testcase import CommandCaptureTestCase


class TestBlockDeviceLvmVolume(CommandCaptureTestCase):
    def setUp(self):
        super(TestBlockDeviceLvmVolume, self).setUp()

        self.blockdevice = BlockDeviceLvmVolume('lvm_volume', '/dev/mappper/lvg-test-lvm-test')

    def test_uuid(self):
        self.results = {
            ("lvs", "--noheadings", "-o", "lv_uuid", '/dev/mappper/lvg-test-lvm-test'): (0, '  CtSfyh-ThdO-Bg3i-EiKU-6knJ-Ix4D-ru49Py\n', 0)}

        self.assertEqual('CtSfyh-ThdO-Bg3i-EiKU-6knJ-Ix4D-ru49Py', self.blockdevice.uuid)
