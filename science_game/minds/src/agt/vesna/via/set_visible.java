package vesna.via;

import jason.asSemantics.DefaultInternalAction;
import jason.asSemantics.TransitionSystem;
import jason.asSemantics.Unifier;
import jason.asSyntax.Literal;
import jason.asSyntax.Term;
import jason.asSyntax.ASSyntax;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to set the physical visibility of an NPC in the game world.
 *
 * <p>Sends a "set_visible" command to the Godot environment via VesnaManager,
 * and updates the internal belief visible(true/false) in the agent's belief base.</p>
 */
public class set_visible extends DefaultInternalAction {
    
    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 1 boolean)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new IllegalArgumentException("set_visible requires exactly 1 boolean argument");
        }
        
        boolean isVisible = false;
        String argString = args[0].toString();
        
        if (argString.equals("true")) {
            isVisible = true;
        } else if (argString.equals("false")) {
            isVisible = false;
        } else {
            throw new IllegalArgumentException("set_visible argument must be a boolean (true or false)");
        }
        
        JSONObject data = new JSONObject();
        data.put("visible", isVisible);
        
        JSONObject fullMessage = new JSONObject();
        fullMessage.put("type", "set_visible");
        fullMessage.put("data", data);
        
        VesnaAgent agent = (VesnaAgent) ts.getAg();
        agent.perform(fullMessage.toString());
        
        // Update the agent's internal belief about its visibility
        agent.delBel(ASSyntax.parseLiteral("visible(_)"));
        Literal belief = ASSyntax.createLiteral("visible", ASSyntax.createAtom(String.valueOf(isVisible)));
        agent.addBel(belief);
        
        return true;
    }
}
