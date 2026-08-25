// Scientist Test Agent

!start.

+!start <-
    .print("Test Agent started.");
    .print("Test Agent started.").

// Scientist Agent - Regia Playbook
{ include("gen/role_testfeatures_scientist.asl") }

+navigation(reached, W) <-
    .print("Arrived at ", W, "!").

