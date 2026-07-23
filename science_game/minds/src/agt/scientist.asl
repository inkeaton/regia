// Scientist Test Agent

!start.

+!start <-
    .print("Test Agent started.");
    vesna.via.set_dialogue("test_features");
    .print("Set dialogue to test_features.").

// Scientist Agent - Regia Playbook
{ include("gen/role_testfeatures_scientist.asl") }

+navigation(reached, W) <-
    .print("Arrived at ", W, "!").

