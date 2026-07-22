import pytest
from pathlib import Path
from regia.compiler import compile_source, compile_file
from regia.ast_nodes import DocAnnotation

def test_doc_comments():
    source = """
    #@desc: This is a test action
    #@author: Inkeaton
    ACTION jump.
    
    #@desc: This is a test event
    EVENT start.
    
    #@desc: File level comment
    """
    result = compile_source(source)
    assert result.success
    
    # Check ast attachment
    ast = result.ast
    assert ast is not None
    
    # Should have attached docs to the items
    action_item = ast.items[0]
    assert action_item.name == "jump"
    assert len(action_item.docs) == 2
    assert action_item.docs[0].key == "desc"
    assert action_item.docs[0].value == "This is a test action"
    assert action_item.docs[1].key == "author"
    
    event_item = ast.items[1]
    assert len(event_item.docs) == 1
    assert event_item.docs[0].key == "desc"
    
    # File level comment
    assert len(ast.doc_comments) == 1
    assert ast.doc_comments[0].value == "File level comment"

def test_inline_transitions():
    source = """
    ACTION jump.
    EVENT trigger.
    
    PLOT Test.
        PHASE start INITIAL.
        PHASE end.
        
        DURING start:
            ON EXIT:
                WORLD DO jump.
                
            WHEN trigger:
                TRANSITION TO end.
                
        DURING end:
            ON ENTER:
                WORLD DO jump.
    """
    result = compile_source(source)
    assert result.success
    assert result.error_count == 0
    
    # Check emitter output has expanded the transition
    # Should include: ON EXIT of start (jump), phase change, ON ENTER of end (jump)
    director_code = result.outputs["director_test.asl"]
    
    # Look for the plan for the trigger event
    assert "+trigger" in director_code
    assert "!switch_phase(end)" in director_code
    assert "+!on_exit(start) <-" in director_code
    assert "jump" in director_code

def test_inline_transitions_invalid_placement():
    # Should fail if transition is not the last statement
    source = """
    ACTION jump.
    EVENT trigger.
    
    PLOT Test.
        PHASE start INITIAL.
        PHASE end.
        
        DURING start:
            WHEN trigger:
                TRANSITION TO end.
                WORLD DO jump.
    """
    result = compile_source(source)
    assert not result.success
    assert "Unreachable statement after TRANSITION TO" in result.messages[0].message

    # Should fail if transition is in DURING PLOT
    source2 = """
    EVENT trigger.
    
    PLOT Test.
        PHASE start INITIAL.
        PHASE end.
        
        DURING PLOT:
            WHEN trigger:
                TRANSITION TO end.
    """
    result2 = compile_source(source2)
    assert not result2.success
    assert "cannot appear inside DURING PLOT" in result2.messages[0].message

def test_imports(tmp_path):
    # Create two files: main.regia and imported.regia
    main_file = tmp_path / "main.regia"
    imported_file = tmp_path / "imported.regia"
    
    imported_source = """
    ACTION imported_action.
    EVENT imported_event.
    """
    imported_file.write_text(imported_source)
    
    main_source = f"""
    IMPORT "{imported_file.name}".
    
    PLOT Test.
        PHASE start INITIAL.
        DURING start:
            WHEN imported_event:
                WORLD DO imported_action.
    """
    main_file.write_text(main_source)
    
    # We compile main_file, which should resolve the import
    # by looking in the same directory.
    result = compile_file(main_file)
    assert result.success
    assert result.error_count == 0
    assert "imported_action" in result.outputs["director_test.asl"]
