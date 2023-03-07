import re
import enum
import tailer
import threading
from decimal import Decimal
from datetime import datetime
from collections import namedtuple
import win_unicode_console

win_unicode_console.enable()


class ChatType(str, enum.Enum):
    HEAL = "heal"
    COMBAT = "combat"
    SKILL = "skill"
    DEATH = "death"
    EVADE = "evade"
    DAMAGE = "damage"
    DEFLECT = "deflect"
    DODGE = "dodge"
    ENHANCER = "enhancer"
    LOOT = "loot"
    GLOBAL = "global"

class BaseChatRow(object):
    def __init__(self, *args, **kwargs):
        self.time = None

class HealRow(BaseChatRow):
    def __init__(self, amount=0.0, diminished=False):
        super().__init__()
        self.amount = float(amount) if amount else 0.0
        self.diminished = diminished

class CombatRow(BaseChatRow):
    def __init__(self, amount=0.0, critical=False, miss=False):
        super.__init__()
        self.amount = float(amount) if amount else 0.0
        self.critical = critical
        self.miss = miss

class SkillRow(BaseChatRow):
    def __init__(self, amount, skill):
        super().__init__()
        try:
            self.amount = float(amount)
            self.skill = skill
        except ValueError:
            # Attributes have their values swapped around in the chat message sometimes.
            self.amount = float(skill)
            self.skill = amount

class EnhancerRow(BaseChatRow):
    def __init__(self, type):
        super().__init__()
        self.type = type

class LootRow(BaseChatRow):
    CustomValues = {
        "Shrapnel" : Decimal("0.0001")
    }
    def __init__(self, name, amount, value):
        super().__init__()
        self.name = name
        self.amount = int(amount)
        if name in self.CustomValues:
            self.value = Decimal(amount) * self.CustomValues[name]
        else:
            self.value = Decimal(value)    

class GlobalRow(BaseChatRow):
    #add discovery/ath/tier?
    def __init__(self, name, creature, value, location=None, hof=False):
        super().__init__()
        self.name = name
        self.creature = creature
        self.value = value
        self.hof = hof
        self.location = location

LogLineRegex = re.compile(r"([\d\-]+ [\d:]+) \[(\w+)\] \[(.*)\] (.*)")
LogLine = namedtuple("LogLine", ["time", "channel", "speaker", "msg"])

"""parses raw logline into a namedtuple for easier manipulation."""
def parseLogLine(line: str) -> LogLine:
    matchedLine = LogLineRegex.match(line)
    if not matchedLine:
        return LogLine("", "", "", "")
    return LogLine(*matchedLine.groups())

