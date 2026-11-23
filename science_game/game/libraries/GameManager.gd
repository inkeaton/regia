## GameManager
##
## Stores cross-scene run state for the narrative game.
## This Autoload manages the player's inventory and diary entries.
extends Node

# ==============================================================================
# STATE
# ==============================================================================

var inventory: Array[String] = []
var diary_entries: Array[String] = []

# ==============================================================================
# SIGNALS
# ==============================================================================

signal inventory_changed
signal diary_changed
signal item_picked_up_in_world(item_name: String)

# ==============================================================================
# HELPER METHODS
# ==============================================================================

## Adds an item to the player's inventory.
##
## @param item_name The name of the item to add.
func add_item(item_name: String) -> void:
	if not inventory.has(item_name):
		inventory.append(item_name)
		inventory_changed.emit()

## Removes an item from the player's inventory.
##
## @param item_name The name of the item to remove.
func remove_item(item_name: String) -> void:
	if inventory.has(item_name):
		inventory.erase(item_name)
		inventory_changed.emit()

## Adds a text entry to the player's diary.
##
## @param entry_text The text of the diary entry to add.
func add_diary_entry(entry_text: String) -> void:
	if not diary_entries.has(entry_text):
		diary_entries.append(entry_text)
		diary_changed.emit()

## Removes a text entry from the player's diary.
##
## @param entry_text The text of the diary entry to remove.
func remove_diary_entry(entry_text: String) -> void:
	if diary_entries.has(entry_text):
		diary_entries.erase(entry_text)
		diary_changed.emit()

# ==============================================================================
# WORLD ACTIONS
# ==============================================================================

## Spawns an item in the game world at a specific waypoint.
##
## @param item_name The name of the item to spawn.
## @param waypoint_name The name of the waypoint to spawn the item at.
func spawn_item(item_name: String, waypoint_name: String) -> void:
	var waypoints = get_tree().get_nodes_in_group("waypoints")
	var target_wp = null
	for wp in waypoints:
		if wp.name == waypoint_name:
			target_wp = wp
			break
			
	if target_wp == null:
		print("GameManager: Error spawning - Waypoint '", waypoint_name, "' not found!")
		return
		
	var scene_path = "res://bodies/items/" + item_name + ".tscn"
	var ItemScene = load(scene_path) if ResourceLoader.exists(scene_path) else load("res://bodies/items/pickup_item.tscn")
	
	if ItemScene:
		var instance = ItemScene.instantiate()
		instance.global_position = target_wp.global_position
		if instance.get("item_name") != null:
			instance.item_name = item_name
		get_tree().current_scene.add_child(instance)
		print("GameManager: Spawned ", item_name, " at ", waypoint_name)
	else:
		print("GameManager: Failed to load item scene for ", item_name)

## Despawns an item from the game world.
##
## @param item_name The name of the item to despawn.
func despawn_item(item_name: String) -> void:
	var items = get_tree().get_nodes_in_group("items")
	var found = false
	for item in items:
		if item.has_method("get") and item.get("item_name") == item_name:
			item.queue_free()
			found = true
			print("GameManager: Despawned ", item_name)
			break
			
	if not found:
		print("GameManager: Error despawning - Item '", item_name, "' not found in world!")
