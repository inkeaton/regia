package vesna.via;

import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

public class stop_wandering extends DefaultInternalAction {
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        VesnaAgent agent = (VesnaAgent) ts.getAg();
        
        JSONObject message = new JSONObject();
        message.put("type", "stop_wandering");
        message.put("data", new JSONObject());

        agent.perform(message.toString());
        return true;
    }
}
