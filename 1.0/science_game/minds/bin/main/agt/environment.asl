// Environment Agent
// Forward events from the environment to all agents
+picked_up_flower <-
    .print("Coordinator: Detected player picked up flower, broadcasting...");
    .broadcast(untell, picked_up_flower);
    .broadcast(tell, picked_up_flower).
