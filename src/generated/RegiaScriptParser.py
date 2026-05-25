# Generated from grammars/RegiaScript.g4 by ANTLR 4.13.2
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
        4,1,28,180,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,1,0,5,0,34,8,0,10,0,12,0,37,9,0,1,0,5,0,40,8,
        0,10,0,12,0,43,9,0,1,0,1,0,1,1,5,1,48,8,1,10,1,12,1,51,9,1,1,1,1,
        1,5,1,55,8,1,10,1,12,1,58,9,1,1,1,1,1,5,1,62,8,1,10,1,12,1,65,9,
        1,1,1,1,1,5,1,69,8,1,10,1,12,1,72,9,1,1,1,3,1,75,8,1,1,2,1,2,1,2,
        1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,
        1,5,1,6,1,6,1,7,5,7,100,8,7,10,7,12,7,103,9,7,1,7,1,7,1,7,1,7,4,
        7,109,8,7,11,7,12,7,110,1,8,1,8,1,9,5,9,116,8,9,10,9,12,9,119,9,
        9,1,9,1,9,1,9,1,9,1,9,3,9,126,8,9,1,9,1,9,1,9,1,10,1,10,1,10,5,10,
        134,8,10,10,10,12,10,137,9,10,1,11,1,11,1,11,5,11,142,8,11,10,11,
        12,11,145,9,11,1,12,3,12,148,8,12,1,12,1,12,1,13,1,13,1,13,1,13,
        1,13,1,13,3,13,158,8,13,1,14,1,14,1,14,5,14,163,8,14,10,14,12,14,
        166,9,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,3,15,
        178,8,15,1,15,0,0,16,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,
        0,2,1,0,16,18,2,0,7,7,25,25,183,0,35,1,0,0,0,2,74,1,0,0,0,4,76,1,
        0,0,0,6,82,1,0,0,0,8,86,1,0,0,0,10,91,1,0,0,0,12,96,1,0,0,0,14,101,
        1,0,0,0,16,112,1,0,0,0,18,117,1,0,0,0,20,130,1,0,0,0,22,138,1,0,
        0,0,24,147,1,0,0,0,26,157,1,0,0,0,28,159,1,0,0,0,30,177,1,0,0,0,
        32,34,3,2,1,0,33,32,1,0,0,0,34,37,1,0,0,0,35,33,1,0,0,0,35,36,1,
        0,0,0,36,41,1,0,0,0,37,35,1,0,0,0,38,40,3,14,7,0,39,38,1,0,0,0,40,
        43,1,0,0,0,41,39,1,0,0,0,41,42,1,0,0,0,42,44,1,0,0,0,43,41,1,0,0,
        0,44,45,5,0,0,1,45,1,1,0,0,0,46,48,5,26,0,0,47,46,1,0,0,0,48,51,
        1,0,0,0,49,47,1,0,0,0,49,50,1,0,0,0,50,52,1,0,0,0,51,49,1,0,0,0,
        52,75,3,4,2,0,53,55,5,26,0,0,54,53,1,0,0,0,55,58,1,0,0,0,56,54,1,
        0,0,0,56,57,1,0,0,0,57,59,1,0,0,0,58,56,1,0,0,0,59,75,3,6,3,0,60,
        62,5,26,0,0,61,60,1,0,0,0,62,65,1,0,0,0,63,61,1,0,0,0,63,64,1,0,
        0,0,64,66,1,0,0,0,65,63,1,0,0,0,66,75,3,8,4,0,67,69,5,26,0,0,68,
        67,1,0,0,0,69,72,1,0,0,0,70,68,1,0,0,0,70,71,1,0,0,0,71,73,1,0,0,
        0,72,70,1,0,0,0,73,75,3,10,5,0,74,49,1,0,0,0,74,56,1,0,0,0,74,63,
        1,0,0,0,74,70,1,0,0,0,75,3,1,0,0,0,76,77,5,1,0,0,77,78,5,25,0,0,
        78,79,5,5,0,0,79,80,5,24,0,0,80,81,5,19,0,0,81,5,1,0,0,0,82,83,5,
        2,0,0,83,84,5,25,0,0,84,85,5,19,0,0,85,7,1,0,0,0,86,87,5,3,0,0,87,
        88,5,25,0,0,88,89,3,12,6,0,89,90,5,19,0,0,90,9,1,0,0,0,91,92,5,4,
        0,0,92,93,5,25,0,0,93,94,3,12,6,0,94,95,5,19,0,0,95,11,1,0,0,0,96,
        97,7,0,0,0,97,13,1,0,0,0,98,100,5,26,0,0,99,98,1,0,0,0,100,103,1,
        0,0,0,101,99,1,0,0,0,101,102,1,0,0,0,102,104,1,0,0,0,103,101,1,0,
        0,0,104,105,5,6,0,0,105,106,3,16,8,0,106,108,5,20,0,0,107,109,3,
        18,9,0,108,107,1,0,0,0,109,110,1,0,0,0,110,108,1,0,0,0,110,111,1,
        0,0,0,111,15,1,0,0,0,112,113,7,1,0,0,113,17,1,0,0,0,114,116,5,26,
        0,0,115,114,1,0,0,0,116,119,1,0,0,0,117,115,1,0,0,0,117,118,1,0,
        0,0,118,120,1,0,0,0,119,117,1,0,0,0,120,121,5,8,0,0,121,122,5,25,
        0,0,122,125,3,12,6,0,123,124,5,9,0,0,124,126,3,20,10,0,125,123,1,
        0,0,0,125,126,1,0,0,0,126,127,1,0,0,0,127,128,5,20,0,0,128,129,3,
        28,14,0,129,19,1,0,0,0,130,135,3,22,11,0,131,132,5,11,0,0,132,134,
        3,22,11,0,133,131,1,0,0,0,134,137,1,0,0,0,135,133,1,0,0,0,135,136,
        1,0,0,0,136,21,1,0,0,0,137,135,1,0,0,0,138,143,3,24,12,0,139,140,
        5,10,0,0,140,142,3,24,12,0,141,139,1,0,0,0,142,145,1,0,0,0,143,141,
        1,0,0,0,143,144,1,0,0,0,144,23,1,0,0,0,145,143,1,0,0,0,146,148,5,
        12,0,0,147,146,1,0,0,0,147,148,1,0,0,0,148,149,1,0,0,0,149,150,3,
        26,13,0,150,25,1,0,0,0,151,152,5,25,0,0,152,158,3,12,6,0,153,154,
        5,22,0,0,154,155,3,20,10,0,155,156,5,23,0,0,156,158,1,0,0,0,157,
        151,1,0,0,0,157,153,1,0,0,0,158,27,1,0,0,0,159,164,3,30,15,0,160,
        161,5,21,0,0,161,163,3,30,15,0,162,160,1,0,0,0,163,166,1,0,0,0,164,
        162,1,0,0,0,164,165,1,0,0,0,165,167,1,0,0,0,166,164,1,0,0,0,167,
        168,5,19,0,0,168,29,1,0,0,0,169,170,5,13,0,0,170,171,5,14,0,0,171,
        178,5,25,0,0,172,173,5,13,0,0,173,174,5,15,0,0,174,178,5,25,0,0,
        175,176,5,13,0,0,176,178,5,25,0,0,177,169,1,0,0,0,177,172,1,0,0,
        0,177,175,1,0,0,0,178,31,1,0,0,0,17,35,41,49,56,63,70,74,101,110,
        117,125,135,143,147,157,164,177
    ]

