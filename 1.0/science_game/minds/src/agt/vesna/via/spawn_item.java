package vesna.via;

import jason.asSemantics.DefaultInternalAction;
import jason.asSemantics.TransitionSystem;
import jason.asSemantics.Unifier;
import jason.asSyntax.StringTerm;
import jason.asSyntax.Term;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to spawn an item in the game world.
 *
 * <p>Sends a "spawn_item" command to the Godot environment via VesnaManager.</p>
 */
public class spawn_item extends DefaultInternalAction {
    
    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 2 strings: item_name, waypoint_name)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 2) {
            throw new IllegalArgumentException("spawn_item requires exactly 2 string arguments: item_name and waypoint_name");
        }
        
        String itemName = ((StringTerm) args[0]).getString();
        String waypointName = ((StringTerm) args[1]).getString();
        
        JSONObject data = new JSONObject();
        data.put("item", itemName);
        data.put("waypoint", waypointName);
        
        JSONObject fullMessage = new JSONObject();
        fullMessage.put("sender", "vesna");
        fullMessage.put("receiver", "body");
        fullMessage.put("type", "spawn_item");
        fullMessage.put("data", data);
        
        VesnaAgent agent = (VesnaAgent) ts.getAg();
        agent.perform(fullMessage.toString());
        
        return true;
    }
}
