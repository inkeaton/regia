package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to clear the current dialogue options.
 */
public class clear_dialogue_options extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        VesnaAgent agent = (VesnaAgent) ts.getAg();

        JSONObject message = new JSONObject();
        message.put("type", "clear_dialogue_options");
        message.put("data", new JSONObject());

        agent.perform(message.toString());
        return true;
    }
}
