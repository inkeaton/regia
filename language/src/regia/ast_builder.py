"""
AST builder for the Regia compiler.

Transforms a Lark parse tree into our typed AST (defined in ast_nodes).
Uses Lark's Transformer pattern: each method is named after a grammar
rule and is called bottom-up after its children have already been
transformed.

This is the ONLY module that knows about the Lark Tree structure.
All downstream passes (validation, emission) work exclusively on
the typed AST.

How Lark's Transformer works:
    1. Lark walks the tree from leaves to root.
    2. For each node, it calls the method matching the rule name.
    3. The method receives its children ALREADY TRANSFORMED.
    4. Rules prefixed with ? in the grammar are inlined (no method
       needed). Rules with -> aliases use the alias as method name.
    5. @v_args(meta=True) gives access to source positions from the
       tree's metadata (requires propagate_positions=True on parser).
    6. @v_args(inline=True) unpacks children as positional args
       (only for rules with a fixed number of children).
"""

from typing import Any, List, Optional, Tuple, Union

from lark import Transformer, Token, v_args

from regia.ast_nodes import (
    # Shared
    SourceLoc, Arg, EventOrigin, SPECIAL_ACTIONS,
    # Imports
    ImportDecl,
    # Base elements
    ActionDecl, EventDecl, FactDecl,
    # Conditions
    FactRef, ConditionNot, ConditionAnd, ConditionOr, ConditionExpr,
    # Playbook
    DoStmt, SignalStmt, PbIfBranch, PbElseBranch, PbWhenBlock, PlaybookDef,
    # Temper (VEsNA)
    TemperEntry, TemperSpec,
    # Imperative
    AssignStmt, UnassignStmt, WorldDoStmt, RoleDoStmt,
    InlineTransitionStmt, RoleMapping, StartSubplotStmt, PlotEndStmt,
    # Plot
    OnEnter, OnExit,
    PlotIfBranch, PlotElseBranch, PlotWhenBlock, PlotWhenSubplotEndsBlock,
    DuringBlock, PhaseDecl, RoleDecl, PlotDef,
    # Root
    Program,
)


# == Internal helpers ==========================================================
# These small types are used to pass intermediate results between
# Transformer methods. They never appear in the final AST.

class _ActionInfo:
    """Intermediate result from action_name rule.

    Bundles the action name string and whether it is a special
    AgentSpeak primitive, so that do_stmt / world_do_stmt /
    role_do_stmt can consume both values cleanly.
    """

    __slots__ = ("name", "is_special") # memory optimization

    def __init__(self, name: str, is_special: bool) -> None:
        self.name = name
        self.is_special = is_special


def _meta_loc(meta: Any, filename: str = "") -> SourceLoc:
    """Extract a SourceLoc from a Lark tree's Meta object.

    With propagate_positions=True, every Tree node gets a .meta
    with .line and .column pointing to the FIRST terminal in the
    rule (including filtered keywords like "DO", "WHEN", etc.).

    Args:
        meta:     The Lark Meta object from @v_args(meta=True).
        filename: The source file name to embed in the SourceLoc.

    Returns:
        A SourceLoc with the extracted position.
    """
    line = getattr(meta, "line", 0) or 0
    column = getattr(meta, "column", 0) or 0
    return SourceLoc(line=line, column=column, filename=filename)


def _token_loc(token: Token, filename: str = "") -> SourceLoc:
    """Extract a SourceLoc from a Lark Token.

    Args:
        token:    A Lark Token with .line and .column attributes.
        filename: The source file name to embed in the SourceLoc.

    Returns:
        A SourceLoc with the token's position.
    """
    return SourceLoc(
        line=getattr(token, "line", 0) or 0,
        column=getattr(token, "column", 0) or 0,
        filename=filename,
    )


# == Transformer ===============================================================

