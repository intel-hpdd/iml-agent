import os

import chroma_agent.device_plugins.audit
from chroma_agent.device_plugins.audit.local import LocalAudit
from chroma_agent.device_plugins.audit.node import NodeAudit
from chroma_agent.device_plugins.audit.lustre import LnetAudit, MdtAudit, MgsAudit

from tests.test_utils import PatchedContextTestCase
from tests.test_utils import patch_run


class TestAuditScanner(PatchedContextTestCase):
    def setUp(self):
        tests = os.path.join(os.path.dirname(__file__), '..')
        self.test_root = os.path.join(tests, "data/lustre_versions/2.0.66/mds_mgs")
        super(TestAuditScanner, self).setUp()

    def test_audit_scanner(self):
        """chroma_agent.device_plugins.audit.local_audit_classes() should return a list of classes."""
        list = [cls for cls in
                chroma_agent.device_plugins.audit.local_audit_classes()]
        self.assertEqual(list, [LnetAudit, MdtAudit, MgsAudit, NodeAudit])


class TestLocalAudit(PatchedContextTestCase):
    def setUp(self):
        tests = os.path.join(os.path.dirname(__file__), '..')
        self.test_root = os.path.join(tests, "data/lustre_versions/2.0.66/mds_mgs")
        super(TestLocalAudit, self).setUp()
        self.audit = LocalAudit()

    def test_localaudit_audit_classes(self):
        """LocalAudit.audit_classes() should return a list of classes."""
        self.assertEqual(self.audit.audit_classes(), [LnetAudit, MdtAudit, MgsAudit, NodeAudit])

    def test_properties(self):
        with patch_run(['which', 'zfs'], 0, "/sbin/zfs", ""):
            self.assertEqual(self.audit.properties(), {'zfs_installed': True})

        with patch_run(['which', 'zfs'], 1, "", "which: no zfs in (/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin)"):
            self.assertEqual(self.audit.properties(), {'zfs_installed': False})
