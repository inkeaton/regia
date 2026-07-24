## DialogueUI
##
## Manages the user interface for dialogue sequences. Displays text, portraits,
## and clickable options, and sends events back to the DialogueManager when
## the player makes a choice.
extends CanvasLayer
class_name DialogueUI

# ==============================================================================
# DEPENDENCIES & UI NODES
# ==============================================================================

@export var text_label: RichTextLabel
@export var portrait_sprite: Sprite2D
@export var options_container: VBoxContainer
@export var option_button_scene: PackedScene # A basic Button scene

# ==============================================================================
# STATE
# ==============================================================================

var current_player: Node2D
var current_npc: Node2D

# ==============================================================================
# LIFECYCLE
# ==============================================================================

## Connects to the DialogueManager to listen for dialogue requests.
func _ready() -> void:
	visible = false
	DialogueManager.request_dialogue.connect(start_dialogue)
	DialogueManager.request_dialogue_update.connect(_on_dialogue_update)
	
	# Listen to events for testing (simulating VEsNA transmission to Jason)
	DialogueManager.dialogue_event.connect(func(event_id, npc):
		print("VEsNA SIMULATION -> Sent event to Jason: ", event_id, " from ", npc.name)
		
		# --- HUD TESTING SIMULATION ---
		if event_id == "told_dummy_nice":
			GameManager.add_item("flower")
			GameManager.add_diary_entry("Be nice to the dummy.")
	)

# ==============================================================================
# DIALOGUE FLOW
# ==============================================================================

## Called by the DialogueManager when an NPC wants to start a dialogue.
##
## @param node_id The ID of the dialogue node to start.
## @param player Reference to the player.
## @param npc Reference to the NPC.
func start_dialogue(node_id: String, player: Node2D, npc: Node2D) -> void:
	current_player = player
	current_npc = npc
	current_player.can_move = false
	visible = true
	_load_node(node_id)

## Loads a specific dialogue node and populates the UI elements.
##
## @param node_id The ID of the dialogue node to load.
func _load_node(node_id: String) -> void:
	# Clear previous options
	for child in options_container.get_children():
		child.queue_free()
		
	var data = DialogueManager.get_node_data(node_id)
	if data.is_empty():
		_close_dialogue()
		return
		
	# Set Text
	if data.has("text"):
		text_label.text = data["text"]
		
	# Set Portrait
	if data.has("portrait"):
		var tex = load(data["portrait"])
		if tex:
			portrait_sprite.texture = tex
			
	# Spawn Option Buttons
	if data.has("options"):
		for opt in data["options"]:
			_spawn_option_button(opt)
			
	# Spawn Injected Options
	if current_npc and "injected_options" in current_npc:
		for opt_id in current_npc.injected_options:
			var opt_data = DialogueManager.get_injected_option(opt_id)
			if not opt_data.is_empty():
				_spawn_option_button(opt_data)

## Instantiates and adds an option button to the UI container.
##
## @param opt_data Dictionary containing the option's text, next node, and event.
func _spawn_option_button(opt_data: Dictionary) -> void:
	if current_npc and "removed_options" in current_npc and opt_data.has("id") and opt_data["id"] in current_npc.removed_options:
		return
		
	if not option_button_scene:
		print("DialogueUI Error: option_button_scene is not assigned!")
		return
		
	var btn = option_button_scene.instantiate() as Button
	btn.text = opt_data.get("text", "...")
	
	# Connect the press event
	btn.pressed.connect(func():
		_on_option_selected(opt_data)
	)
	options_container.add_child(btn)

## Callback for when the player clicks a dialogue option.
##
## @param opt_data The dictionary data associated with the clicked option.
func _on_option_selected(opt_data: Dictionary) -> void:
	if opt_data.get("remove_on_select", false) and current_npc and "removed_options" in current_npc and opt_data.has("id"):
		if not opt_data["id"] in current_npc.removed_options:
			current_npc.removed_options.append(opt_data["id"])
			
	# Fire event if present
	if opt_data.has("event"):
		DialogueManager.dialogue_event.emit(opt_data["event"], current_npc)
		
	# Handle flow
	var next_id = opt_data.get("next", "exit")
	if next_id == "exit":
		_close_dialogue()
	elif next_id == "await_agent":
		# Disable options to indicate "thinking" state
		for child in options_container.get_children():
			if child is Button:
				child.disabled = true
	else:
		_load_node(next_id)

## Called when an NPC receives a command from Jason to update the open dialogue.
func _on_dialogue_update(node_id: String, npc: Node2D) -> void:
	if current_npc == npc and visible:
		_load_node(node_id)

## Closes the dialogue UI and unfreezes the player.
func _close_dialogue() -> void:
	visible = false
	if current_player:
		current_player.can_move = true
		current_player = null
	current_npc = null
