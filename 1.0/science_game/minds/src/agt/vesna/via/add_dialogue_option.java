package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONArray;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to inject a single dialogue option.
 */
public class add_dialogue_option extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length != 4) {
            throw new JasonException("vesna.via.add_dialogue_option requires exactly 4 arguments (id, text, event, close_ui).");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        JSONArray optionsArray = new JSONArray();

        String id = args[0].toString().replace("\"", "");
        String text = args[1].toString().replace("\"", "");
        String event = args[2].toString().replace("\"", "");
        boolean closeUi = args[3].toString().replace("\"", "").equals("true");

        JSONObject opt = new JSONObject();
        opt.put("id", id);
        opt.put("text", text);
        opt.put("event", event);
        opt.put("close_on_select", closeUi);
        optionsArray.put(opt);

        JSONObject data = new JSONObject();
        data.put("options", optionsArray);

        JSONObject message = new JSONObject();
        message.put("type", "add_dialogue_options");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
