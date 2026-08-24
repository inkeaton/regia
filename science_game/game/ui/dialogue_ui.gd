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
	add_to_group("dialogue_ui")
	
	# Listen to updates from NPCs if they update their dialogue while it's open.
	# We will rely on NPC signals if needed, but for now we'll just check state on start.

# ==============================================================================
# DIALOGUE FLOW
# ==============================================================================

## Called by the NPC when it wants to start a dialogue.
##
## @param player Reference to the player.
## @param npc Reference to the NPC.
func start_dialogue(player: Node2D, npc: Node2D) -> void:
	current_player = player
	current_npc = npc
	current_player.can_move = false
	visible = true
	_render_current_state()

## Refreshes the UI elements based on the NPC's current state.
func _render_current_state() -> void:
	# Clear previous options
	for child in options_container.get_children():
		options_container.remove_child(child)
		child.queue_free()
		
	if current_npc == null or not "current_dialogue_text" in current_npc:
		_close_dialogue()
		return
		
	var text = current_npc.current_dialogue_text
	if text == "":
		_close_dialogue()
		return
		
	# Set Text
	text_label.text = text
		
	# Set Portrait
	if "portrait" in current_npc and current_npc.portrait:
		portrait_sprite.texture = current_npc.portrait
	else:
		portrait_sprite.texture = null
		
	# Spawn Option Buttons
	if "current_options" in current_npc:
		for opt in current_npc.current_options:
			_spawn_option_button(opt)

## Instantiates and adds an option button to the UI container.
##
## @param opt_data Dictionary containing the option's text, next node, and event.
func _spawn_option_button(opt_data: Dictionary) -> void:
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
	# Fire event back to Regia
	var event_id = opt_data.get("event", "")
	
	if event_id == "exit_dialogue" or event_id == "exit":
		_close_dialogue()
		# Optionally we can still send the exit event to Jason if requested
		if event_id == "exit_dialogue":
			current_npc.vesna_manager.send_regia_event(event_id)
		return
		
	if event_id != "":
		current_npc.vesna_manager.send_regia_event(event_id)
		
	# Check if this option should close the UI
	if opt_data.get("close_on_select", false):
		_close_dialogue()
	else:
		# Disable options to indicate "thinking" state
		for child in options_container.get_children():
			if child is Button:
				child.disabled = true

## Called when an NPC receives a command from Jason to update the open dialogue.
func update_dialogue(npc: Node2D) -> void:
	if current_npc == npc and visible:
		_render_current_state()

## Closes the dialogue UI and unfreezes the player.
func _close_dialogue() -> void:
	visible = false
	if current_player:
		current_player.can_move = true
		current_player = null
	current_npc = null
