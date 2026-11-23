package vesna;

import jason.asSyntax.Pred;

/**
 * Interface for getting a predicate from both Options and Intentions
 */
public interface TemperSelectable {

    /**
     * Get the label of this TemperSelectable
     * @return the label as a Predicate
     */
    Pred getLabel();

}