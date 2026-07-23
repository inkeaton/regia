## DialogueManager
##
## Autoload that manages the global dialogue database. Loads the JSON file
## and provides dialogue data to UI and NPC nodes upon request.
extends Node

# ==============================================================================
# STATE
# ==============================================================================

## The globally loaded JSON dialogue dictionary.
var database: Dictionary = {}

# ==============================================================================
# SIGNALS
# ==============================================================================

## Signal emitted when the player chooses an option that has an "event" attached.
signal dialogue_event(event_id: String, npc_reference: Node2D)

## Signal emitted when an NPC wants to start a dialogue.
signal request_dialogue(node_id: String, player: Node2D, npc_reference: Node2D)

# ==============================================================================
# LIFECYCLE
# ==============================================================================

## Initializes the manager and loads the dialogue database from disk.
func _ready() -> void:
	_load_database()

## Loads the JSON dialogue database.
func _load_database() -> void:
	var file = FileAccess.open("res://resources/dialogue/dialogue.json", FileAccess.READ)
	if file:
		var json_string = file.get_as_text()
		var json = JSON.new()
		var error = json.parse(json_string)
		if error == OK:
			database = json.data
			print("Dialogue database loaded successfully. Found ", database.size(), " nodes.")
		else:
			print("JSON Parse Error: ", json.get_error_message())
	else:
		print("Failed to open dialogue.json")

# ==============================================================================
# DIALOGUE HELPERS
# ==============================================================================

## Returns the dialogue node dictionary for a given ID.
##
## @param node_id The ID of the dialogue node to retrieve.
## @return Dictionary The dialogue node data, or empty dictionary if not found.
func get_node_data(node_id: String) -> Dictionary:
	if database.has(node_id):
		return database[node_id]
	print("Dialogue Error: Node '", node_id, "' not found in database!")
	return {}

## Triggers the global dialogue UI to open.
##
## @param node_id The ID of the dialogue node to start.
## @param player Reference to the player node.
## @param npc_reference Reference to the NPC node starting the dialogue.
func start_dialogue(node_id: String, player: Node2D, npc_reference: Node2D) -> void:
	request_dialogue.emit(node_id, player, npc_reference)
