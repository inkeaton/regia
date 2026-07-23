!test_sequence.

+!test_sequence : target_director(Dir) <-
    .print("Test runner started. Waiting 2 seconds for director to boot...");
    .wait(2000);
    
    .print("Sending 'battle_starts' event to director to trigger phase transition...");
    .send(Dir, tell, battle_starts);
    
    .wait(2000);
    .print("Sending 'battle_ends' to terminate the plot!");
    .send(Dir, tell, battle_ends).
