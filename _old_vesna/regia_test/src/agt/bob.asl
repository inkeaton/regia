// Bob is a simple agent that logs whatever the Director tells it to do.

// Catch playbook assignments
+add_playbook(PbName)[source(Dir)] <-
    .print("I received playbook '", PbName, "' from director ", Dir, "!").

+remove_playbook(PbName)[source(Dir)] <-
    .print("I lost playbook '", PbName, "' from director ", Dir, ".").

// Catch role assignment notifications (from subplots)
+plot_started(Plot, Roles)[source(Dir)] <-
    .print("Plot '", Plot, "' has started! Roles: ", Roles).

+plot_ended(Dir)[source(Dir)] <-
    .print("Director ", Dir, " just told me the plot ended.").

// Catch achieve commands (DO actions)
+!Action[source(Dir)] <-
    .print("Director ", Dir, " ordered me to do action: ", Action).

// Fallback for any other tell
+Belief[source(Dir)] <-
    .print("Director ", Dir, " told me: ", Belief).