class ASTBuilder(Transformer):
    """Bottom-up Transformer: Lark Tree -> typed AST nodes.

    Method names match grammar rule names (or -> aliases) exactly.
    Methods decorated with @v_args(meta=True) receive (meta, children)
    where meta carries source position info. Methods decorated with
    @v_args(inline=True) receive children as positional args.

    Rules prefixed with ? in the grammar (element_decl, pb_stmt, etc.)
    are inlined by Lark and do NOT need methods here.
    """

    def __init__(self, filename: str = "") -> None:
        """Initialise the builder with an optional source filename.

        Args:
            filename: The name of the source file being built.
                      Embedded into every SourceLoc for multi-file
                      error reporting.
        """
        super().__init__()
        self._filename: str = filename

    # == Import declarations ===================================================

    @v_args(meta=True)
    def import_stmt(self, meta: Any, children: List) -> ImportDecl:
        """IMPORT \"path\"  -> import declaration.

        Args:
            meta:     Position of the IMPORT keyword.
            children: [Token(STRING, path)].

        Returns:
            An ImportDecl AST node.
        """
        path_token = children[0]
        # Strip surrounding quotes from the STRING token
        raw = str(path_token)
        path = raw[1:-1] if raw.startswith('"') else raw
        return ImportDecl(
            path=path,
            loc=_meta_loc(meta, self._filename),
        )

    # == Base element declarations =============================================

    @v_args(meta=True)
    def action_decl(self, meta: Any, children: List) -> ActionDecl:
        """ACTION greet. or ACTION give_item(item, target).

        Args:
            meta:     Position of the ACTION keyword.
            children: [Token(ID, name), optional List[str] from param_names].

        Returns:
            An ActionDecl AST node.
        """
        name_token = children[0]
        params = []
        alias = None
        
        for child in children[1:]:
            if isinstance(child, list):
                params = child
            elif isinstance(child, Token):
                alias = str(child)

        return ActionDecl(
            name=str(name_token),
            params=params,
            alias=alias,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def event_decl(self, meta: Any, children: List) -> EventDecl:
        """EVENT fan_greets. or EVENT check SELF.

        Args:
            meta:     Position of the EVENT keyword.
            children: [Token(ID, name), optional EventOrigin].

        Returns:
            An EventDecl AST node.
        """
        name_token = children[0]
        origin = children[1] if len(children) > 1 else None
        return EventDecl(
            name=str(name_token),
            origin=origin,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def fact_decl(self, meta: Any, children: List) -> FactDecl:
        """FACT happy. or FACT has_item(item).

        Args:
            meta:     Position of the FACT keyword.
            children: [Token(ID, name), optional List[str] from param_names].

        Returns:
            A FactDecl AST node.
        """
        name_token = children[0]
        params = children[1] if len(children) > 1 else []
        return FactDecl(
            name=str(name_token),
            params=params,
            loc=_meta_loc(meta, self._filename),
        )

    def param_names(self, children: List[Token]) -> List[str]:
        """(name1, name2, ...) -> list of parameter name strings.

        Args:
            children: List of ID tokens.

        Returns:
            A plain list of strings (consumed by action_decl/fact_decl).
        """
        return [str(t) for t in children]

    @v_args(inline=True)
    def event_origin(self, token: Token) -> EventOrigin:
        """SELF or ENVIRONMENT -> EventOrigin enum.

        Args:
            token: A SELF or ENVIRONMENT terminal token.

        Returns:
            The corresponding EventOrigin enum value.
        """
        return EventOrigin(str(token))

    # == Arguments and action names ============================================

    @v_args(inline=True, meta=True)
    def arg(self, meta: Any, token: Token) -> Arg:
        """ID | NUMBER | STRING -> Arg.

        Args:
            meta:  Position of the argument.
            token: The terminal token.

        Returns:
            An Arg AST node.
        """
        if token.type == "NUMBER":
            return Arg(value=int(token), is_string=False, loc=_meta_loc(meta, self._filename))
        elif token.type == "STRING":
            # Strip the surrounding quotes
            val = str(token)[1:-1]
            return Arg(value=val, is_string=True, loc=_meta_loc(meta, self._filename))
        return Arg(value=str(token), is_string=False, loc=_meta_loc(meta, self._filename))

    def arg_list(self, children: List[Arg]) -> List[Arg]:
        """(arg1, arg2, ...) -> list of Args.

        Args:
            children: List of already-transformed Arg objects.

        Returns:
            The same list (pass-through for parent to consume).
        """
        return list(children)

    @v_args(inline=True)
    def action_name(self, token: Token) -> _ActionInfo:
        """ID or TELL/BROADCAST/etc -> action info bundle.

        This intermediate result is consumed by do_stmt,
        world_do_stmt, and role_do_stmt to populate their
        action name and is_special fields.

        Args:
            token: An ID or special-action terminal token.

        Returns:
            An _ActionInfo with name and is_special flag.
        """
        name = str(token)
        return _ActionInfo(name=name, is_special=name in SPECIAL_ACTIONS)

    @v_args(inline=True)
    def priority(self, num_token: Token) -> int:
        """PRIORITY NUMBER -> integer value.

        Args:
            num_token: The NUMBER terminal token.

        Returns:
            The priority as a plain int (consumed by when block methods).
        """
        return int(num_token)

    # == Temper annotations (VEsNA) ============================================

    @v_args(inline=True)
    def temper_entry(self, name_token: Token, value_token: Token) -> TemperEntry:
        """ID "(" FLOAT ")" -> TemperEntry.

        Args:
            name_token:  The dimension name (e.g. sympathy).
            value_token: The FLOAT token (e.g. 0.8).

        Returns:
            A TemperEntry with name and float value.
        """
        return TemperEntry(name=str(name_token), value=float(value_token))

    def effects(self, children: List) -> List[TemperEntry]:
        """EFFECTS temper_entry+ -> list of TemperEntry.

        Args:
            children: One or more TemperEntry nodes.

        Returns:
            The list of TemperEntry objects for the effects.
        """
        return list(children)

    def temper(self, children: List) -> TemperSpec:
        """TEMPER temper_entry+ effects? -> TemperSpec.

        Args:
            children: One or more TemperEntry nodes, optionally
                      followed by a list of TemperEntry (the effects).

        Returns:
            A TemperSpec with dimensions and optional effects.
        """
        dimensions: List[TemperEntry] = []
        effects_list: List[TemperEntry] = []

        for child in children:
            if isinstance(child, TemperEntry):
                dimensions.append(child)
            elif isinstance(child, list):
                # The effects rule returns a list of TemperEntry
                effects_list = child

        return TemperSpec(dimensions=dimensions, effects=effects_list)

    # == Playbook actions ======================================================

    @v_args(meta=True)
    def do_stmt(self, meta: Any, children: List) -> DoStmt:
        """DO action(args). -> self-directed action.

        Args:
            meta:     Position of the DO keyword.
            children: [_ActionInfo, optional List[Arg]].

        Returns:
            A DoStmt AST node.
        """
        info = children[0]
        args = children[1] if len(children) > 1 else []
        return DoStmt(
            action=info.name,
            is_special=info.is_special,
            args=args,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def signal_stmt(self, meta: Any, children: List) -> SignalStmt:
        """SIGNAL event(args). -> signal to the Director.

        Args:
            meta:     Position of the SIGNAL keyword.
            children: [Token(ID, event), optional List[Arg]].

        Returns:
            A SignalStmt AST node.
        """
        event_token = children[0]
        args = children[1] if len(children) > 1 else []
        return SignalStmt(
            event=str(event_token),
            args=args,
            loc=_meta_loc(meta, self._filename),
        )

    # == Playbook WHEN blocks ==================================================

    @v_args(meta=True)
    def pb_if_branch(self, meta: Any, children: List) -> PbIfBranch:
        """IF condition: stmt+ -> conditional branch.

        Args:
            meta:     Position of the IF keyword.
            children: [ConditionExpr, DoStmt|SignalStmt, ...].

        Returns:
            A PbIfBranch AST node.
        """
        return PbIfBranch(
            condition=children[0],
            stmts=list(children[1:]),
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def pb_else_branch(self, meta: Any, children: List) -> PbElseBranch:
        """ELSE: stmt+ -> fallback branch.

        Args:
            meta:     Position of the ELSE keyword.
            children: [DoStmt|SignalStmt, ...].

        Returns:
            A PbElseBranch AST node.
        """
        return PbElseBranch(stmts=list(children), loc=_meta_loc(meta, self._filename))

    def pb_when_body(
        self,
        children: List,
    ) -> Tuple[List, List[PbIfBranch], Optional[PbElseBranch]]:
        """Body of a Playbook WHEN block -> (prefix, branches, else).

        Classifies the flat list of children (produced by ? inlining)
        into three categories for the parent pb_when_block:
          1. prefix_stmts:  DoStmt/SignalStmt that appear before branches
          2. branches:      PbIfBranch objects
          3. else_branch:   optional PbElseBranch

        The validator (Pass 4) checks that prefix stmts come before
        branches (no interleaving).

        Args:
            children: Flat list of DoStmt, SignalStmt, PbIfBranch,
                      and optionally one PbElseBranch at the end.

        Returns:
            A (prefix_stmts, branches, else_branch) tuple.
        """
        prefix_stmts: List[Union[DoStmt, SignalStmt]] = []
        branches: List[PbIfBranch] = []
        else_branch: Optional[PbElseBranch] = None

        for child in children:
            if isinstance(child, PbElseBranch):
                else_branch = child
            elif isinstance(child, PbIfBranch):
                branches.append(child)
            else:
                # DoStmt or SignalStmt
                prefix_stmts.append(child)

        return (prefix_stmts, branches, else_branch)

    @v_args(meta=True)
    def pb_when_block(self, meta: Any, children: List) -> PbWhenBlock:
        """WHEN event PRIORITY n TEMPER ...: body -> reactive plan.

        Args:
            meta:     Position of the WHEN keyword.
            children: [Token(ID, event), optional int, optional TemperSpec,
                       body_tuple]. Variable length due to optional
                       priority and temper.

        Returns:
            A PbWhenBlock AST node with separated body parts.
        """
        event_token = children[0]

        # Determine optional children by type inspection
        priority_val: Optional[int] = None
        temper_val: Optional[TemperSpec] = None
        body = children[-1]  # Body is always the last child

        for child in children[1:-1]:
            if isinstance(child, int):
                priority_val = child
            elif isinstance(child, TemperSpec):
                temper_val = child

        prefix_stmts, branches, else_branch = body
        return PbWhenBlock(
            event=str(event_token),
            priority=priority_val,
            temper=temper_val,
            prefix_stmts=prefix_stmts,
            branches=branches,
            else_branch=else_branch,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def playbook_def(self, meta: Any, children: List) -> PlaybookDef:
        """PLAYBOOK Name: when_blocks -> Playbook definition.

        Args:
            meta:     Position of the PLAYBOOK keyword.
            children: [Token(ID, name), PbWhenBlock, PbWhenBlock, ...].

        Returns:
            A PlaybookDef AST node.
        """
        name_token = children[0]
        return PlaybookDef(
            name=str(name_token),
            when_blocks=list(children[1:]),
            loc=_meta_loc(meta, self._filename),
        )

    # == Conditions ============================================================

    @v_args(meta=True)
    def fact_ref(self, meta: Any, children: List) -> FactRef:
        """fact_name or fact_name(arg1, arg2) -> fact reference.

        Args:
            meta:     Position of the fact name.
            children: [Token(ID, name), optional Arg, Arg, ...].

        Returns:
            A FactRef AST node.
        """
        name_token = children[0]
        args = [c for c in children[1:] if c is not None]
        return FactRef(
            name=str(name_token),
            args=args,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def condition(self, meta: Any, children: List[ConditionExpr]) -> ConditionExpr:
        """condition_and OR condition_and OR ... -> ConditionOr or collapse.

        If there is only one operand (no OR), the wrapper is collapsed:
        the single child is returned directly. This keeps simple
        conditions like 'IF happy:' as just a FactRef, not a
        nested ConditionOr > ConditionAnd > FactRef chain.

        Args:
            meta:     Position of the first operand.
            children: List of condition_and results.

        Returns:
            A ConditionOr (if 2+ operands) or the single child.
        """
        if len(children) == 1:
            return children[0]
        return ConditionOr(operands=list(children), loc=_meta_loc(meta, self._filename))

    @v_args(meta=True)
    def condition_and(
        self,
        meta: Any,
        children: List[ConditionExpr],
    ) -> ConditionExpr:
        """condition_atom AND condition_atom AND ... -> ConditionAnd or collapse.

        Same collapsing logic as condition(): single operand is
        returned directly.

        Args:
            meta:     Position of the first operand.
            children: List of condition_atom results.

        Returns:
            A ConditionAnd (if 2+ operands) or the single child.
        """
        if len(children) == 1:
            return children[0]
        return ConditionAnd(operands=list(children), loc=_meta_loc(meta, self._filename))

    @v_args(meta=True)
    def condition_not(self, meta: Any, children: List) -> ConditionNot:
        """NOT condition_atom -> negation.

        Args:
            meta:     Position of the NOT keyword.
            children: [ConditionExpr (the negated inner expression)].

        Returns:
            A ConditionNot AST node.
        """
        return ConditionNot(operand=children[0], loc=_meta_loc(meta, self._filename))

    @v_args(meta=True)
    def condition_group(self, meta: Any, children: List) -> ConditionExpr:
        """(condition) -> unwrap parentheses.

        Parentheses served their purpose during parsing (overriding
        precedence). The AST does not need to remember them; the
        inner condition is returned directly.

        Args:
            meta:     Position of the opening parenthesis.
            children: [ConditionExpr (the inner condition)].

        Returns:
            The inner ConditionExpr, unwrapped.
        """
        return children[0]

    # == Imperative statements =================================================

    @v_args(meta=True)
    def assign_stmt(self, meta: Any, children: List[Token]) -> AssignStmt:
        """ASSIGN Playbook TO Role. -> assignment.

        Args:
            meta:     Position of the ASSIGN keyword.
            children: [Token(ID, playbook), Token(ID, role)].

        Returns:
            An AssignStmt AST node.
        """
        return AssignStmt(
            playbook=str(children[0]),
            role=str(children[1]),
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def unassign_stmt(self, meta: Any, children: List[Token]) -> UnassignStmt:
        """UNASSIGN Playbook FROM Role. -> removal.

        Args:
            meta:     Position of the UNASSIGN keyword.
            children: [Token(ID, playbook), Token(ID, role)].

        Returns:
            An UnassignStmt AST node.
        """
        return UnassignStmt(
            playbook=str(children[0]),
            role=str(children[1]),
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def world_do_stmt(self, meta: Any, children: List) -> WorldDoStmt:
        """WORLD DO action(args). -> director-executed action.

        Args:
            meta:     Position of the WORLD keyword.
            children: [_ActionInfo, optional List[Arg]].

        Returns:
            A WorldDoStmt AST node.
        """
        info = children[0]
        args = children[1] if len(children) > 1 else []
        return WorldDoStmt(
            action=info.name,
            is_special=info.is_special,
            args=args,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def role_do_stmt(self, meta: Any, children: List) -> RoleDoStmt:
        """Role DO action(args). -> role-directed action.

        Args:
            meta:     Position of the Role name token.
            children: [Token(ID, role), _ActionInfo, optional List[Arg]].

        Returns:
            A RoleDoStmt AST node.
        """
        role_token = children[0]
        info = children[1]
        args = children[2] if len(children) > 2 else []
        return RoleDoStmt(
            role=str(role_token),
            action=info.name,
            is_special=info.is_special,
            args=args,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def inline_transition_stmt(
        self,
        meta: Any,
        children: List,
    ) -> InlineTransitionStmt:
        """TRANSITION TO phase. -> inline phase transition.

        Used as the last statement of a WHEN body or branch body.
        The trigger and guard are provided by the enclosing WHEN block
        and IF branch.

        Args:
            meta:     Position of the TRANSITION keyword.
            children: [Token(ID, target_phase)].

        Returns:
            An InlineTransitionStmt AST node.
        """
        target_token = children[0]
        return InlineTransitionStmt(
            target_phase=str(target_token),
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def role_mapping(self, meta: Any, children: List[Token]) -> RoleMapping:
        """SourceRole TO TargetRole -> a single role binding.

        Args:
            meta:     Position of the source role token.
            children: [Token(ID, source_role), Token(ID, target_role)].

        Returns:
            A RoleMapping AST node.
        """
        return RoleMapping(
            source_role=str(children[0]),
            target_role=str(children[1]),
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def start_subplot_stmt(
        self,
        meta: Any,
        children: List,
    ) -> StartSubplotStmt:
        """START SUBPLOT PlotName [MAPPING ...]. -> child plot spawn.

        The MAPPING clause is optional: if present, children contains
        the plot-name token followed by one or more RoleMapping objects.
        If absent, only the plot-name token is present.

        Args:
            meta:     Position of the START keyword.
            children: [Token(ID, plot_name), optional RoleMapping, ...].

        Returns:
            A StartSubplotStmt AST node.
        """
        plot_name_token = children[0]
        mappings = [
            c for c in children[1:]
            if isinstance(c, RoleMapping)
        ]
        return StartSubplotStmt(
            plot_name=str(plot_name_token),
            mappings=mappings,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def plot_end_stmt(self, meta: Any, children: List) -> PlotEndStmt:
        """END PLOT. -> terminate the current Plot.

        Args:
            meta:     Position of the END keyword.
            children: [] (no children; keywords are filtered).

        Returns:
            A PlotEndStmt AST node.
        """
        return PlotEndStmt(loc=_meta_loc(meta, self._filename))

    # == Plot WHEN blocks ======================================================

    @v_args(meta=True)
    def plot_if_branch(self, meta: Any, children: List) -> PlotIfBranch:
        """IF condition: imperative_stmt+ -> conditional branch (plot).

        Args:
            meta:     Position of the IF keyword.
            children: [ConditionExpr, ImperativeStmt, ...].

        Returns:
            A PlotIfBranch AST node.
        """
        return PlotIfBranch(
            condition=children[0],
            stmts=list(children[1:]),
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def plot_else_branch(self, meta: Any, children: List) -> PlotElseBranch:
        """ELSE: imperative_stmt+ -> fallback branch (plot).

        Args:
            meta:     Position of the ELSE keyword.
            children: [ImperativeStmt, ...].

        Returns:
            A PlotElseBranch AST node.
        """
        return PlotElseBranch(stmts=list(children), loc=_meta_loc(meta, self._filename))

    def plot_when_body(
        self,
        children: List,
    ) -> Tuple[List, List[PlotIfBranch], Optional[PlotElseBranch]]:
        """Body of a Plot WHEN block -> (prefix, branches, else).

        Same logic as pb_when_body but for imperative statements.

        Args:
            children: Flat list of ImperativeStmt, PlotIfBranch,
                      and optionally one PlotElseBranch at the end.

        Returns:
            A (prefix_stmts, branches, else_branch) tuple.
        """
        prefix_stmts: List = []
        branches: List[PlotIfBranch] = []
        else_branch: Optional[PlotElseBranch] = None

        for child in children:
            if isinstance(child, PlotElseBranch):
                else_branch = child
            elif isinstance(child, PlotIfBranch):
                branches.append(child)
            else:
                # AssignStmt, UnassignStmt, WorldDoStmt, or RoleDoStmt
                prefix_stmts.append(child)

        return (prefix_stmts, branches, else_branch)

    @v_args(meta=True)
    def plot_when_block(self, meta: Any, children: List) -> PlotWhenBlock:
        """WHEN event PRIORITY n: body -> director-centric reactive plan.

        Args:
            meta:     Position of the WHEN keyword.
            children: [Token(ID, event), optional int, body_tuple].

        Returns:
            A PlotWhenBlock AST node.
        """
        event_token = children[0]

        if len(children) == 3:
            priority_val = children[1]
            body = children[2]
        else:
            priority_val = None
            body = children[1]

        prefix_stmts, branches, else_branch = body
        return PlotWhenBlock(
            event=str(event_token),
            priority=priority_val,
            prefix_stmts=prefix_stmts,
            branches=branches,
            else_branch=else_branch,
            loc=_meta_loc(meta, self._filename),
        )


    @v_args(meta=True)
    def plot_when_subplot_ends_block(self, meta: Any, children: List) -> PlotWhenSubplotEndsBlock:
        """WHEN SUBPLOT name ENDS PRIORITY n: body -> director-centric reactive plan.

        Args:
            meta:     Position of the WHEN keyword.
            children: [Token(ID, name), optional int, body_tuple].

        Returns:
            A PlotWhenSubplotEndsBlock AST node.
        """
        subplot_name = str(children[0])

        if len(children) == 3:
            priority_val = children[1]
            body = children[2]
        else:
            priority_val = None
            body = children[1]

        prefix_stmts, branches, else_branch = body
        return PlotWhenSubplotEndsBlock(
            subplot_name=subplot_name,
            priority=priority_val,
            prefix_stmts=prefix_stmts,
            branches=branches,
            else_branch=else_branch,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def on_enter(self, meta: Any, children: List) -> OnEnter:
        """ON ENTER: imperative_stmt+ -> phase entry hook.

        Args:
            meta:     Position of the ON keyword.
            children: [ImperativeStmt, ...].

        Returns:
            An OnEnter AST node.
        """
        return OnEnter(stmts=list(children), loc=_meta_loc(meta, self._filename))

    @v_args(meta=True)
    def on_exit(self, meta: Any, children: List) -> OnExit:
        """ON EXIT: imperative_stmt+ -> phase exit hook.

        Args:
            meta:     Position of the ON keyword.
            children: [ImperativeStmt, ...].

        Returns:
            An OnExit AST node.
        """
        return OnExit(stmts=list(children), loc=_meta_loc(meta, self._filename))

    @v_args(meta=True)
    def initial_phase_decl(self, meta: Any, children: List[Token]) -> PhaseDecl:
        """PHASE name INITIAL. -> initial phase declaration.

        This is the -> alias for the first alternative of phase_decl
        in the grammar. The INITIAL keyword is filtered, so we know
        it was present from the method name alone.

        Args:
            meta:     Position of the PHASE keyword.
            children: [Token(ID, name)].

        Returns:
            A PhaseDecl with is_initial=True.
        """
        return PhaseDecl(
            name=str(children[0]),
            is_initial=True,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def phase_decl(self, meta: Any, children: List[Token]) -> PhaseDecl:
        """PHASE name. -> normal phase declaration.

        Args:
            meta:     Position of the PHASE keyword.
            children: [Token(ID, name)].

        Returns:
            A PhaseDecl with is_initial=False.
        """
        return PhaseDecl(
            name=str(children[0]),
            is_initial=False,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def role_decl(self, meta: Any, children: List[Token]) -> RoleDecl:
        """ROLE name. -> role declaration.

        Args:
            meta:     Position of the ROLE keyword.
            children: [Token(ID, name)].

        Returns:
            A RoleDecl AST node.
        """
        return RoleDecl(name=str(children[0]), loc=_meta_loc(meta, self._filename))

    def plot_header(
        self,
        children: List[Union[PhaseDecl, RoleDecl]],
    ) -> Tuple[List[PhaseDecl], List[RoleDecl]]:
        """(phase_decl | role_decl)+ -> (phases, roles).

        Separates the mixed list of header declarations into two
        typed lists for the parent plot_def to consume.

        Args:
            children: Mixed list of PhaseDecl and RoleDecl objects.

        Returns:
            A (phases, roles) tuple.
        """
        phases = [c for c in children if isinstance(c, PhaseDecl)]
        roles = [c for c in children if isinstance(c, RoleDecl)]
        return (phases, roles)

    # == Plot structure ========================================================

    def _sort_during_content(
        self,
        items: List,
    ) -> Tuple[
        List[OnEnter],
        List[OnExit],
        List[Union[PlotWhenBlock, PlotWhenSubplotEndsBlock]],
    ]:
        """Sort during_content items into typed lists.

        Called by during_phase and during_plot_wide to classify
        the flat children (produced by ?during_content inlining)
        into three categories for the DuringBlock.

        Args:
            items: Mixed list of during-block content items.

        Returns:
            A (on_enters, on_exits, when_blocks) tuple.
        """
        on_enters: List[OnEnter] = []
        on_exits: List[OnExit] = []
        when_blocks: List[Union[PlotWhenBlock, PlotWhenSubplotEndsBlock]] = []

        for item in items:
            if isinstance(item, OnEnter):
                on_enters.append(item)
            elif isinstance(item, OnExit):
                on_exits.append(item)
            elif isinstance(item, (PlotWhenBlock, PlotWhenSubplotEndsBlock)):
                when_blocks.append(item)

        return (on_enters, on_exits, when_blocks)

    @v_args(meta=True)
    def during_phase(self, meta: Any, children: List) -> DuringBlock:
        """DURING phase_name: content+ -> phase-specific block.

        This is the -> alias for the first alternative of during_block.

        Args:
            meta:     Position of the DURING keyword.
            children: [Token(ID, phase_name), content_items...].

        Returns:
            A DuringBlock with phase_name set to the phase identifier.
        """
        name_token = children[0]
        on_enters, on_exits, when_blocks = (
            self._sort_during_content(children[1:])
        )
        return DuringBlock(
            phase_name=str(name_token),
            on_enters=on_enters,
            on_exits=on_exits,
            when_blocks=when_blocks,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def during_plot_wide(self, meta: Any, children: List) -> DuringBlock:
        """DURING PLOT: content+ -> plot-wide block.

        This is the -> alias for the second alternative of during_block.
        The "PLOT" keyword is filtered (anonymous terminal), so children
        contain only content items.

        Args:
            meta:     Position of the DURING keyword.
            children: [content_items...].

        Returns:
            A DuringBlock with phase_name=None (plot-wide).
        """
        on_enters, on_exits, when_blocks = (
            self._sort_during_content(children)
        )
        return DuringBlock(
            phase_name=None,
            on_enters=on_enters,
            on_exits=on_exits,
            when_blocks=when_blocks,
            loc=_meta_loc(meta, self._filename),
        )

    @v_args(meta=True)
    def plot_def(self, meta: Any, children: List) -> PlotDef:
        """PLOT Name. header during_blocks -> Plot definition.

        Args:
            meta:     Position of the PLOT keyword.
            children: [Token(ID, name), (phases, roles) tuple,
                       DuringBlock, DuringBlock, ...].

        Returns:
            A PlotDef AST node.
        """
        name_token = children[0]
        phases, roles = children[1]
        during_blocks = list(children[2:])
        return PlotDef(
            name=str(name_token),
            phases=phases,
            roles=roles,
            during_blocks=during_blocks,
            loc=_meta_loc(meta, self._filename),
        )

    # == Root ==================================================================

    @v_args(meta=True)
    def program(self, meta: Any, children: List) -> Program:
        """Top-level program: all items -> root AST node.

        Args:
            meta:     Position of the first item.
            children: List of ActionDecl, EventDecl, FactDecl,
                      PlaybookDef, and PlotDef objects.

        Returns:
            The root Program AST node.
        """
        return Program(items=list(children))
