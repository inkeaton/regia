import pytest

from regia.ast_builder import ASTBuilder
from regia.ast_nodes import (
    StartSubplotStmt, RoleMapping, PlotEndStmt,
)
from regia.errors import ErrorReporter
from regia.parser import parse
from regia.validator import Validator
from regia.emitter import Emitter


@pytest.fixture
def parser():
    return parse


@pytest.fixture
def builder():
    return ASTBuilder("test.regia")


@pytest.fixture
def reporter():
    return ErrorReporter()


def parse_and_build(parser, builder, text):
    tree = parser(text)
    return builder.transform(tree)


# == Parsing Tests ==============================================================

def test_parse_start_subplot_with_mapping(parser, builder):
    src = """
    PLOT Test.
        PHASE one INITIAL.
        ROLE Hero.
        DURING one:
            ON ENTER:
                START SUBPLOT Child MAPPING Hero TO Fighter.
    """
    ast = parse_and_build(parser, builder, src)
    stmt = ast.items[0].during_blocks[0].on_enters[0].stmts[0]
    
    assert isinstance(stmt, StartSubplotStmt)
    assert stmt.plot_name == "Child"
    assert len(stmt.mappings) == 1
    assert stmt.mappings[0].source_role == "Hero"
    assert stmt.mappings[0].target_role == "Fighter"


def test_parse_start_subplot_without_mapping(parser, builder):
    src = """
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            ON ENTER:
                START SUBPLOT Cutscene.
    """
    ast = parse_and_build(parser, builder, src)
    stmt = ast.items[0].during_blocks[0].on_enters[0].stmts[0]
    
    assert isinstance(stmt, StartSubplotStmt)
    assert stmt.plot_name == "Cutscene"
    assert len(stmt.mappings) == 0


def test_parse_end_plot(parser, builder):
    src = """
    EVENT done.
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            WHEN done:
                END PLOT.
    """
    ast = parse_and_build(parser, builder, src)
    stmt = ast.items[1].during_blocks[0].when_blocks[0].prefix_stmts[0]
    
    assert isinstance(stmt, PlotEndStmt)


# == Validation Tests ==========================================================

def test_validator_error_on_unknown_subplot_target(parser, builder, reporter):
    src = """
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            ON ENTER:
                START SUBPLOT Missing.
    """
    ast = parse_and_build(parser, builder, src)
    validator = Validator(reporter)
    validator.validate(ast)
    
    assert reporter.has_errors()
    assert "undeclared plot: 'Missing'" in reporter.messages[0].message


def test_validator_error_on_invalid_source_role(parser, builder, reporter):
    src = """
    EVENT e.
    ACTION f.
    
    PLOT Child.
        PHASE a INITIAL.
        ROLE TargetRole.
        DURING PLOT:
            WHEN e:
                WORLD DO f.
    
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            ON ENTER:
                START SUBPLOT Child MAPPING MissingRole TO TargetRole.
    """
    ast = parse_and_build(parser, builder, src)
    validator = Validator(reporter)
    validator.validate(ast)
    
    assert reporter.has_errors()
    assert "source role 'MissingRole' is not declared" in reporter.messages[0].message


def test_validator_error_on_invalid_target_role(parser, builder, reporter):
    src = """
    EVENT e.
    ACTION f.
    
    PLOT Child.
        PHASE a INITIAL.
        DURING PLOT:
            WHEN e:
                WORLD DO f.
    
    PLOT Test.
        PHASE one INITIAL.
        ROLE SourceRole.
        DURING one:
            ON ENTER:
                START SUBPLOT Child MAPPING SourceRole TO MissingRole.
    """
    ast = parse_and_build(parser, builder, src)
    validator = Validator(reporter)
    validator.validate(ast)
    
    assert reporter.has_errors()
    assert "target role 'MissingRole' is not declared" in reporter.messages[0].message


