// Cop Test Agent

!start.

+!start <-
    .print("Cop Test Agent started.").

// Cop Agent - Regia Playbook
{ include("role_forscience_cop.asl") }
