package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to add a new entry to the player's diary.
 *
 * <p>Sends an "add_diary_entry" command to the Godot environment via VesnaManager.</p>
 */
public class add_diary_entry extends DefaultInternalAction {

    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 1 string: diary text)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new JasonException("vesna.add_diary_entry requires a string argument.");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        String text = args[0].toString().replace("\"", "");

        JSONObject data = new JSONObject();
        data.put("text", text);

        JSONObject message = new JSONObject();
        message.put("type", "add_diary_entry");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
