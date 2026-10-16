package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to issue a movement command to a body.
 *
 * <p>Sends a "move_to" command to the Godot environment via VesnaManager.</p>
 */
public class move_to extends DefaultInternalAction {

    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 1 string: target waypoint)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new JasonException("vesna.move_to requires a string argument representing the target waypoint name.");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        String target = args[0].toString().replace("\"", "");

        JSONObject data = new JSONObject();
        data.put("target", target);

        JSONObject message = new JSONObject();
        message.put("type", "move_to");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
