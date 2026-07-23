package vesna.via;

import jason.asSemantics.DefaultInternalAction;
import jason.asSemantics.TransitionSystem;
import jason.asSemantics.Unifier;
import jason.asSyntax.StringTerm;
import jason.asSyntax.Term;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to make an NPC display a speech bubble utterance.
 *
 * <p>Sends an "utter" command to the Godot environment via VesnaManager.</p>
 */
public class utter extends DefaultInternalAction {
    
    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 1 string: text)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new IllegalArgumentException("utter requires at least 1 string argument: text");
        }
        
        String text = ((StringTerm) args[0]).getString();
        
        JSONObject data = new JSONObject();
        data.put("text", text);
        
        JSONObject fullMessage = new JSONObject();
        fullMessage.put("type", "utter");
        fullMessage.put("data", data);
        
        VesnaAgent agent = (VesnaAgent) ts.getAg();
        agent.perform(fullMessage.toString());
        
        return true;
    }
}
