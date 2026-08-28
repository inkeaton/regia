package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

public class start_wandering extends DefaultInternalAction {
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        VesnaAgent agent = (VesnaAgent) ts.getAg();
        
        JSONObject data = new JSONObject();
        if (args.length > 0) {
            try {
                int radius = 500;
                if (args[0].isNumeric()) {
                    radius = (int) ((NumberTerm) args[0]).solve();
                } else {
                    radius = Integer.parseInt(args[0].toString().replace("\"", ""));
                }
                data.put("radius", radius);
            } catch (Exception e) {
                throw new JasonException("vesna.start_wandering requires a valid number argument.");
            }
        } else {
            data.put("radius", 500); // Default radius
        }

        JSONObject message = new JSONObject();
        message.put("type", "start_wandering");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
