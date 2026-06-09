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
        4,1,36,295,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,1,0,4,0,48,8,0,11,0,12,0,49,1,0,1,0,1,1,
        1,1,3,1,56,8,1,1,2,5,2,59,8,2,10,2,12,2,62,9,2,1,2,1,2,1,2,1,2,4,
        2,68,8,2,11,2,12,2,69,1,3,5,3,73,8,3,10,3,12,3,76,9,3,1,3,1,3,1,
        3,1,3,1,3,1,3,5,3,84,8,3,10,3,12,3,87,9,3,1,3,5,3,90,8,3,10,3,12,
        3,93,9,3,1,3,4,3,96,8,3,11,3,12,3,97,1,4,5,4,101,8,4,10,4,12,4,104,
        9,4,1,4,1,4,5,4,108,8,4,10,4,12,4,111,9,4,1,4,1,4,5,4,115,8,4,10,
        4,12,4,118,9,4,1,4,3,4,121,8,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,
        6,1,7,1,7,1,7,1,7,1,7,1,8,1,8,1,9,5,9,140,8,9,10,9,12,9,143,9,9,
        1,9,1,9,1,9,1,9,1,10,5,10,150,8,10,10,10,12,10,153,9,10,1,10,1,10,
        1,10,1,10,5,10,159,8,10,10,10,12,10,162,9,10,1,11,5,11,165,8,11,
        10,11,12,11,168,9,11,1,11,1,11,5,11,172,8,11,10,11,12,11,175,9,11,
        1,11,1,11,5,11,179,8,11,10,11,12,11,182,9,11,1,11,1,11,3,11,186,
        8,11,1,12,5,12,189,8,12,10,12,12,12,192,9,12,1,12,1,12,1,12,1,12,
        5,12,198,8,12,10,12,12,12,201,9,12,1,12,4,12,204,8,12,11,12,12,12,
        205,1,13,5,13,209,8,13,10,13,12,13,212,9,13,1,13,1,13,1,13,1,13,
        1,13,1,13,1,13,1,13,3,13,222,8,13,1,13,1,13,1,14,1,14,1,15,1,15,
        1,16,5,16,231,8,16,10,16,12,16,234,9,16,1,16,1,16,1,16,1,16,1,16,
        3,16,241,8,16,1,16,1,16,1,16,1,17,1,17,1,17,5,17,249,8,17,10,17,
        12,17,252,9,17,1,18,1,18,1,18,5,18,257,8,18,10,18,12,18,260,9,18,
        1,19,3,19,263,8,19,1,19,1,19,1,20,1,20,1,20,1,20,1,20,1,20,3,20,
        273,8,20,1,21,1,21,1,21,5,21,278,8,21,10,21,12,21,281,9,21,1,21,
        1,21,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,3,22,293,8,22,1,22,
        0,0,23,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,
        42,44,0,3,1,0,19,23,2,0,26,26,33,33,2,0,10,10,33,33,307,0,47,1,0,
        0,0,2,55,1,0,0,0,4,60,1,0,0,0,6,74,1,0,0,0,8,120,1,0,0,0,10,122,
        1,0,0,0,12,126,1,0,0,0,14,131,1,0,0,0,16,136,1,0,0,0,18,141,1,0,
        0,0,20,151,1,0,0,0,22,185,1,0,0,0,24,190,1,0,0,0,26,210,1,0,0,0,
        28,225,1,0,0,0,30,227,1,0,0,0,32,232,1,0,0,0,34,245,1,0,0,0,36,253,
        1,0,0,0,38,262,1,0,0,0,40,272,1,0,0,0,42,274,1,0,0,0,44,292,1,0,
        0,0,46,48,3,2,1,0,47,46,1,0,0,0,48,49,1,0,0,0,49,47,1,0,0,0,49,50,
        1,0,0,0,50,51,1,0,0,0,51,52,5,0,0,1,52,1,1,0,0,0,53,56,3,4,2,0,54,
        56,3,6,3,0,55,53,1,0,0,0,55,54,1,0,0,0,56,3,1,0,0,0,57,59,5,34,0,
        0,58,57,1,0,0,0,59,62,1,0,0,0,60,58,1,0,0,0,60,61,1,0,0,0,61,63,
        1,0,0,0,62,60,1,0,0,0,63,64,5,1,0,0,64,65,5,2,0,0,65,67,5,27,0,0,
        66,68,3,24,12,0,67,66,1,0,0,0,68,69,1,0,0,0,69,67,1,0,0,0,69,70,
        1,0,0,0,70,5,1,0,0,0,71,73,5,34,0,0,72,71,1,0,0,0,73,76,1,0,0,0,
        74,72,1,0,0,0,74,75,1,0,0,0,75,77,1,0,0,0,76,74,1,0,0,0,77,78,5,
        1,0,0,78,79,5,33,0,0,79,80,5,3,0,0,80,81,5,32,0,0,81,85,5,27,0,0,
        82,84,3,8,4,0,83,82,1,0,0,0,84,87,1,0,0,0,85,83,1,0,0,0,85,86,1,
        0,0,0,86,91,1,0,0,0,87,85,1,0,0,0,88,90,3,18,9,0,89,88,1,0,0,0,90,
        93,1,0,0,0,91,89,1,0,0,0,91,92,1,0,0,0,92,95,1,0,0,0,93,91,1,0,0,
        0,94,96,3,24,12,0,95,94,1,0,0,0,96,97,1,0,0,0,97,95,1,0,0,0,97,98,
        1,0,0,0,98,7,1,0,0,0,99,101,5,34,0,0,100,99,1,0,0,0,101,104,1,0,
        0,0,102,100,1,0,0,0,102,103,1,0,0,0,103,105,1,0,0,0,104,102,1,0,
        0,0,105,121,3,10,5,0,106,108,5,34,0,0,107,106,1,0,0,0,108,111,1,
        0,0,0,109,107,1,0,0,0,109,110,1,0,0,0,110,112,1,0,0,0,111,109,1,
        0,0,0,112,121,3,12,6,0,113,115,5,34,0,0,114,113,1,0,0,0,115,118,
        1,0,0,0,116,114,1,0,0,0,116,117,1,0,0,0,117,119,1,0,0,0,118,116,
        1,0,0,0,119,121,3,14,7,0,120,102,1,0,0,0,120,109,1,0,0,0,120,116,
        1,0,0,0,121,9,1,0,0,0,122,123,5,6,0,0,123,124,5,33,0,0,124,125,5,
        27,0,0,125,11,1,0,0,0,126,127,5,7,0,0,127,128,5,33,0,0,128,129,3,
        16,8,0,129,130,5,27,0,0,130,13,1,0,0,0,131,132,5,8,0,0,132,133,5,
        33,0,0,133,134,3,16,8,0,134,135,5,27,0,0,135,15,1,0,0,0,136,137,
        7,0,0,0,137,17,1,0,0,0,138,140,5,34,0,0,139,138,1,0,0,0,140,143,
        1,0,0,0,141,139,1,0,0,0,141,142,1,0,0,0,142,144,1,0,0,0,143,141,
        1,0,0,0,144,145,5,4,0,0,145,146,5,33,0,0,146,147,5,27,0,0,147,19,
        1,0,0,0,148,150,5,34,0,0,149,148,1,0,0,0,150,153,1,0,0,0,151,149,
        1,0,0,0,151,152,1,0,0,0,152,154,1,0,0,0,153,151,1,0,0,0,154,155,
        5,5,0,0,155,156,5,33,0,0,156,160,5,28,0,0,157,159,3,22,11,0,158,
        157,1,0,0,0,159,162,1,0,0,0,160,158,1,0,0,0,160,161,1,0,0,0,161,
        21,1,0,0,0,162,160,1,0,0,0,163,165,5,34,0,0,164,163,1,0,0,0,165,
        168,1,0,0,0,166,164,1,0,0,0,166,167,1,0,0,0,167,169,1,0,0,0,168,
        166,1,0,0,0,169,186,3,10,5,0,170,172,5,34,0,0,171,170,1,0,0,0,172,
        175,1,0,0,0,173,171,1,0,0,0,173,174,1,0,0,0,174,176,1,0,0,0,175,
        173,1,0,0,0,176,186,3,12,6,0,177,179,5,34,0,0,178,177,1,0,0,0,179,
        182,1,0,0,0,180,178,1,0,0,0,180,181,1,0,0,0,181,183,1,0,0,0,182,
        180,1,0,0,0,183,186,3,14,7,0,184,186,3,32,16,0,185,166,1,0,0,0,185,
        173,1,0,0,0,185,180,1,0,0,0,185,184,1,0,0,0,186,23,1,0,0,0,187,189,
        5,34,0,0,188,187,1,0,0,0,189,192,1,0,0,0,190,188,1,0,0,0,190,191,
        1,0,0,0,191,193,1,0,0,0,192,190,1,0,0,0,193,194,5,9,0,0,194,195,
        3,30,15,0,195,199,5,28,0,0,196,198,3,26,13,0,197,196,1,0,0,0,198,
        201,1,0,0,0,199,197,1,0,0,0,199,200,1,0,0,0,200,203,1,0,0,0,201,
        199,1,0,0,0,202,204,3,20,10,0,203,202,1,0,0,0,204,205,1,0,0,0,205,
        203,1,0,0,0,205,206,1,0,0,0,206,25,1,0,0,0,207,209,5,34,0,0,208,
        207,1,0,0,0,209,212,1,0,0,0,210,208,1,0,0,0,210,211,1,0,0,0,211,
        213,1,0,0,0,212,210,1,0,0,0,213,214,5,24,0,0,214,215,5,25,0,0,215,
        216,3,28,14,0,216,217,5,11,0,0,217,218,5,33,0,0,218,221,3,16,8,0,
        219,220,5,12,0,0,220,222,3,34,17,0,221,219,1,0,0,0,221,222,1,0,0,
        0,222,223,1,0,0,0,223,224,5,27,0,0,224,27,1,0,0,0,225,226,7,1,0,
        0,226,29,1,0,0,0,227,228,7,2,0,0,228,31,1,0,0,0,229,231,5,34,0,0,
        230,229,1,0,0,0,231,234,1,0,0,0,232,230,1,0,0,0,232,233,1,0,0,0,
        233,235,1,0,0,0,234,232,1,0,0,0,235,236,5,11,0,0,236,237,5,33,0,
        0,237,240,3,16,8,0,238,239,5,12,0,0,239,241,3,34,17,0,240,238,1,
        0,0,0,240,241,1,0,0,0,241,242,1,0,0,0,242,243,5,28,0,0,243,244,3,
        42,21,0,244,33,1,0,0,0,245,250,3,36,18,0,246,247,5,14,0,0,247,249,
        3,36,18,0,248,246,1,0,0,0,249,252,1,0,0,0,250,248,1,0,0,0,250,251,
        1,0,0,0,251,35,1,0,0,0,252,250,1,0,0,0,253,258,3,38,19,0,254,255,
        5,13,0,0,255,257,3,38,19,0,256,254,1,0,0,0,257,260,1,0,0,0,258,256,
        1,0,0,0,258,259,1,0,0,0,259,37,1,0,0,0,260,258,1,0,0,0,261,263,5,
        15,0,0,262,261,1,0,0,0,262,263,1,0,0,0,263,264,1,0,0,0,264,265,3,
        40,20,0,265,39,1,0,0,0,266,267,5,33,0,0,267,273,3,16,8,0,268,269,
        5,30,0,0,269,270,3,34,17,0,270,271,5,31,0,0,271,273,1,0,0,0,272,
        266,1,0,0,0,272,268,1,0,0,0,273,41,1,0,0,0,274,279,3,44,22,0,275,
        276,5,29,0,0,276,278,3,44,22,0,277,275,1,0,0,0,278,281,1,0,0,0,279,
        277,1,0,0,0,279,280,1,0,0,0,280,282,1,0,0,0,281,279,1,0,0,0,282,
        283,5,27,0,0,283,43,1,0,0,0,284,285,5,16,0,0,285,286,5,17,0,0,286,
        293,5,33,0,0,287,288,5,16,0,0,288,289,5,18,0,0,289,293,5,33,0,0,
        290,291,5,16,0,0,291,293,5,33,0,0,292,284,1,0,0,0,292,287,1,0,0,
        0,292,290,1,0,0,0,293,45,1,0,0,0,32,49,55,60,69,74,85,91,97,102,
        109,116,120,141,151,160,166,173,180,185,190,199,205,210,221,232,
        240,250,258,262,272,279,292
    ]

