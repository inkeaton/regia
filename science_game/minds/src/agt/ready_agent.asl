// Coordinator Agent
// Listens for requests from other agents to modify the global HUD state
{ include("gen/role_testfeatures_coordinator.asl") }

+!add_item(Item) <-
    .print("Coordinator: Adding item ", Item);
    vesna.via.add_item(Item).

+!add_diary(Text) <-
    .print("Coordinator: Adding diary entry ", Text);
    vesna.via.add_diary_entry(Text).

+!spawn_item(Item, Waypoint) <-
    .print("Coordinator: Spawning item ", Item, " at ", Waypoint);
    vesna.via.spawn_item(Item, Waypoint).

+!despawn_item(Item) <-
    .print("Coordinator: Despawning item ", Item);
    vesna.via.despawn_item(Item).

// Forward world events to all agents
+picked_up_flower <-
    .print("Coordinator: Detected player picked up flower, broadcasting...");
    .broadcast(untell, picked_up_flower);
    .broadcast(tell, picked_up_flower).
