// Cop Test Agent

!start.

+!start <-
    .print("Cop Agent started.");
    vesna.via.set_dialogue("cop_idle");
    .print("Set dialogue to cop_idle.").

// Cop Agent - Regia Playbook
{ include("gen/role_testfeatures_cop.asl") }
