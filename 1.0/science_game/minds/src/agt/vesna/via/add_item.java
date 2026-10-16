package vesna.via;

import jason.JasonException;
import jason.asSemantics.*;
import jason.asSyntax.*;
import org.json.JSONObject;
import vesna.VesnaAgent;

/**
 * Internal action to add an item to the player's inventory.
 *
 * <p>Sends an "add_item" command to the Godot environment via VesnaManager.</p>
 */
public class add_item extends DefaultInternalAction {

    /**
     * Executes the internal action.
     *
     * @param ts   the transition system
     * @param un   the unifier
     * @param args the arguments supplied to the internal action (requires 1 string: item name)
     * @return true if the message was sent successfully
     * @throws Exception if an error occurs or arguments are invalid
     */
    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        if (args.length < 1) {
            throw new JasonException("vesna.add_item requires a string argument representing the item name.");
        }

        VesnaAgent agent = (VesnaAgent) ts.getAg();
        String itemName = args[0].toString().replace("\"", "");

        JSONObject data = new JSONObject();
        data.put("item", itemName);

        JSONObject message = new JSONObject();
        message.put("type", "add_item");
        message.put("data", data);

        agent.perform(message.toString());
        return true;
    }
}
