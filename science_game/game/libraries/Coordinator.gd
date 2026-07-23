## Coordinator
##
## This class manages the global game state from the Godot side and acts as the
## bridge for the "Coordinator" Jason agent. It handles commands like adding items,
## spawning items, and updating the diary, and forwards world events back to Jason.
extends Node
class_name Coordinator

# ==============================================================================
# DEPENDENCIES
# ==============================================================================

@onready var vesna_manager: VesnaManager = $VesnaManager

# ==============================================================================
# LIFECYCLE
# ==============================================================================

## Initializes the coordinator and connects required signals.
func _ready() -> void:
	if vesna_manager:
		vesna_manager.command_received.connect(_on_command_received)
	GameManager.item_picked_up_in_world.connect(_on_item_picked_up)

# ==============================================================================
# SIGNAL HANDLERS
# ==============================================================================

## Handles the event when a player picks up an item in the world.
##
## Formats the signal to be Regia-compatible (e.g. "picked_up_flower") and
## sends it to the Jason agent.
##
## @param item_name The name of the item picked up.
func _on_item_picked_up(item_name: String) -> void:
	# Format the signal as 'picked_up_itemname' for easy Regia compatibility
	var event_id = "picked_up_" + item_name.replace(" ", "_").to_lower()
	vesna_manager.send_regia_event(event_id)

## Receives commands from the Jason agent via the VesnaManager.
##
## @param intention The dictionary containing the command type and data.
func _on_command_received(intention: Dictionary) -> void:
	var type = intention.get("type", "")
	var data = intention.get("data", {})
	
	if type == "add_item":
		GameManager.add_item(data.get("item", ""))
	elif type == "remove_item":
		GameManager.remove_item(data.get("item", ""))
	elif type == "add_diary_entry":
		GameManager.add_diary_entry(data.get("text", ""))
	elif type == "remove_diary_entry":
		GameManager.remove_diary_entry(data.get("text", ""))
	elif type == "spawn_item":
		GameManager.spawn_item(data.get("item", ""), data.get("waypoint", ""))
	elif type == "despawn_item":
		GameManager.despawn_item(data.get("item", ""))
