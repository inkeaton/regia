# Generated from grammars/RegiaScript.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .RegiaScriptParser import RegiaScriptParser
else:
    from RegiaScriptParser import RegiaScriptParser

# This class defines a complete listener for a parse tree produced by RegiaScriptParser.
class RegiaScriptListener(ParseTreeListener):

    # Enter a parse tree produced by RegiaScriptParser#program.
    def enterProgram(self, ctx:RegiaScriptParser.ProgramContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#program.
    def exitProgram(self, ctx:RegiaScriptParser.ProgramContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#storyDef.
    def enterStoryDef(self, ctx:RegiaScriptParser.StoryDefContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#storyDef.
    def exitStoryDef(self, ctx:RegiaScriptParser.StoryDefContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#defaultStory.
    def enterDefaultStory(self, ctx:RegiaScriptParser.DefaultStoryContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#defaultStory.
    def exitDefaultStory(self, ctx:RegiaScriptParser.DefaultStoryContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#namedStory.
    def enterNamedStory(self, ctx:RegiaScriptParser.NamedStoryContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#namedStory.
    def exitNamedStory(self, ctx:RegiaScriptParser.NamedStoryContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#declaration.
    def enterDeclaration(self, ctx:RegiaScriptParser.DeclarationContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#declaration.
    def exitDeclaration(self, ctx:RegiaScriptParser.DeclarationContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#actionDecl.
    def enterActionDecl(self, ctx:RegiaScriptParser.ActionDeclContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#actionDecl.
    def exitActionDecl(self, ctx:RegiaScriptParser.ActionDeclContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#eventDecl.
    def enterEventDecl(self, ctx:RegiaScriptParser.EventDeclContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#eventDecl.
    def exitEventDecl(self, ctx:RegiaScriptParser.EventDeclContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#conditionDecl.
    def enterConditionDecl(self, ctx:RegiaScriptParser.ConditionDeclContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#conditionDecl.
    def exitConditionDecl(self, ctx:RegiaScriptParser.ConditionDeclContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#origin.
    def enterOrigin(self, ctx:RegiaScriptParser.OriginContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#origin.
    def exitOrigin(self, ctx:RegiaScriptParser.OriginContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#phaseDecl.
    def enterPhaseDecl(self, ctx:RegiaScriptParser.PhaseDeclContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#phaseDecl.
    def exitPhaseDecl(self, ctx:RegiaScriptParser.PhaseDeclContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#agentBlock.
    def enterAgentBlock(self, ctx:RegiaScriptParser.AgentBlockContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#agentBlock.
    def exitAgentBlock(self, ctx:RegiaScriptParser.AgentBlockContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#agentSection.
    def enterAgentSection(self, ctx:RegiaScriptParser.AgentSectionContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#agentSection.
    def exitAgentSection(self, ctx:RegiaScriptParser.AgentSectionContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#duringBlock.
    def enterDuringBlock(self, ctx:RegiaScriptParser.DuringBlockContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#duringBlock.
    def exitDuringBlock(self, ctx:RegiaScriptParser.DuringBlockContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#phaseRef.
    def enterPhaseRef(self, ctx:RegiaScriptParser.PhaseRefContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#phaseRef.
    def exitPhaseRef(self, ctx:RegiaScriptParser.PhaseRefContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#whenBlock.
    def enterWhenBlock(self, ctx:RegiaScriptParser.WhenBlockContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#whenBlock.
    def exitWhenBlock(self, ctx:RegiaScriptParser.WhenBlockContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#condExpr.
    def enterCondExpr(self, ctx:RegiaScriptParser.CondExprContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#condExpr.
    def exitCondExpr(self, ctx:RegiaScriptParser.CondExprContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#condAnd.
    def enterCondAnd(self, ctx:RegiaScriptParser.CondAndContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#condAnd.
    def exitCondAnd(self, ctx:RegiaScriptParser.CondAndContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#condTerm.
    def enterCondTerm(self, ctx:RegiaScriptParser.CondTermContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#condTerm.
    def exitCondTerm(self, ctx:RegiaScriptParser.CondTermContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#condAtom.
    def enterCondAtom(self, ctx:RegiaScriptParser.CondAtomContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#condAtom.
    def exitCondAtom(self, ctx:RegiaScriptParser.CondAtomContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#doSequence.
    def enterDoSequence(self, ctx:RegiaScriptParser.DoSequenceContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#doSequence.
    def exitDoSequence(self, ctx:RegiaScriptParser.DoSequenceContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#doAction.
    def enterDoAction(self, ctx:RegiaScriptParser.DoActionContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#doAction.
    def exitDoAction(self, ctx:RegiaScriptParser.DoActionContext):
        pass



del RegiaScriptParser