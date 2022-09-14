import unittest
import os
from CommonModule import *


class TestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = read_config()
        cls.url = config.get("Information", "xml_source_path")
        cls.csv_path = config.get("Information", "csv_path")
        cls.download_path = config.get("Information", "xml_download_path")

    def setUp(self):
        self.xmlpath = os.path.join(os.getcwd(), TestMethods.download_path)
        self.csvpath = os.path.join(os.getcwd(), TestMethods.csv_path)

    def test_download_xml(self):
        self.assertEqual(
            download_xml(TestMethods.url, self.xmlpath, "source.xml"),
            self.xmlpath + os.sep + "source.xml",
        )

        self.assertEqual(
            download_xml(
                TestMethods.url,
                os.path.join(os.getcwd(), "diffpath"),
                "source.xml",
            ),
            os.path.join(os.getcwd(), "diffpath") + os.sep + "source.xml",
        )


if __name__ == "__main__":
    unittest.main()