class RegiaScriptParser ( Parser ):

    grammarFileName = "RegiaScript.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'STORY'", "'DEFAULT'", "'PRIORITY'", 
                     "'PHASE'", "'AGENT'", "'ACTION'", "'EVENT'", "'CONDITION'", 
                     "'DURING'", "'ALWAYS'", "'WHEN'", "'IF'", "'AND'", 
                     "'OR'", "'NOT'", "'DO'", "'BELIEVE'", "'FORGET'", "'ENVIRONMENT'", 
                     "'DIRECTOR'", "'MYSELF'", "'PLAYER'", "'TIMER'", "'TRANSITION'", 
                     "'TO'", "'END'", "'.'", "':'", "','", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "STORY", "DEFAULT", "PRIORITY", "PHASE", 
                      "AGENT", "ACTION", "EVENT", "CONDITION", "DURING", 
                      "ALWAYS", "WHEN", "IF", "AND", "OR", "NOT", "DO", 
                      "BELIEVE", "FORGET", "ENVIRONMENT", "DIRECTOR", "MYSELF", 
                      "PLAYER", "TIMER", "TRANSITION", "TO", "END", "PERIOD", 
                      "COLON", "COMMA", "LPAREN", "RPAREN", "NUMBER", "ID", 
                      "DOC_COMMENT", "COMMENT", "WS" ]

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
    RULE_agentBlock = 10
    RULE_agentSection = 11
    RULE_duringBlock = 12
    RULE_transitionRule = 13
    RULE_phaseTarget = 14
    RULE_phaseRef = 15
    RULE_whenBlock = 16
    RULE_condExpr = 17
    RULE_condAnd = 18
    RULE_condTerm = 19
    RULE_condAtom = 20
    RULE_doSequence = 21
    RULE_doAction = 22

    ruleNames =  [ "program", "storyDef", "defaultStory", "namedStory", 
                   "declaration", "actionDecl", "eventDecl", "conditionDecl", 
                   "origin", "phaseDecl", "agentBlock", "agentSection", 
                   "duringBlock", "transitionRule", "phaseTarget", "phaseRef", 
                   "whenBlock", "condExpr", "condAnd", "condTerm", "condAtom", 
                   "doSequence", "doAction" ]

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
    ALWAYS=10
    WHEN=11
    IF=12
    AND=13
    OR=14
    NOT=15
    DO=16
    BELIEVE=17
    FORGET=18
    ENVIRONMENT=19
    DIRECTOR=20
    MYSELF=21
    PLAYER=22
    TIMER=23
    TRANSITION=24
    TO=25
    END=26
    PERIOD=27
    COLON=28
    COMMA=29
    LPAREN=30
    RPAREN=31
    NUMBER=32
    ID=33
    DOC_COMMENT=34
    COMMENT=35
    WS=36

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
            self.state = 47 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 46
                self.storyDef()
                self.state = 49 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==34):
                    break

            self.state = 51
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
            self.state = 55
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 53
                self.defaultStory()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 54
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

        def duringBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.DuringBlockContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.DuringBlockContext,i)


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
            self.state = 60
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 57
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 62
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 63
            self.match(RegiaScriptParser.STORY)
            self.state = 64
            self.match(RegiaScriptParser.DEFAULT)
            self.state = 65
            self.match(RegiaScriptParser.PERIOD)
            self.state = 67 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 66
                    self.duringBlock()

                else:
                    raise NoViableAltException(self)
                self.state = 69 
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
            self.state = 74
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 71
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 77
            self.match(RegiaScriptParser.STORY)
            self.state = 78
            self.match(RegiaScriptParser.ID)
            self.state = 79
            self.match(RegiaScriptParser.PRIORITY)
            self.state = 80
            self.match(RegiaScriptParser.NUMBER)
            self.state = 81
            self.match(RegiaScriptParser.PERIOD)
            self.state = 85
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 82
                    self.declaration() 
                self.state = 87
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

            self.state = 91
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 88
                    self.phaseDecl() 
                self.state = 93
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

            self.state = 95 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 94
                    self.duringBlock()

                else:
                    raise NoViableAltException(self)
                self.state = 97 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

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
            self.state = 120
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 102
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==34:
                    self.state = 99
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 104
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 105
                self.actionDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 109
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==34:
                    self.state = 106
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 111
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 112
                self.eventDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 116
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==34:
                    self.state = 113
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 118
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 119
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
            self.state = 122
            self.match(RegiaScriptParser.ACTION)
            self.state = 123
            self.match(RegiaScriptParser.ID)
            self.state = 124
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
            self.state = 126
            self.match(RegiaScriptParser.EVENT)
            self.state = 127
            self.match(RegiaScriptParser.ID)
            self.state = 128
            self.origin()
            self.state = 129
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
            self.state = 131
            self.match(RegiaScriptParser.CONDITION)
            self.state = 132
            self.match(RegiaScriptParser.ID)
            self.state = 133
            self.origin()
            self.state = 134
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
            self.state = 136
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16252928) != 0)):
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
            self.state = 141
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 138
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 144
            self.match(RegiaScriptParser.PHASE)
            self.state = 145
            self.match(RegiaScriptParser.ID)
            self.state = 146
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
        self.enterRule(localctx, 20, self.RULE_agentBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 148
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 154
            self.match(RegiaScriptParser.AGENT)
            self.state = 155
            self.match(RegiaScriptParser.ID)
            self.state = 156
            self.match(RegiaScriptParser.COLON)
            self.state = 160
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 157
                    self.agentSection() 
                self.state = 162
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

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
        self.enterRule(localctx, 22, self.RULE_agentSection)
        self._la = 0 # Token type
        try:
            self.state = 185
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 166
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==34:
                    self.state = 163
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 168
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 169
                self.actionDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 173
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==34:
                    self.state = 170
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 175
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 176
                self.eventDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 180
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==34:
                    self.state = 177
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 182
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 183
                self.conditionDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 184
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
        self.enterRule(localctx, 24, self.RULE_duringBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 187
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 192
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 193
            self.match(RegiaScriptParser.DURING)
            self.state = 194
            self.phaseRef()
            self.state = 195
            self.match(RegiaScriptParser.COLON)
            self.state = 199
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,20,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 196
                    self.transitionRule() 
                self.state = 201
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,20,self._ctx)

            self.state = 203 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 202
                    self.agentBlock()

                else:
                    raise NoViableAltException(self)
                self.state = 205 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,21,self._ctx)

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

        def origin(self):
            return self.getTypedRuleContext(RegiaScriptParser.OriginContext,0)


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
        self.enterRule(localctx, 26, self.RULE_transitionRule)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 207
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 212
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 213
            self.match(RegiaScriptParser.TRANSITION)
            self.state = 214
            self.match(RegiaScriptParser.TO)
            self.state = 215
            self.phaseTarget()
            self.state = 216
            self.match(RegiaScriptParser.WHEN)
            self.state = 217
            self.match(RegiaScriptParser.ID)
            self.state = 218
            self.origin()
            self.state = 221
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 219
                self.match(RegiaScriptParser.IF)
                self.state = 220
                self.condExpr()


            self.state = 223
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
        self.enterRule(localctx, 28, self.RULE_phaseTarget)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 225
            _la = self._input.LA(1)
            if not(_la==26 or _la==33):
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

        def ALWAYS(self):
            return self.getToken(RegiaScriptParser.ALWAYS, 0)

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
        self.enterRule(localctx, 30, self.RULE_phaseRef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 227
            _la = self._input.LA(1)
            if not(_la==10 or _la==33):
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

        def origin(self):
            return self.getTypedRuleContext(RegiaScriptParser.OriginContext,0)


        def COLON(self):
            return self.getToken(RegiaScriptParser.COLON, 0)

        def doSequence(self):
            return self.getTypedRuleContext(RegiaScriptParser.DoSequenceContext,0)


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
        self.enterRule(localctx, 32, self.RULE_whenBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 232
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34:
                self.state = 229
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 234
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 235
            self.match(RegiaScriptParser.WHEN)
            self.state = 236
            self.match(RegiaScriptParser.ID)
            self.state = 237
            self.origin()
            self.state = 240
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 238
                self.match(RegiaScriptParser.IF)
                self.state = 239
                self.condExpr()


            self.state = 242
            self.match(RegiaScriptParser.COLON)
            self.state = 243
            self.doSequence()
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
        self.enterRule(localctx, 34, self.RULE_condExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 245
            self.condAnd()
            self.state = 250
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==14:
                self.state = 246
                self.match(RegiaScriptParser.OR)
                self.state = 247
                self.condAnd()
                self.state = 252
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
        self.enterRule(localctx, 36, self.RULE_condAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            self.condTerm()
            self.state = 258
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 254
                self.match(RegiaScriptParser.AND)
                self.state = 255
                self.condTerm()
                self.state = 260
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
        self.enterRule(localctx, 38, self.RULE_condTerm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 262
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==15:
                self.state = 261
                self.match(RegiaScriptParser.NOT)


            self.state = 264
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

        def origin(self):
            return self.getTypedRuleContext(RegiaScriptParser.OriginContext,0)


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
        self.enterRule(localctx, 40, self.RULE_condAtom)
        try:
            self.state = 272
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [33]:
                self.enterOuterAlt(localctx, 1)
                self.state = 266
                self.match(RegiaScriptParser.ID)
                self.state = 267
                self.origin()
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 2)
                self.state = 268
                self.match(RegiaScriptParser.LPAREN)
                self.state = 269
                self.condExpr()
                self.state = 270
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
        self.enterRule(localctx, 42, self.RULE_doSequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 274
            self.doAction()
            self.state = 279
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==29:
                self.state = 275
                self.match(RegiaScriptParser.COMMA)
                self.state = 276
                self.doAction()
                self.state = 281
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 282
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
        self.enterRule(localctx, 44, self.RULE_doAction)
        try:
            self.state = 292
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 284
                self.match(RegiaScriptParser.DO)
                self.state = 285
                self.match(RegiaScriptParser.BELIEVE)
                self.state = 286
                self.match(RegiaScriptParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 287
                self.match(RegiaScriptParser.DO)
                self.state = 288
                self.match(RegiaScriptParser.FORGET)
                self.state = 289
                self.match(RegiaScriptParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 290
                self.match(RegiaScriptParser.DO)
                self.state = 291
                self.match(RegiaScriptParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





