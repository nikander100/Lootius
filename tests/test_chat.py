import unittest
from lootius.modules.logParser import LogLine, parseLogLine

#run tests using py -m unittest c:/Users/ndvds/Documents/GitHub/Lootius/tests/test_chat.py

class TestLogParsing(unittest.TestCase):
    def _internal(self, line, expected):
        testLogLine = parseLogLine(line)
        print(testLogLine)
        self.assertEqual(testLogLine, expected)

    def testParseSystemMessage(self):
        msg = "2021-09-21 09:42:35 [System] [] Critical hit - Additional damage! You inflicted 519.1 points of damage"
        expected = LogLine(
            "2021-09-21 09:42:35",
            "System",
            "",
            "Critical hit - Additional damage! You inflicted 519.1 points of damage"
        )
        self._internal(msg, expected)

    def testParseGlobalMessage(self):
        msg = "2021-09-21 09:46:31 [Globals] [] Nanashana Nana Itsanai killed a creature " \
              "(Desert Crawler Provider) with a value of 416 PED!"
        expected = LogLine(
            "2021-09-21 09:46:31",
            "Globals",
            "",
            "Nanashana Nana Itsanai killed a creature (Desert Crawler Provider) with a value of 416 PED!"
        )
        self._internal(msg, expected)

    def testParseSystemHealMessage(self):
        msg = "2022-07-08 02:16:04 [System] [] You healed yourself 24.0 points"
        expected = LogLine(
            "2022-07-08 02:16:04",
            "System",
            "",
            "You healed yourself 24.0 points"
        )
        self._internal(msg, expected)

    def testParseSystemEnhancerMessage(self):
        msg = "2023-03-30 23:55:18 [System] [] Your enhancer Weapon Skill Modification Enhancer 1 on your Herman ASI TEN Edition broke. You have 27 enhancers remaining on the item. You received 0.6000 PED Shrapnel."
        expected = LogLine(
            "2023-03-30 23:55:18",
            "System",
            "",
            "Your enhancer Weapon Skill Modification Enhancer 1 on your Herman ASI TEN Edition broke. You have 27 enhancers remaining on the item. You received 0.6000 PED Shrapnel."
        )
        self._internal(msg, expected)

if __name__ == '__main__':
    unittest.main()
