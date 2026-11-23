package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to set the current dialogue text for an NPC.
 */
public class set_dialogue_text extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new JasonException("vesna.via.set_dialogue_text requires a string argument representing the dialogue text.");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        String text = args[0].toString().replace("\"", "");

        JSONObject data = new JSONObject();
        data.put("text", text);

        JSONObject message = new JSONObject();
        message.put("type", "set_dialogue_text");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
