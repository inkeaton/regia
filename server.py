import json
import dataclasses
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import your compiler pipeline
from language.src.regia.compiler import compile_source
from language.src.regia.ast_nodes import Program

# ==============================================================================
# SERVER CONFIGURATION
# ==============================================================================
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) allows our React app running on a 
# different port to communicate with this Python server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodePayload(BaseModel):
    source_code: str

# ==============================================================================
# JSON ENCODER
# ==============================================================================
class ASTEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to transform Python dataclasses into JSON objects.
    It injects a 'type' field into every dictionary so the React frontend 
    knows which AST node it is looking at.
    """
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            # FIX: We use __dict__.copy() instead of asdict(). 
            # This only converts the current level to a dict, forcing 
            # json.dumps to recursively call this method for child dataclasses!
            d = obj.__dict__.copy()
            d["type"] = obj.__class__.__name__ 
            return d
        if hasattr(obj, "value"): 
            return obj.value
        return super().default(obj)

# ==============================================================================
# API ENDPOINTS
# ==============================================================================
@app.post("/parse")
def parse_code(payload: CodePayload):
    print("--- NEW PARSE REQUEST ---")
    result = compile_source(payload.source_code, emit=False)
    
    if not result.success:
        print(f"Compilation Failed with {len(result.messages)} errors.")
        safe_errors = []
        for msg in result.messages:
            msg_dict = msg.__dict__.copy()
            if 'severity' in msg_dict and hasattr(msg_dict['severity'], 'name'):
                msg_dict['severity'] = msg_dict['severity'].name
            safe_errors.append(msg_dict)
            
        raise HTTPException(status_code=400, detail=safe_errors)
    
    # Check if AST exists
    if not result.ast:
        print("CRITICAL: result.ast is None! compiler.py is still not attaching it.")
        return None

    # Convert to JSON and print a tiny preview
    ast_dict = json.loads(json.dumps(result.ast, cls=ASTEncoder))
    print(f"SUCCESS! AST Root Type: {ast_dict.get('type')}")
    print(f"Number of Items: {len(ast_dict.get('items', []))}")
    
    # Check if PlotDef is in the items
    plot_found = any(item.get("type") == "PlotDef" for item in ast_dict.get("items", []))
    print(f"PlotDef Found in JSON?: {plot_found}")
    
    return ast_dict

if __name__ == "__main__":
    import uvicorn
    # Runs the server on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)