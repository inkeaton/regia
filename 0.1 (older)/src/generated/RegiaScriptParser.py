# Generated from grammars/RegiaScript.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,37,352,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,4,0,52,8,0,11,0,
        12,0,53,1,0,1,0,1,1,1,1,3,1,60,8,1,1,2,5,2,63,8,2,10,2,12,2,66,9,
        2,1,2,1,2,1,2,1,2,4,2,72,8,2,11,2,12,2,73,1,3,5,3,77,8,3,10,3,12,
        3,80,9,3,1,3,1,3,1,3,1,3,1,3,1,3,5,3,88,8,3,10,3,12,3,91,9,3,1,3,
        5,3,94,8,3,10,3,12,3,97,9,3,1,3,5,3,100,8,3,10,3,12,3,103,9,3,1,
        3,4,3,106,8,3,11,3,12,3,107,1,4,5,4,111,8,4,10,4,12,4,114,9,4,1,
        4,1,4,5,4,118,8,4,10,4,12,4,121,9,4,1,4,1,4,5,4,125,8,4,10,4,12,
        4,128,9,4,1,4,3,4,131,8,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,
        7,1,7,1,7,1,7,1,7,1,8,1,8,1,9,5,9,150,8,9,10,9,12,9,153,9,9,1,9,
        1,9,1,9,3,9,158,8,9,1,9,1,9,1,10,5,10,163,8,10,10,10,12,10,166,9,
        10,1,10,1,10,1,10,3,10,171,8,10,1,10,1,10,1,11,5,11,176,8,11,10,
        11,12,11,179,9,11,1,11,1,11,1,11,1,11,5,11,185,8,11,10,11,12,11,
        188,9,11,1,12,5,12,191,8,12,10,12,12,12,194,9,12,1,12,1,12,5,12,
        198,8,12,10,12,12,12,201,9,12,1,12,1,12,5,12,205,8,12,10,12,12,12,
        208,9,12,1,12,1,12,3,12,212,8,12,1,13,5,13,215,8,13,10,13,12,13,
        218,9,13,1,13,1,13,1,13,1,13,5,13,224,8,13,10,13,12,13,227,9,13,
        1,13,4,13,230,8,13,11,13,12,13,231,1,14,5,14,235,8,14,10,14,12,14,
        238,9,14,1,14,1,14,1,14,1,14,1,14,1,14,1,14,3,14,247,8,14,1,14,1,
        14,1,15,1,15,1,16,1,16,1,17,5,17,256,8,17,10,17,12,17,259,9,17,1,
        17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,5,17,269,8,17,10,17,12,17,
        272,9,17,1,17,1,17,1,17,1,17,4,17,278,8,17,11,17,12,17,279,1,17,
        5,17,283,8,17,10,17,12,17,286,9,17,1,17,1,17,1,17,1,17,3,17,292,
        8,17,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,3,18,302,8,18,1,19,
        1,19,1,19,5,19,307,8,19,10,19,12,19,310,9,19,1,20,1,20,1,20,5,20,
        315,8,20,10,20,12,20,318,9,20,1,21,3,21,321,8,21,1,21,1,21,1,22,
        1,22,1,22,1,22,1,22,3,22,330,8,22,1,23,1,23,1,23,5,23,335,8,23,10,
        23,12,23,338,9,23,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,24,1,24,1,
        24,3,24,350,8,24,1,24,0,0,25,0,2,4,6,8,10,12,14,16,18,20,22,24,26,
        28,30,32,34,36,38,40,42,44,46,48,0,3,1,0,18,22,2,0,25,25,34,34,2,
        0,1,1,34,34,371,0,51,1,0,0,0,2,59,1,0,0,0,4,64,1,0,0,0,6,78,1,0,
        0,0,8,130,1,0,0,0,10,132,1,0,0,0,12,136,1,0,0,0,14,141,1,0,0,0,16,
        146,1,0,0,0,18,151,1,0,0,0,20,164,1,0,0,0,22,177,1,0,0,0,24,211,
        1,0,0,0,26,216,1,0,0,0,28,236,1,0,0,0,30,250,1,0,0,0,32,252,1,0,
        0,0,34,291,1,0,0,0,36,301,1,0,0,0,38,303,1,0,0,0,40,311,1,0,0,0,
        42,320,1,0,0,0,44,329,1,0,0,0,46,331,1,0,0,0,48,349,1,0,0,0,50,52,
        3,2,1,0,51,50,1,0,0,0,52,53,1,0,0,0,53,51,1,0,0,0,53,54,1,0,0,0,
        54,55,1,0,0,0,55,56,5,0,0,1,56,1,1,0,0,0,57,60,3,4,2,0,58,60,3,6,
        3,0,59,57,1,0,0,0,59,58,1,0,0,0,60,3,1,0,0,0,61,63,5,35,0,0,62,61,
        1,0,0,0,63,66,1,0,0,0,64,62,1,0,0,0,64,65,1,0,0,0,65,67,1,0,0,0,
        66,64,1,0,0,0,67,68,5,1,0,0,68,69,5,2,0,0,69,71,5,28,0,0,70,72,3,
        22,11,0,71,70,1,0,0,0,72,73,1,0,0,0,73,71,1,0,0,0,73,74,1,0,0,0,
        74,5,1,0,0,0,75,77,5,35,0,0,76,75,1,0,0,0,77,80,1,0,0,0,78,76,1,
        0,0,0,78,79,1,0,0,0,79,81,1,0,0,0,80,78,1,0,0,0,81,82,5,1,0,0,82,
        83,5,34,0,0,83,84,5,3,0,0,84,85,5,33,0,0,85,89,5,28,0,0,86,88,3,
        8,4,0,87,86,1,0,0,0,88,91,1,0,0,0,89,87,1,0,0,0,89,90,1,0,0,0,90,
        95,1,0,0,0,91,89,1,0,0,0,92,94,3,18,9,0,93,92,1,0,0,0,94,97,1,0,
        0,0,95,93,1,0,0,0,95,96,1,0,0,0,96,101,1,0,0,0,97,95,1,0,0,0,98,
        100,3,20,10,0,99,98,1,0,0,0,100,103,1,0,0,0,101,99,1,0,0,0,101,102,
        1,0,0,0,102,105,1,0,0,0,103,101,1,0,0,0,104,106,3,26,13,0,105,104,
        1,0,0,0,106,107,1,0,0,0,107,105,1,0,0,0,107,108,1,0,0,0,108,7,1,
        0,0,0,109,111,5,35,0,0,110,109,1,0,0,0,111,114,1,0,0,0,112,110,1,
        0,0,0,112,113,1,0,0,0,113,115,1,0,0,0,114,112,1,0,0,0,115,131,3,
        10,5,0,116,118,5,35,0,0,117,116,1,0,0,0,118,121,1,0,0,0,119,117,
        1,0,0,0,119,120,1,0,0,0,120,122,1,0,0,0,121,119,1,0,0,0,122,131,
        3,12,6,0,123,125,5,35,0,0,124,123,1,0,0,0,125,128,1,0,0,0,126,124,
        1,0,0,0,126,127,1,0,0,0,127,129,1,0,0,0,128,126,1,0,0,0,129,131,
        3,14,7,0,130,112,1,0,0,0,130,119,1,0,0,0,130,126,1,0,0,0,131,9,1,
        0,0,0,132,133,5,6,0,0,133,134,5,34,0,0,134,135,5,28,0,0,135,11,1,
        0,0,0,136,137,5,7,0,0,137,138,5,34,0,0,138,139,3,16,8,0,139,140,
        5,28,0,0,140,13,1,0,0,0,141,142,5,8,0,0,142,143,5,34,0,0,143,144,
        3,16,8,0,144,145,5,28,0,0,145,15,1,0,0,0,146,147,7,0,0,0,147,17,
        1,0,0,0,148,150,5,35,0,0,149,148,1,0,0,0,150,153,1,0,0,0,151,149,
        1,0,0,0,151,152,1,0,0,0,152,154,1,0,0,0,153,151,1,0,0,0,154,155,
        5,4,0,0,155,157,5,34,0,0,156,158,5,26,0,0,157,156,1,0,0,0,157,158,
        1,0,0,0,158,159,1,0,0,0,159,160,5,28,0,0,160,19,1,0,0,0,161,163,
        5,35,0,0,162,161,1,0,0,0,163,166,1,0,0,0,164,162,1,0,0,0,164,165,
        1,0,0,0,165,167,1,0,0,0,166,164,1,0,0,0,167,168,5,5,0,0,168,170,
        5,34,0,0,169,171,5,21,0,0,170,169,1,0,0,0,170,171,1,0,0,0,171,172,
        1,0,0,0,172,173,5,28,0,0,173,21,1,0,0,0,174,176,5,35,0,0,175,174,
        1,0,0,0,176,179,1,0,0,0,177,175,1,0,0,0,177,178,1,0,0,0,178,180,
        1,0,0,0,179,177,1,0,0,0,180,181,5,5,0,0,181,182,5,34,0,0,182,186,
        5,29,0,0,183,185,3,24,12,0,184,183,1,0,0,0,185,188,1,0,0,0,186,184,
        1,0,0,0,186,187,1,0,0,0,187,23,1,0,0,0,188,186,1,0,0,0,189,191,5,
        35,0,0,190,189,1,0,0,0,191,194,1,0,0,0,192,190,1,0,0,0,192,193,1,
        0,0,0,193,195,1,0,0,0,194,192,1,0,0,0,195,212,3,10,5,0,196,198,5,
        35,0,0,197,196,1,0,0,0,198,201,1,0,0,0,199,197,1,0,0,0,199,200,1,
        0,0,0,200,202,1,0,0,0,201,199,1,0,0,0,202,212,3,12,6,0,203,205,5,
        35,0,0,204,203,1,0,0,0,205,208,1,0,0,0,206,204,1,0,0,0,206,207,1,
        0,0,0,207,209,1,0,0,0,208,206,1,0,0,0,209,212,3,14,7,0,210,212,3,
        34,17,0,211,192,1,0,0,0,211,199,1,0,0,0,211,206,1,0,0,0,211,210,
        1,0,0,0,212,25,1,0,0,0,213,215,5,35,0,0,214,213,1,0,0,0,215,218,
        1,0,0,0,216,214,1,0,0,0,216,217,1,0,0,0,217,219,1,0,0,0,218,216,
        1,0,0,0,219,220,5,9,0,0,220,221,3,32,16,0,221,225,5,29,0,0,222,224,
        3,28,14,0,223,222,1,0,0,0,224,227,1,0,0,0,225,223,1,0,0,0,225,226,
        1,0,0,0,226,229,1,0,0,0,227,225,1,0,0,0,228,230,3,22,11,0,229,228,
        1,0,0,0,230,231,1,0,0,0,231,229,1,0,0,0,231,232,1,0,0,0,232,27,1,
        0,0,0,233,235,5,35,0,0,234,233,1,0,0,0,235,238,1,0,0,0,236,234,1,
        0,0,0,236,237,1,0,0,0,237,239,1,0,0,0,238,236,1,0,0,0,239,240,5,
        23,0,0,240,241,5,24,0,0,241,242,3,30,15,0,242,243,5,10,0,0,243,246,
        5,34,0,0,244,245,5,11,0,0,245,247,3,38,19,0,246,244,1,0,0,0,246,
        247,1,0,0,0,247,248,1,0,0,0,248,249,5,28,0,0,249,29,1,0,0,0,250,
        251,7,1,0,0,251,31,1,0,0,0,252,253,7,2,0,0,253,33,1,0,0,0,254,256,
        5,35,0,0,255,254,1,0,0,0,256,259,1,0,0,0,257,255,1,0,0,0,257,258,
        1,0,0,0,258,260,1,0,0,0,259,257,1,0,0,0,260,261,5,10,0,0,261,262,
        5,34,0,0,262,263,5,11,0,0,263,264,3,38,19,0,264,265,5,29,0,0,265,
        266,3,46,23,0,266,292,1,0,0,0,267,269,5,35,0,0,268,267,1,0,0,0,269,
        272,1,0,0,0,270,268,1,0,0,0,270,271,1,0,0,0,271,273,1,0,0,0,272,
        270,1,0,0,0,273,274,5,10,0,0,274,275,5,34,0,0,275,277,5,29,0,0,276,
        278,3,36,18,0,277,276,1,0,0,0,278,279,1,0,0,0,279,277,1,0,0,0,279,
        280,1,0,0,0,280,292,1,0,0,0,281,283,5,35,0,0,282,281,1,0,0,0,283,
        286,1,0,0,0,284,282,1,0,0,0,284,285,1,0,0,0,285,287,1,0,0,0,286,
        284,1,0,0,0,287,288,5,10,0,0,288,289,5,34,0,0,289,290,5,29,0,0,290,
        292,3,46,23,0,291,257,1,0,0,0,291,270,1,0,0,0,291,284,1,0,0,0,292,
        35,1,0,0,0,293,294,5,11,0,0,294,295,3,38,19,0,295,296,5,29,0,0,296,
        297,3,46,23,0,297,302,1,0,0,0,298,299,5,27,0,0,299,300,5,29,0,0,
        300,302,3,46,23,0,301,293,1,0,0,0,301,298,1,0,0,0,302,37,1,0,0,0,
        303,308,3,40,20,0,304,305,5,13,0,0,305,307,3,40,20,0,306,304,1,0,
        0,0,307,310,1,0,0,0,308,306,1,0,0,0,308,309,1,0,0,0,309,39,1,0,0,
        0,310,308,1,0,0,0,311,316,3,42,21,0,312,313,5,12,0,0,313,315,3,42,
        21,0,314,312,1,0,0,0,315,318,1,0,0,0,316,314,1,0,0,0,316,317,1,0,
        0,0,317,41,1,0,0,0,318,316,1,0,0,0,319,321,5,14,0,0,320,319,1,0,
        0,0,320,321,1,0,0,0,321,322,1,0,0,0,322,323,3,44,22,0,323,43,1,0,
        0,0,324,330,5,34,0,0,325,326,5,31,0,0,326,327,3,38,19,0,327,328,
        5,32,0,0,328,330,1,0,0,0,329,324,1,0,0,0,329,325,1,0,0,0,330,45,
        1,0,0,0,331,336,3,48,24,0,332,333,5,30,0,0,333,335,3,48,24,0,334,
        332,1,0,0,0,335,338,1,0,0,0,336,334,1,0,0,0,336,337,1,0,0,0,337,
        339,1,0,0,0,338,336,1,0,0,0,339,340,5,28,0,0,340,47,1,0,0,0,341,
        342,5,15,0,0,342,343,5,16,0,0,343,350,5,34,0,0,344,345,5,15,0,0,
        345,346,5,17,0,0,346,350,5,34,0,0,347,348,5,15,0,0,348,350,5,34,
        0,0,349,341,1,0,0,0,349,344,1,0,0,0,349,347,1,0,0,0,350,49,1,0,0,
        0,40,53,59,64,73,78,89,95,101,107,112,119,126,130,151,157,164,170,
        177,186,192,199,206,211,216,225,231,236,246,257,270,279,284,291,
        301,308,316,320,329,336,349
    ]

