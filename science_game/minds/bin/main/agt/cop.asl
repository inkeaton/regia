// Cop Test Agent

!start.

+!start <-
    .print("Cop Agent started.");
    vesna.via.set_dialogue_text("Move along, citizen. Nothing to see here.");
    vesna.via.clear_dialogue_options;
    vesna.via.add_dialogue_option("opt_leave", "Goodbye. (Leave)", "exit", "true");
    .print("Set default dialogue text and options.").

// Cop Agent - Regia Playbook
{ include("gen/role_testfeatures_cop.asl") }
