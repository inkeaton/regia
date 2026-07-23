package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to set the active dialogue node for an NPC.
 *
 * <p>Sends a "set_dialogue" command to the Godot environment via VesnaManager.</p>
 */
public class set_dialogue extends DefaultInternalAction {

    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 1 string: dialogue node ID)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new JasonException("vesna.set_dialogue requires a string argument representing the dialogue node ID.");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        String nodeId = args[0].toString().replace("\"", "");

        JSONObject data = new JSONObject();
        data.put("node", nodeId);

        JSONObject message = new JSONObject();
        message.put("type", "set_dialogue");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
