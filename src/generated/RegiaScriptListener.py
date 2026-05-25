# Generated from grammars/RegiaScript.g4 by ANTLR 4.13.2
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


    # Enter a parse tree produced by RegiaScriptParser#declaration.
    def enterDeclaration(self, ctx:RegiaScriptParser.DeclarationContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#declaration.
    def exitDeclaration(self, ctx:RegiaScriptParser.DeclarationContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#storyDecl.
    def enterStoryDecl(self, ctx:RegiaScriptParser.StoryDeclContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#storyDecl.
    def exitStoryDecl(self, ctx:RegiaScriptParser.StoryDeclContext):
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


    # Enter a parse tree produced by RegiaScriptParser#duringBlock.
    def enterDuringBlock(self, ctx:RegiaScriptParser.DuringBlockContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#duringBlock.
    def exitDuringBlock(self, ctx:RegiaScriptParser.DuringBlockContext):
        pass


    # Enter a parse tree produced by RegiaScriptParser#storyRef.
    def enterStoryRef(self, ctx:RegiaScriptParser.StoryRefContext):
        pass

    # Exit a parse tree produced by RegiaScriptParser#storyRef.
    def exitStoryRef(self, ctx:RegiaScriptParser.StoryRefContext):
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