Regexes = {
    re.compile("Critical hit - Additional damage! You inflicted (\d+\.\d+) points of damage"): (ChatType.DAMAGE, CombatRow, {"critical": True}),
    re.compile("You inflicted (\d+\.\d+) points of damage"): (ChatType.DAMAGE, CombatRow, {}),
    re.compile("Healing is diminished while moving"): (ChatType.HEAL, HealRow, {"diminished": True}),
    re.compile("You healed yourself (\d+\.\d+) points"): (ChatType.HEAL, HealRow, {}),
    re.compile("Damage deflected!"): (ChatType.DEFLECT, BaseChatRow, {}),
    re.compile("You Evaded the attack"): (ChatType.EVADE, BaseChatRow, {}),
    re.compile("You missed"): (ChatType.DODGE, CombatRow, {"miss": True}),
    re.compile("The target Dodged your attack"): (ChatType.DODGE, CombatRow, {"miss": True}),
    re.compile("The target Evaded your attack"): (ChatType.DODGE, CombatRow, {"miss": True}),
    re.compile("The target Jammed your attack"): (ChatType.DODGE, CombatRow, {"miss": True}),
    re.compile("You took (\d+\.\d+) points of damage"): (ChatType.DAMAGE, BaseChatRow, {}),
    re.compile("You have gained (\d+\.\d+) experience in your ([a-zA-Z ]+) skill"): (ChatType.SKILL, SkillRow, {}),
    re.compile("You have gained (\d+\.\d+) ([a-zA-Z ]+)"): (ChatType.SKILL, SkillRow, {}),
    re.compile("Your ([a-zA-Z ]+) has improved by (\d+\.\d+)"): (ChatType.SKILL, SkillRow, {}),
    re.compile("Your enhancer ([a-zA-Z0-9 ]+) on your .* broke."): (ChatType.ENHANCER, EnhancerRow, {}),
    re.compile(r"You received (.*) x \((\d+)\) Value: (\d+\.\d+) PED"): (ChatType.LOOT, LootRow, {}),
}
GlobalRegexes = {
    re.compile(r"([\w\s\'\(\)]+) killed a creature \(([\w\s\(\)]+)\) with a value of (\d+) PED! A record has been added to the Hall of Fame!"): (ChatType.GLOBAL, GlobalRow, {"hof": True}),
    re.compile(r"([\w\s\'\(\)]+) killed a creature \(([\w\s\(\)]+)\) with a value of (\d+) PED!"): (ChatType.GLOBAL, GlobalRow, {}),
    re.compile(r"([\w\s\'\(\)]+) constructed an item \(([\w\s\(\)]+)\) worth (\d+) PED! A record has been added to the Hall of Fame!"): (ChatType.GLOBAL, GlobalRow, {"hof": True}),
    re.compile(r"([\w\s\'\(\)]+) constructed an item \(([\w\s\(\)]+)\) worth (\d+) PED!"): (ChatType.GLOBAL, GlobalRow, {}),
    re.compile(r"([\w\s\'\(\)]+) found a deposit \(([\w\s\(\)]+)\) with a value of (\d+) PED! A record has been added to the Hall of Fame!"): (ChatType.GLOBAL, GlobalRow, {"hof": True}),
    re.compile(r"([\w\s\'\(\)]+) found a deposit \(([\w\s\(\)]+)\) with a value of (\d+) PED!"): (ChatType.GLOBAL, GlobalRow, {}),
    re.compile(r"([\w\s\'\(\)]+) killed a creature \(([\w\s\(\)]+)\) with a value of (\d+) PED at ([\s\w\W]+)!"): (ChatType.GLOBAL, GlobalRow, {}),
    # re.compile(r"([\w\s\(\)]+) examined (newRegexHere) and found something with a value of (\d+) PED! A record has been added to the Hall of Fame!"): (ChatType.GLOBAL, GlobalRow, {"hof": True}),
    # re.compile(r"([\w\s\(\)]+) examined (newRegexHere) and found something with a value of (\d+) PED!"): (ChatType.GLOBAL, GlobalRow, {}),
}

class ChatLogParser(object):
    def __init__(self, app):
        self.app = app
        self.lines = []
        self.reader = None
    
    def delayStartLogger(self):
        if self.reader:
            return
    
        self.fd = tailer.follow(open("C:/Users/ndvds/Documents/Entropia Universe/chat.log"), "r", encoding="utf_8_sig", delay=0.01)
        self.reader = threading.Thread(target=self.readLogLines, daemon=True)
        self.reader.start()

    def readLogLines(self):
        try:
            for line in self.fd:
                logLine = parseLogLine(line)
                if logLine.channel == "System":
                    matched = False
                    for rx in Regexes:
                        match = rx.search(logLine.msg)
                        if match:
                            chatType, chatCls, kwargs = Regexes[rx]
                            chatInstance: BaseChatRow = chatCls(*match.groups(), **kwargs)
                            chatInstance.time = datetime.strptime(logLine.time, "%Y-%m-%d %H:%M:%S")
                            self.lines.append(chatInstance)
                            matched = True
                            break
                    if not matched:
                        print([logLine.msg])
                elif logLine.channel == "Globals":
                    matched = False
                    for rx in GlobalRegexes:
                        match = rx.search(logLine.msg)
                        if match:
                            chatType, chatCls, kwargs = GlobalRegexes[rx]
                            chatInstance: GlobalRow = chatCls(*match.groups(), **kwargs)
                            chatInstance.time = datetime.strptime(logLine.time, "%Y-%m-%d %H:%M:%S")
                            self.lines.append(chatInstance)
                            matched = True
                            break
        except UnicodeDecodeError:
            pass
    
    def getline(self):
        if len(self.lines):
            return self.lines.pop(0)
        return None