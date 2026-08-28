package vesna.via;

import jason.asSemantics.DefaultInternalAction;
import jason.asSemantics.TransitionSystem;
import jason.asSemantics.Unifier;
import jason.asSyntax.StringTerm;
import jason.asSyntax.Term;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to trigger a game over in the Godot environment.
 */
public class trigger_game_over extends DefaultInternalAction {
    
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new IllegalArgumentException("trigger_game_over requires at least 1 string argument: reason");
        }
        
        String reason = ((StringTerm) args[0]).getString();
        
        JSONObject data = new JSONObject();
        data.put("reason", reason);
        
        JSONObject fullMessage = new JSONObject();
        fullMessage.put("type", "trigger_game_over");
        fullMessage.put("data", data);
        
        VesnaAgent agent = (VesnaAgent) ts.getAg();
        agent.perform(fullMessage.toString());
        
        return true;
    }
}