class RegiaScriptParser ( Parser ):

    grammarFileName = "RegiaScript.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'STORY'", "'DEFAULT'", "'PRIORITY'", 
                     "'PHASE'", "'AGENT'", "'ACTION'", "'EVENT'", "'CONDITION'", 
                     "'DURING'", "'WHEN'", "'IF'", "'AND'", "'OR'", "'NOT'", 
                     "'DO'", "'BELIEVE'", "'FORGET'", "'ENVIRONMENT'", "'DIRECTOR'", 
                     "'MYSELF'", "'PLAYER'", "'TIMER'", "'TRANSITION'", 
                     "'TO'", "'END'", "'INITIAL'", "'OTHERWISE'", "'.'", 
                     "':'", "','", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "STORY", "DEFAULT", "PRIORITY", "PHASE", 
                      "AGENT", "ACTION", "EVENT", "CONDITION", "DURING", 
                      "WHEN", "IF", "AND", "OR", "NOT", "DO", "BELIEVE", 
                      "FORGET", "ENVIRONMENT", "DIRECTOR", "MYSELF", "PLAYER", 
                      "TIMER", "TRANSITION", "TO", "END", "INITIAL", "OTHERWISE", 
                      "PERIOD", "COLON", "COMMA", "LPAREN", "RPAREN", "NUMBER", 
                      "ID", "DOC_COMMENT", "COMMENT", "WS" ]

    RULE_program = 0
    RULE_storyDef = 1
    RULE_defaultStory = 2
    RULE_namedStory = 3
    RULE_declaration = 4
    RULE_actionDecl = 5
    RULE_eventDecl = 6
    RULE_conditionDecl = 7
    RULE_origin = 8
    RULE_phaseDecl = 9
    RULE_storyAgentDecl = 10
    RULE_agentBlock = 11
    RULE_agentSection = 12
    RULE_duringBlock = 13
    RULE_transitionRule = 14
    RULE_phaseTarget = 15
    RULE_phaseRef = 16
    RULE_whenBlock = 17
    RULE_ifBranch = 18
    RULE_condExpr = 19
    RULE_condAnd = 20
    RULE_condTerm = 21
    RULE_condAtom = 22
    RULE_doSequence = 23
    RULE_doAction = 24

    ruleNames =  [ "program", "storyDef", "defaultStory", "namedStory", 
                   "declaration", "actionDecl", "eventDecl", "conditionDecl", 
                   "origin", "phaseDecl", "storyAgentDecl", "agentBlock", 
                   "agentSection", "duringBlock", "transitionRule", "phaseTarget", 
                   "phaseRef", "whenBlock", "ifBranch", "condExpr", "condAnd", 
                   "condTerm", "condAtom", "doSequence", "doAction" ]

    EOF = Token.EOF
    STORY=1
    DEFAULT=2
    PRIORITY=3
    PHASE=4
    AGENT=5
    ACTION=6
    EVENT=7
    CONDITION=8
    DURING=9
    WHEN=10
    IF=11
    AND=12
    OR=13
    NOT=14
    DO=15
    BELIEVE=16
    FORGET=17
    ENVIRONMENT=18
    DIRECTOR=19
    MYSELF=20
    PLAYER=21
    TIMER=22
    TRANSITION=23
    TO=24
    END=25
    INITIAL=26
    OTHERWISE=27
    PERIOD=28
    COLON=29
    COMMA=30
    LPAREN=31
    RPAREN=32
    NUMBER=33
    ID=34
    DOC_COMMENT=35
    COMMENT=36
    WS=37

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(RegiaScriptParser.EOF, 0)

        def storyDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.StoryDefContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.StoryDefContext,i)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = RegiaScriptParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 50
                self.storyDef()
                self.state = 53 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==35):
                    break

            self.state = 55
            self.match(RegiaScriptParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StoryDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def defaultStory(self):
            return self.getTypedRuleContext(RegiaScriptParser.DefaultStoryContext,0)


        def namedStory(self):
            return self.getTypedRuleContext(RegiaScriptParser.NamedStoryContext,0)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_storyDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStoryDef" ):
                listener.enterStoryDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStoryDef" ):
                listener.exitStoryDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStoryDef" ):
                return visitor.visitStoryDef(self)
            else:
                return visitor.visitChildren(self)




    def storyDef(self):

        localctx = RegiaScriptParser.StoryDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_storyDef)
        try:
            self.state = 59
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.defaultStory()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 58
                self.namedStory()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefaultStoryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STORY(self):
            return self.getToken(RegiaScriptParser.STORY, 0)

        def DEFAULT(self):
            return self.getToken(RegiaScriptParser.DEFAULT, 0)

        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def agentBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.AgentBlockContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.AgentBlockContext,i)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_defaultStory

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefaultStory" ):
                listener.enterDefaultStory(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefaultStory" ):
                listener.exitDefaultStory(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDefaultStory" ):
                return visitor.visitDefaultStory(self)
            else:
                return visitor.visitChildren(self)




    def defaultStory(self):

        localctx = RegiaScriptParser.DefaultStoryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_defaultStory)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 61
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 66
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 67
            self.match(RegiaScriptParser.STORY)
            self.state = 68
            self.match(RegiaScriptParser.DEFAULT)
            self.state = 69
            self.match(RegiaScriptParser.PERIOD)
            self.state = 71 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 70
                    self.agentBlock()

                else:
                    raise NoViableAltException(self)
                self.state = 73 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamedStoryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STORY(self):
            return self.getToken(RegiaScriptParser.STORY, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def PRIORITY(self):
            return self.getToken(RegiaScriptParser.PRIORITY, 0)

        def NUMBER(self):
            return self.getToken(RegiaScriptParser.NUMBER, 0)

        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.DeclarationContext,i)


        def phaseDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.PhaseDeclContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.PhaseDeclContext,i)


        def storyAgentDecl(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.StoryAgentDeclContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.StoryAgentDeclContext,i)


        def duringBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.DuringBlockContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.DuringBlockContext,i)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_namedStory

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamedStory" ):
                listener.enterNamedStory(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamedStory" ):
                listener.exitNamedStory(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedStory" ):
                return visitor.visitNamedStory(self)
            else:
                return visitor.visitChildren(self)




    def namedStory(self):

        localctx = RegiaScriptParser.NamedStoryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_namedStory)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 78
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 75
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 80
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 81
            self.match(RegiaScriptParser.STORY)
            self.state = 82
            self.match(RegiaScriptParser.ID)
            self.state = 83
            self.match(RegiaScriptParser.PRIORITY)
            self.state = 84
            self.match(RegiaScriptParser.NUMBER)
            self.state = 85
            self.match(RegiaScriptParser.PERIOD)
            self.state = 89
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 86
                    self.declaration() 
                self.state = 91
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 95
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 92
                    self.phaseDecl() 
                self.state = 97
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 101
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 98
                    self.storyAgentDecl() 
                self.state = 103
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

            self.state = 105 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 104
                    self.duringBlock()

                else:
                    raise NoViableAltException(self)
                self.state = 107 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def actionDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.ActionDeclContext,0)


        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def eventDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.EventDeclContext,0)


        def conditionDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.ConditionDeclContext,0)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = RegiaScriptParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_declaration)
        self._la = 0 # Token type
        try:
            self.state = 130
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 112
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 109
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 114
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 115
                self.actionDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 119
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 116
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 121
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 122
                self.eventDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 126
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 123
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 128
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 129
                self.conditionDecl()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ActionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ACTION(self):
            return self.getToken(RegiaScriptParser.ACTION, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_actionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterActionDecl" ):
                listener.enterActionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitActionDecl" ):
                listener.exitActionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitActionDecl" ):
                return visitor.visitActionDecl(self)
            else:
                return visitor.visitChildren(self)




    def actionDecl(self):

        localctx = RegiaScriptParser.ActionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_actionDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 132
            self.match(RegiaScriptParser.ACTION)
            self.state = 133
            self.match(RegiaScriptParser.ID)
            self.state = 134
            self.match(RegiaScriptParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EventDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EVENT(self):
            return self.getToken(RegiaScriptParser.EVENT, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def origin(self):
            return self.getTypedRuleContext(RegiaScriptParser.OriginContext,0)


        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_eventDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEventDecl" ):
                listener.enterEventDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEventDecl" ):
                listener.exitEventDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEventDecl" ):
                return visitor.visitEventDecl(self)
            else:
                return visitor.visitChildren(self)




    def eventDecl(self):

        localctx = RegiaScriptParser.EventDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_eventDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.match(RegiaScriptParser.EVENT)
            self.state = 137
            self.match(RegiaScriptParser.ID)
            self.state = 138
            self.origin()
            self.state = 139
            self.match(RegiaScriptParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONDITION(self):
            return self.getToken(RegiaScriptParser.CONDITION, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def origin(self):
            return self.getTypedRuleContext(RegiaScriptParser.OriginContext,0)


        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_conditionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConditionDecl" ):
                listener.enterConditionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConditionDecl" ):
                listener.exitConditionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConditionDecl" ):
                return visitor.visitConditionDecl(self)
            else:
                return visitor.visitChildren(self)




    def conditionDecl(self):

        localctx = RegiaScriptParser.ConditionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_conditionDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.match(RegiaScriptParser.CONDITION)
            self.state = 142
            self.match(RegiaScriptParser.ID)
            self.state = 143
            self.origin()
            self.state = 144
            self.match(RegiaScriptParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OriginContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ENVIRONMENT(self):
            return self.getToken(RegiaScriptParser.ENVIRONMENT, 0)

        def DIRECTOR(self):
            return self.getToken(RegiaScriptParser.DIRECTOR, 0)

        def MYSELF(self):
            return self.getToken(RegiaScriptParser.MYSELF, 0)

        def PLAYER(self):
            return self.getToken(RegiaScriptParser.PLAYER, 0)

        def TIMER(self):
            return self.getToken(RegiaScriptParser.TIMER, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_origin

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrigin" ):
                listener.enterOrigin(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrigin" ):
                listener.exitOrigin(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrigin" ):
                return visitor.visitOrigin(self)
            else:
                return visitor.visitChildren(self)




    def origin(self):

        localctx = RegiaScriptParser.OriginContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_origin)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 146
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8126464) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PhaseDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PHASE(self):
            return self.getToken(RegiaScriptParser.PHASE, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def INITIAL(self):
            return self.getToken(RegiaScriptParser.INITIAL, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_phaseDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhaseDecl" ):
                listener.enterPhaseDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhaseDecl" ):
                listener.exitPhaseDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhaseDecl" ):
                return visitor.visitPhaseDecl(self)
            else:
                return visitor.visitChildren(self)




    def phaseDecl(self):

        localctx = RegiaScriptParser.PhaseDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_phaseDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 148
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 154
            self.match(RegiaScriptParser.PHASE)
            self.state = 155
            self.match(RegiaScriptParser.ID)
            self.state = 157
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==26:
                self.state = 156
                self.match(RegiaScriptParser.INITIAL)


            self.state = 159
            self.match(RegiaScriptParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StoryAgentDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AGENT(self):
            return self.getToken(RegiaScriptParser.AGENT, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def PLAYER(self):
            return self.getToken(RegiaScriptParser.PLAYER, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_storyAgentDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStoryAgentDecl" ):
                listener.enterStoryAgentDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStoryAgentDecl" ):
                listener.exitStoryAgentDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStoryAgentDecl" ):
                return visitor.visitStoryAgentDecl(self)
            else:
                return visitor.visitChildren(self)




    def storyAgentDecl(self):

        localctx = RegiaScriptParser.StoryAgentDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_storyAgentDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 161
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 166
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 167
            self.match(RegiaScriptParser.AGENT)
            self.state = 168
            self.match(RegiaScriptParser.ID)
            self.state = 170
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21:
                self.state = 169
                self.match(RegiaScriptParser.PLAYER)


            self.state = 172
            self.match(RegiaScriptParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AgentBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AGENT(self):
            return self.getToken(RegiaScriptParser.AGENT, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def COLON(self):
            return self.getToken(RegiaScriptParser.COLON, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def agentSection(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.AgentSectionContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.AgentSectionContext,i)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_agentBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAgentBlock" ):
                listener.enterAgentBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAgentBlock" ):
                listener.exitAgentBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAgentBlock" ):
                return visitor.visitAgentBlock(self)
            else:
                return visitor.visitChildren(self)




    def agentBlock(self):

        localctx = RegiaScriptParser.AgentBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_agentBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 174
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 179
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 180
            self.match(RegiaScriptParser.AGENT)
            self.state = 181
            self.match(RegiaScriptParser.ID)
            self.state = 182
            self.match(RegiaScriptParser.COLON)
            self.state = 186
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 183
                    self.agentSection() 
                self.state = 188
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AgentSectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def actionDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.ActionDeclContext,0)


        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def eventDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.EventDeclContext,0)


        def conditionDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.ConditionDeclContext,0)


        def whenBlock(self):
            return self.getTypedRuleContext(RegiaScriptParser.WhenBlockContext,0)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_agentSection

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAgentSection" ):
                listener.enterAgentSection(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAgentSection" ):
                listener.exitAgentSection(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAgentSection" ):
                return visitor.visitAgentSection(self)
            else:
                return visitor.visitChildren(self)




    def agentSection(self):

        localctx = RegiaScriptParser.AgentSectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_agentSection)
        self._la = 0 # Token type
        try:
            self.state = 211
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 192
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 189
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 194
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 195
                self.actionDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 199
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 196
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 201
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 202
                self.eventDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 203
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 208
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 209
                self.conditionDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 210
                self.whenBlock()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DuringBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DURING(self):
            return self.getToken(RegiaScriptParser.DURING, 0)

        def phaseRef(self):
            return self.getTypedRuleContext(RegiaScriptParser.PhaseRefContext,0)


        def COLON(self):
            return self.getToken(RegiaScriptParser.COLON, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def transitionRule(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.TransitionRuleContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.TransitionRuleContext,i)


        def agentBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.AgentBlockContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.AgentBlockContext,i)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_duringBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDuringBlock" ):
                listener.enterDuringBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDuringBlock" ):
                listener.exitDuringBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDuringBlock" ):
                return visitor.visitDuringBlock(self)
            else:
                return visitor.visitChildren(self)




    def duringBlock(self):

        localctx = RegiaScriptParser.DuringBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_duringBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 216
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 213
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 218
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 219
            self.match(RegiaScriptParser.DURING)
            self.state = 220
            self.phaseRef()
            self.state = 221
            self.match(RegiaScriptParser.COLON)
            self.state = 225
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,24,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 222
                    self.transitionRule() 
                self.state = 227
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,24,self._ctx)

            self.state = 229 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 228
                    self.agentBlock()

                else:
                    raise NoViableAltException(self)
                self.state = 231 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,25,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransitionRuleContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRANSITION(self):
            return self.getToken(RegiaScriptParser.TRANSITION, 0)

        def TO(self):
            return self.getToken(RegiaScriptParser.TO, 0)

        def phaseTarget(self):
            return self.getTypedRuleContext(RegiaScriptParser.PhaseTargetContext,0)


        def WHEN(self):
            return self.getToken(RegiaScriptParser.WHEN, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def IF(self):
            return self.getToken(RegiaScriptParser.IF, 0)

        def condExpr(self):
            return self.getTypedRuleContext(RegiaScriptParser.CondExprContext,0)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_transitionRule

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransitionRule" ):
                listener.enterTransitionRule(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransitionRule" ):
                listener.exitTransitionRule(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTransitionRule" ):
                return visitor.visitTransitionRule(self)
            else:
                return visitor.visitChildren(self)




    def transitionRule(self):

        localctx = RegiaScriptParser.TransitionRuleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_transitionRule)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 236
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==35:
                self.state = 233
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 238
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 239
            self.match(RegiaScriptParser.TRANSITION)
            self.state = 240
            self.match(RegiaScriptParser.TO)
            self.state = 241
            self.phaseTarget()
            self.state = 242
            self.match(RegiaScriptParser.WHEN)
            self.state = 243
            self.match(RegiaScriptParser.ID)
            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==11:
                self.state = 244
                self.match(RegiaScriptParser.IF)
                self.state = 245
                self.condExpr()


            self.state = 248
            self.match(RegiaScriptParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PhaseTargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def END(self):
            return self.getToken(RegiaScriptParser.END, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_phaseTarget

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhaseTarget" ):
                listener.enterPhaseTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhaseTarget" ):
                listener.exitPhaseTarget(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhaseTarget" ):
                return visitor.visitPhaseTarget(self)
            else:
                return visitor.visitChildren(self)




    def phaseTarget(self):

        localctx = RegiaScriptParser.PhaseTargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_phaseTarget)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 250
            _la = self._input.LA(1)
            if not(_la==25 or _la==34):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PhaseRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def STORY(self):
            return self.getToken(RegiaScriptParser.STORY, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_phaseRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPhaseRef" ):
                listener.enterPhaseRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPhaseRef" ):
                listener.exitPhaseRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPhaseRef" ):
                return visitor.visitPhaseRef(self)
            else:
                return visitor.visitChildren(self)




    def phaseRef(self):

        localctx = RegiaScriptParser.PhaseRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_phaseRef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            _la = self._input.LA(1)
            if not(_la==1 or _la==34):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhenBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHEN(self):
            return self.getToken(RegiaScriptParser.WHEN, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def IF(self):
            return self.getToken(RegiaScriptParser.IF, 0)

        def condExpr(self):
            return self.getTypedRuleContext(RegiaScriptParser.CondExprContext,0)


        def COLON(self):
            return self.getToken(RegiaScriptParser.COLON, 0)

        def doSequence(self):
            return self.getTypedRuleContext(RegiaScriptParser.DoSequenceContext,0)


        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def ifBranch(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.IfBranchContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.IfBranchContext,i)


        def getRuleIndex(self):
            return RegiaScriptParser.RULE_whenBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhenBlock" ):
                listener.enterWhenBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhenBlock" ):
                listener.exitWhenBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhenBlock" ):
                return visitor.visitWhenBlock(self)
            else:
                return visitor.visitChildren(self)




    def whenBlock(self):

        localctx = RegiaScriptParser.WhenBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_whenBlock)
        self._la = 0 # Token type
        try:
            self.state = 291
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 257
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 254
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 259
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 260
                self.match(RegiaScriptParser.WHEN)
                self.state = 261
                self.match(RegiaScriptParser.ID)
                self.state = 262
                self.match(RegiaScriptParser.IF)
                self.state = 263
                self.condExpr()
                self.state = 264
                self.match(RegiaScriptParser.COLON)
                self.state = 265
                self.doSequence()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 270
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 267
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 272
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 273
                self.match(RegiaScriptParser.WHEN)
                self.state = 274
                self.match(RegiaScriptParser.ID)
                self.state = 275
                self.match(RegiaScriptParser.COLON)
                self.state = 277 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 276
                    self.ifBranch()
                    self.state = 279 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==11 or _la==27):
                        break

                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 284
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==35:
                    self.state = 281
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 286
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 287
                self.match(RegiaScriptParser.WHEN)
                self.state = 288
                self.match(RegiaScriptParser.ID)
                self.state = 289
                self.match(RegiaScriptParser.COLON)
                self.state = 290
                self.doSequence()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfBranchContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(RegiaScriptParser.IF, 0)

        def condExpr(self):
            return self.getTypedRuleContext(RegiaScriptParser.CondExprContext,0)


        def COLON(self):
            return self.getToken(RegiaScriptParser.COLON, 0)

        def doSequence(self):
            return self.getTypedRuleContext(RegiaScriptParser.DoSequenceContext,0)


        def OTHERWISE(self):
            return self.getToken(RegiaScriptParser.OTHERWISE, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_ifBranch

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfBranch" ):
                listener.enterIfBranch(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfBranch" ):
                listener.exitIfBranch(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfBranch" ):
                return visitor.visitIfBranch(self)
            else:
                return visitor.visitChildren(self)




    def ifBranch(self):

        localctx = RegiaScriptParser.IfBranchContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_ifBranch)
        try:
            self.state = 301
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 293
                self.match(RegiaScriptParser.IF)
                self.state = 294
                self.condExpr()
                self.state = 295
                self.match(RegiaScriptParser.COLON)
                self.state = 296
                self.doSequence()
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 2)
                self.state = 298
                self.match(RegiaScriptParser.OTHERWISE)
                self.state = 299
                self.match(RegiaScriptParser.COLON)
                self.state = 300
                self.doSequence()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condAnd(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.CondAndContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.CondAndContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.OR)
            else:
                return self.getToken(RegiaScriptParser.OR, i)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_condExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondExpr" ):
                listener.enterCondExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondExpr" ):
                listener.exitCondExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondExpr" ):
                return visitor.visitCondExpr(self)
            else:
                return visitor.visitChildren(self)




    def condExpr(self):

        localctx = RegiaScriptParser.CondExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_condExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 303
            self.condAnd()
            self.state = 308
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 304
                self.match(RegiaScriptParser.OR)
                self.state = 305
                self.condAnd()
                self.state = 310
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondAndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condTerm(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.CondTermContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.CondTermContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.AND)
            else:
                return self.getToken(RegiaScriptParser.AND, i)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_condAnd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondAnd" ):
                listener.enterCondAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondAnd" ):
                listener.exitCondAnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondAnd" ):
                return visitor.visitCondAnd(self)
            else:
                return visitor.visitChildren(self)




    def condAnd(self):

        localctx = RegiaScriptParser.CondAndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_condAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 311
            self.condTerm()
            self.state = 316
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==12:
                self.state = 312
                self.match(RegiaScriptParser.AND)
                self.state = 313
                self.condTerm()
                self.state = 318
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondTermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def condAtom(self):
            return self.getTypedRuleContext(RegiaScriptParser.CondAtomContext,0)


        def NOT(self):
            return self.getToken(RegiaScriptParser.NOT, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_condTerm

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondTerm" ):
                listener.enterCondTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondTerm" ):
                listener.exitCondTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondTerm" ):
                return visitor.visitCondTerm(self)
            else:
                return visitor.visitChildren(self)




    def condTerm(self):

        localctx = RegiaScriptParser.CondTermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_condTerm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 320
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==14:
                self.state = 319
                self.match(RegiaScriptParser.NOT)


            self.state = 322
            self.condAtom()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CondAtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def LPAREN(self):
            return self.getToken(RegiaScriptParser.LPAREN, 0)

        def condExpr(self):
            return self.getTypedRuleContext(RegiaScriptParser.CondExprContext,0)


        def RPAREN(self):
            return self.getToken(RegiaScriptParser.RPAREN, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_condAtom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondAtom" ):
                listener.enterCondAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondAtom" ):
                listener.exitCondAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondAtom" ):
                return visitor.visitCondAtom(self)
            else:
                return visitor.visitChildren(self)




    def condAtom(self):

        localctx = RegiaScriptParser.CondAtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_condAtom)
        try:
            self.state = 329
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [34]:
                self.enterOuterAlt(localctx, 1)
                self.state = 324
                self.match(RegiaScriptParser.ID)
                pass
            elif token in [31]:
                self.enterOuterAlt(localctx, 2)
                self.state = 325
                self.match(RegiaScriptParser.LPAREN)
                self.state = 326
                self.condExpr()
                self.state = 327
                self.match(RegiaScriptParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoSequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def doAction(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.DoActionContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.DoActionContext,i)


        def PERIOD(self):
            return self.getToken(RegiaScriptParser.PERIOD, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.COMMA)
            else:
                return self.getToken(RegiaScriptParser.COMMA, i)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_doSequence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoSequence" ):
                listener.enterDoSequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoSequence" ):
                listener.exitDoSequence(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoSequence" ):
                return visitor.visitDoSequence(self)
            else:
                return visitor.visitChildren(self)




    def doSequence(self):

        localctx = RegiaScriptParser.DoSequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_doSequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 331
            self.doAction()
            self.state = 336
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 332
                self.match(RegiaScriptParser.COMMA)
                self.state = 333
                self.doAction()
                self.state = 338
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 339
            self.match(RegiaScriptParser.PERIOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoActionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DO(self):
            return self.getToken(RegiaScriptParser.DO, 0)

        def BELIEVE(self):
            return self.getToken(RegiaScriptParser.BELIEVE, 0)

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def FORGET(self):
            return self.getToken(RegiaScriptParser.FORGET, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_doAction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoAction" ):
                listener.enterDoAction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoAction" ):
                listener.exitDoAction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoAction" ):
                return visitor.visitDoAction(self)
            else:
                return visitor.visitChildren(self)




    def doAction(self):

        localctx = RegiaScriptParser.DoActionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_doAction)
        try:
            self.state = 349
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 341
                self.match(RegiaScriptParser.DO)
                self.state = 342
                self.match(RegiaScriptParser.BELIEVE)
                self.state = 343
                self.match(RegiaScriptParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 344
                self.match(RegiaScriptParser.DO)
                self.state = 345
                self.match(RegiaScriptParser.FORGET)
                self.state = 346
                self.match(RegiaScriptParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 347
                self.match(RegiaScriptParser.DO)
                self.state = 348
                self.match(RegiaScriptParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





