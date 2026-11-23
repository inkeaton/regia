package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to remove a specific dialogue option by ID.
 */
public class remove_dialogue_option extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new JasonException("vesna.via.remove_dialogue_option requires a string argument representing the option ID.");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        String optionId = args[0].toString().replace("\"", "");

        JSONObject data = new JSONObject();
        data.put("id", optionId);

        JSONObject message = new JSONObject();
        message.put("type", "remove_dialogue_option");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