def test_validator_warning_on_missing_mapping_for_roled_plot(parser, builder, reporter):
    src = """
    EVENT e.
    ACTION f.
    
    PLOT Child.
        PHASE a INITIAL.
        ROLE TargetRole.
        DURING PLOT:
            WHEN e:
                WORLD DO f.
        
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            ON ENTER:
                START SUBPLOT Child.
    """
    ast = parse_and_build(parser, builder, src)
    validator = Validator(reporter)
    validator.validate(ast)
    
    assert not reporter.has_errors()
    assert reporter.warning_count > 0
    assert "has no MAPPING clause, but that plot declares 1 role" in reporter.messages[0].message


def test_validator_error_on_end_plot_inside_on_enter(parser, builder, reporter):
    src = """
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            ON ENTER:
                END PLOT.
    """
    ast = parse_and_build(parser, builder, src)
    validator = Validator(reporter)
    validator.validate(ast)
    
    assert reporter.has_errors()
    assert "END PLOT cannot appear inside ON ENTER" in reporter.messages[0].message


def test_validator_error_on_end_plot_not_last_in_block(parser, builder, reporter):
    src = """
    ACTION do_something.
    EVENT e.
    
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            WHEN e:
                END PLOT.
                WORLD DO do_something.
    """
    ast = parse_and_build(parser, builder, src)
    validator = Validator(reporter)
    validator.validate(ast)
    
    assert reporter.has_errors()
    assert "Unreachable statement after END PLOT" in reporter.messages[0].message


def test_validator_accepts_implicit_events(parser, builder, reporter):
    src = """
    PLOT Test.
        PHASE one INITIAL.
        DURING PLOT:
            WHEN parent_ended:
                END PLOT.
            WHEN child_ended:
                END PLOT.
    """
    ast = parse_and_build(parser, builder, src)
    validator = Validator(reporter)
    validator.validate(ast)
    
    assert not reporter.has_errors()


# == Emission Tests ============================================================

def test_emitter_generates_start_subplot(parser, builder):
    src = """
    PLOT Child.
        PHASE a INITIAL.
        ROLE Fighter.
        DURING PLOT:
            WHEN e:
                WORLD DO f.
    
    PLOT Parent.
        PHASE one INITIAL.
        ROLE Hero.
        DURING one:
            ON ENTER:
                START SUBPLOT Child MAPPING Hero TO Fighter.
    """
    ast = parse_and_build(parser, builder, src)
    emitter = Emitter()
    out = emitter.emit(ast)
    
    parent_asl = out["director_parent.asl"]
    
    assert "START SUBPLOT Child" in parent_asl
    assert '.concat("child_", plot_id(Me), ChildId)' in parent_asl
    assert '.create_agent(ChildId, "director_child.asl")' in parent_asl
    assert ".findall(A, role_agent(hero, A), Agents_0)" in parent_asl
    assert "!build_bindings([map(fighter, Agents_0)], Bindings)" in parent_asl
    assert ".send(ChildId, achieve, start_plot(Bindings))" in parent_asl
    assert ".send(ChildId, tell, parent_plot(Me))" in parent_asl
    assert "+child_plot(ChildId, Child, [map(fighter, hero)])" in parent_asl


def test_emitter_generates_end_plot(parser, builder):
    src = """
    EVENT finish.
    PLOT Parent.
        PHASE one INITIAL.
        DURING one:
            WHEN finish:
                END PLOT.
    """
    ast = parse_and_build(parser, builder, src)
    emitter = Emitter()
    out = emitter.emit(ast)
    
    parent_asl = out["director_parent.asl"]
    
    assert "END PLOT" in parent_asl
    assert ".findall(C, child_plot(C, _, _), Children)" in parent_asl
    assert ".send(Child, tell, parent_ended)" in parent_asl
    assert ".send(Parent, tell, child_ended(Parent, Me))" in parent_asl
    assert ".kill_agent(self)" in parent_asl


def test_emitter_generates_boot_beliefs(parser, builder):
    src = """
    PLOT Test.
        PHASE one INITIAL.
        DURING one:
            ON ENTER:
                WORLD DO none.
    """
    ast = parse_and_build(parser, builder, src)
    emitter = Emitter()
    out = emitter.emit(ast)
    
    asl = out["director_test.asl"]
    
    assert "plot_name(Test)." in asl
    assert "+plot_id(Me)" in asl
