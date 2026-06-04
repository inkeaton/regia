# Generated from grammars/RegiaScript.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .RegiaScriptParser import RegiaScriptParser
else:
    from RegiaScriptParser import RegiaScriptParser

# This class defines a complete generic visitor for a parse tree produced by RegiaScriptParser.

class RegiaScriptVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by RegiaScriptParser#program.
    def visitProgram(self, ctx:RegiaScriptParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#storyDef.
    def visitStoryDef(self, ctx:RegiaScriptParser.StoryDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#defaultStory.
    def visitDefaultStory(self, ctx:RegiaScriptParser.DefaultStoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#namedStory.
    def visitNamedStory(self, ctx:RegiaScriptParser.NamedStoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#declaration.
    def visitDeclaration(self, ctx:RegiaScriptParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#actionDecl.
    def visitActionDecl(self, ctx:RegiaScriptParser.ActionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#eventDecl.
    def visitEventDecl(self, ctx:RegiaScriptParser.EventDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#conditionDecl.
    def visitConditionDecl(self, ctx:RegiaScriptParser.ConditionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#origin.
    def visitOrigin(self, ctx:RegiaScriptParser.OriginContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#phaseDecl.
    def visitPhaseDecl(self, ctx:RegiaScriptParser.PhaseDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#agentBlock.
    def visitAgentBlock(self, ctx:RegiaScriptParser.AgentBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#agentSection.
    def visitAgentSection(self, ctx:RegiaScriptParser.AgentSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#duringBlock.
    def visitDuringBlock(self, ctx:RegiaScriptParser.DuringBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#phaseRef.
    def visitPhaseRef(self, ctx:RegiaScriptParser.PhaseRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#whenBlock.
    def visitWhenBlock(self, ctx:RegiaScriptParser.WhenBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#condExpr.
    def visitCondExpr(self, ctx:RegiaScriptParser.CondExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#condAnd.
    def visitCondAnd(self, ctx:RegiaScriptParser.CondAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#condTerm.
    def visitCondTerm(self, ctx:RegiaScriptParser.CondTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#condAtom.
    def visitCondAtom(self, ctx:RegiaScriptParser.CondAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#doSequence.
    def visitDoSequence(self, ctx:RegiaScriptParser.DoSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by RegiaScriptParser#doAction.
    def visitDoAction(self, ctx:RegiaScriptParser.DoActionContext):
        return self.visitChildren(ctx)



del RegiaScriptParser