class RegiaScriptParser ( Parser ):

    grammarFileName = "RegiaScript.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'STORY'", "'ACTION'", "'EVENT'", "'CONDITION'", 
                     "'PRIORITY'", "'DURING'", "'ALWAYS'", "'WHEN'", "'IF'", 
                     "'AND'", "'OR'", "'NOT'", "'DO'", "'BELIEVE'", "'FORGET'", 
                     "'ENVIRONMENT'", "'DIRECTOR'", "'MYSELF'", "'.'", "':'", 
                     "','", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "STORY", "ACTION", "EVENT", "CONDITION", 
                      "PRIORITY", "DURING", "ALWAYS", "WHEN", "IF", "AND", 
                      "OR", "NOT", "DO", "BELIEVE", "FORGET", "ENVIRONMENT", 
                      "DIRECTOR", "MYSELF", "PERIOD", "COLON", "COMMA", 
                      "LPAREN", "RPAREN", "NUMBER", "ID", "DOC_COMMENT", 
                      "COMMENT", "WS" ]

    RULE_program = 0
    RULE_declaration = 1
    RULE_storyDecl = 2
    RULE_actionDecl = 3
    RULE_eventDecl = 4
    RULE_conditionDecl = 5
    RULE_origin = 6
    RULE_duringBlock = 7
    RULE_storyRef = 8
    RULE_whenBlock = 9
    RULE_condExpr = 10
    RULE_condAnd = 11
    RULE_condTerm = 12
    RULE_condAtom = 13
    RULE_doSequence = 14
    RULE_doAction = 15

    ruleNames =  [ "program", "declaration", "storyDecl", "actionDecl", 
                   "eventDecl", "conditionDecl", "origin", "duringBlock", 
                   "storyRef", "whenBlock", "condExpr", "condAnd", "condTerm", 
                   "condAtom", "doSequence", "doAction" ]

    EOF = Token.EOF
    STORY=1
    ACTION=2
    EVENT=3
    CONDITION=4
    PRIORITY=5
    DURING=6
    ALWAYS=7
    WHEN=8
    IF=9
    AND=10
    OR=11
    NOT=12
    DO=13
    BELIEVE=14
    FORGET=15
    ENVIRONMENT=16
    DIRECTOR=17
    MYSELF=18
    PERIOD=19
    COLON=20
    COMMA=21
    LPAREN=22
    RPAREN=23
    NUMBER=24
    ID=25
    DOC_COMMENT=26
    COMMENT=27
    WS=28

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(RegiaScriptParser.EOF, 0)

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.DeclarationContext,i)


        def duringBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.DuringBlockContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.DuringBlockContext,i)


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
            self.state = 35
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 32
                    self.declaration() 
                self.state = 37
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6 or _la==26:
                self.state = 38
                self.duringBlock()
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 44
            self.match(RegiaScriptParser.EOF)
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

        def storyDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.StoryDeclContext,0)


        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def actionDecl(self):
            return self.getTypedRuleContext(RegiaScriptParser.ActionDeclContext,0)


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
        self.enterRule(localctx, 2, self.RULE_declaration)
        self._la = 0 # Token type
        try:
            self.state = 74
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==26:
                    self.state = 46
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 51
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 52
                self.storyDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 56
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==26:
                    self.state = 53
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 58
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 59
                self.actionDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==26:
                    self.state = 60
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 65
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 66
                self.eventDecl()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 70
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==26:
                    self.state = 67
                    self.match(RegiaScriptParser.DOC_COMMENT)
                    self.state = 72
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 73
                self.conditionDecl()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StoryDeclContext(ParserRuleContext):
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

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_storyDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStoryDecl" ):
                listener.enterStoryDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStoryDecl" ):
                listener.exitStoryDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStoryDecl" ):
                return visitor.visitStoryDecl(self)
            else:
                return visitor.visitChildren(self)




    def storyDecl(self):

        localctx = RegiaScriptParser.StoryDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_storyDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(RegiaScriptParser.STORY)
            self.state = 77
            self.match(RegiaScriptParser.ID)
            self.state = 78
            self.match(RegiaScriptParser.PRIORITY)
            self.state = 79
            self.match(RegiaScriptParser.NUMBER)
            self.state = 80
            self.match(RegiaScriptParser.PERIOD)
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
        self.enterRule(localctx, 6, self.RULE_actionDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(RegiaScriptParser.ACTION)
            self.state = 83
            self.match(RegiaScriptParser.ID)
            self.state = 84
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
        self.enterRule(localctx, 8, self.RULE_eventDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(RegiaScriptParser.EVENT)
            self.state = 87
            self.match(RegiaScriptParser.ID)
            self.state = 88
            self.origin()
            self.state = 89
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
        self.enterRule(localctx, 10, self.RULE_conditionDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(RegiaScriptParser.CONDITION)
            self.state = 92
            self.match(RegiaScriptParser.ID)
            self.state = 93
            self.origin()
            self.state = 94
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
        self.enterRule(localctx, 12, self.RULE_origin)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 458752) != 0)):
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


    class DuringBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DURING(self):
            return self.getToken(RegiaScriptParser.DURING, 0)

        def storyRef(self):
            return self.getTypedRuleContext(RegiaScriptParser.StoryRefContext,0)


        def COLON(self):
            return self.getToken(RegiaScriptParser.COLON, 0)

        def DOC_COMMENT(self, i:int=None):
            if i is None:
                return self.getTokens(RegiaScriptParser.DOC_COMMENT)
            else:
                return self.getToken(RegiaScriptParser.DOC_COMMENT, i)

        def whenBlock(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RegiaScriptParser.WhenBlockContext)
            else:
                return self.getTypedRuleContext(RegiaScriptParser.WhenBlockContext,i)


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
        self.enterRule(localctx, 14, self.RULE_duringBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 98
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 103
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 104
            self.match(RegiaScriptParser.DURING)
            self.state = 105
            self.storyRef()
            self.state = 106
            self.match(RegiaScriptParser.COLON)
            self.state = 108 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 107
                    self.whenBlock()

                else:
                    raise NoViableAltException(self)
                self.state = 110 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StoryRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(RegiaScriptParser.ID, 0)

        def ALWAYS(self):
            return self.getToken(RegiaScriptParser.ALWAYS, 0)

        def getRuleIndex(self):
            return RegiaScriptParser.RULE_storyRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStoryRef" ):
                listener.enterStoryRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStoryRef" ):
                listener.exitStoryRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStoryRef" ):
                return visitor.visitStoryRef(self)
            else:
                return visitor.visitChildren(self)




    def storyRef(self):

        localctx = RegiaScriptParser.StoryRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_storyRef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            _la = self._input.LA(1)
            if not(_la==7 or _la==25):
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
        self.enterRule(localctx, 18, self.RULE_whenBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 114
                self.match(RegiaScriptParser.DOC_COMMENT)
                self.state = 119
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 120
            self.match(RegiaScriptParser.WHEN)
            self.state = 121
            self.match(RegiaScriptParser.ID)
            self.state = 122
            self.origin()
            self.state = 125
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 123
                self.match(RegiaScriptParser.IF)
                self.state = 124
                self.condExpr()


            self.state = 127
            self.match(RegiaScriptParser.COLON)
            self.state = 128
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
        self.enterRule(localctx, 20, self.RULE_condExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            self.condAnd()
            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11:
                self.state = 131
                self.match(RegiaScriptParser.OR)
                self.state = 132
                self.condAnd()
                self.state = 137
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
        self.enterRule(localctx, 22, self.RULE_condAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.condTerm()
            self.state = 143
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10:
                self.state = 139
                self.match(RegiaScriptParser.AND)
                self.state = 140
                self.condTerm()
                self.state = 145
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
        self.enterRule(localctx, 24, self.RULE_condTerm)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==12:
                self.state = 146
                self.match(RegiaScriptParser.NOT)


            self.state = 149
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
        self.enterRule(localctx, 26, self.RULE_condAtom)
        try:
            self.state = 157
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [25]:
                self.enterOuterAlt(localctx, 1)
                self.state = 151
                self.match(RegiaScriptParser.ID)
                self.state = 152
                self.origin()
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 2)
                self.state = 153
                self.match(RegiaScriptParser.LPAREN)
                self.state = 154
                self.condExpr()
                self.state = 155
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
        self.enterRule(localctx, 28, self.RULE_doSequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 159
            self.doAction()
            self.state = 164
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==21:
                self.state = 160
                self.match(RegiaScriptParser.COMMA)
                self.state = 161
                self.doAction()
                self.state = 166
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 167
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
        self.enterRule(localctx, 30, self.RULE_doAction)
        try:
            self.state = 177
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                self.match(RegiaScriptParser.DO)
                self.state = 170
                self.match(RegiaScriptParser.BELIEVE)
                self.state = 171
                self.match(RegiaScriptParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 172
                self.match(RegiaScriptParser.DO)
                self.state = 173
                self.match(RegiaScriptParser.FORGET)
                self.state = 174
                self.match(RegiaScriptParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 175
                self.match(RegiaScriptParser.DO)
                self.state = 176
                self.match(RegiaScriptParser.ID)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





