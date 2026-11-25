// PROTOTYPE ticket 07 — throwaway
!go.
+!go <-
    .wait(4000);
    .print("PROBE asking forscience_director to start subplot missingdonut");
    .send(forscience_director, achieve, start_subplot("missingdonut", missingdonut, [map(cop, cop), map(dog, dog)]));
    .wait(5000);
    .all_names(L);
    .print("PROBE agents now: ", L).
// also check that a role agent loaded its gen/ include chain
