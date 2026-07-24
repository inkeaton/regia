package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to inject a dialogue option.
 *
 * <p>Sends an "add_dialogue_option" command to the Godot environment via VesnaManager.</p>
 */
public class add_dialogue_option extends DefaultInternalAction {

    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 1 string: option ID)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new JasonException("vesna.via.add_dialogue_option requires a string argument representing the option ID.");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        String optionId = args[0].toString().replace("\"", "");

        JSONObject data = new JSONObject();
        data.put("id", optionId);

        JSONObject message = new JSONObject();
        message.put("type", "add_dialogue_option");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
