## NPC
##
## Represents a non-playable character in the game world.
## This node manages navigation, interaction (dialogue), and bidirectional
## communication with its corresponding Jason agent via VesnaManager.
extends CharacterBody2D
class_name NPC

# ==============================================================================
# CONFIGURATION
# ==============================================================================

## Movement speed of the NPC.
@export var speed: float = 100.0

## Portrait texture to display in dialogue UI.
@export var portrait: Texture2D

# ==============================================================================
# DEPENDENCIES
# ==============================================================================

@onready var vesna_manager: VesnaManager = $VesnaManager
@onready var nav_agent: NavigationAgent2D = $NavigationAgent2D

# ==============================================================================
# STATE
# ==============================================================================

var current_dialogue_text: String = ""
var current_options: Array[Dictionary] = []
var current_target_waypoint: String = ""

var utterance_queue: Array[String] = []
@onready var utterance_panel: PanelContainer = $SpeechBubble
@onready var utterance_label: Label = $SpeechBubble/Text
@onready var utterance_timer: Timer = $UtteranceTimer

# ==============================================================================
# LIFECYCLE
# ==============================================================================

## Initializes the NPC and connects necessary signals.
func _ready() -> void:
	if vesna_manager:
		vesna_manager.command_received.connect(_on_command_received)
		
	# Listen to the global dialogue event to forward it to Jason
	# (We leave this for now, but DialogueManager is gone, so we must remove it)
	
	if utterance_panel:
		utterance_panel.visible = false
	if utterance_timer:
		utterance_timer.timeout.connect(_on_utterance_timeout)

## Processes visual updates, like the utterance queue.
func _process(_delta: float) -> void:
	if utterance_panel and not utterance_panel.visible and utterance_queue.size() > 0:
		_play_next_utterance()

## Processes physics and navigation logic.
func _physics_process(_delta: float) -> void:
	if nav_agent and not nav_agent.is_navigation_finished():
		var current_agent_position: Vector2 = global_position
		var next_path_position: Vector2 = nav_agent.get_next_path_position()
		
		velocity = current_agent_position.direction_to(next_path_position) * speed
		move_and_slide()
		
		if nav_agent.is_navigation_finished():
			if current_target_waypoint != "":
				vesna_manager.send_navigation_update("reached", current_target_waypoint)
				current_target_waypoint = ""

# ==============================================================================
# INTERACTION
# ==============================================================================

func interact(player: Node2D) -> void:
	if current_dialogue_text != "":
		# We emit a signal that the UI will catch. We'll implement a custom event later or pass references.
		var dialogue_ui = get_tree().get_first_node_in_group("dialogue_ui")
		if dialogue_ui:
			dialogue_ui.start_dialogue(player, self)
	else:
		print(name, " has no dialogue text set by Jason right now.")

func _play_next_utterance() -> void:
	var text = utterance_queue.pop_front()
	if utterance_label and utterance_panel and utterance_timer:
		utterance_label.text = text
		utterance_panel.visible = true
		utterance_timer.start(3.0)
		print(name, " is saying: '", text, "' (3s timer started)")

func _on_utterance_timeout() -> void:
	if utterance_panel:
		utterance_panel.visible = false
		print(name, " finished speaking.")

# ==============================================================================
# SIGNAL HANDLERS
# ==============================================================================

## Handles commands received from the Jason agent.
##
## @param intention The dictionary containing the command details.
func _on_command_received(intention: Dictionary) -> void:
	var type = intention.get("type", "")
	var data = intention.get("data", {})
	
	var dialogue_updated = false
	
	if type == "set_dialogue_text":
		current_dialogue_text = data.get("text", "")
		print(name, " received new dialogue text: ", current_dialogue_text)
		dialogue_updated = true
		
	elif type == "add_dialogue_options":
		var opts = data.get("options", [])
		for opt in opts:
			current_options.append(opt)
		print(name, " added options. Total options: ", current_options.size())
		dialogue_updated = true
		
	elif type == "clear_dialogue_options":
		current_options.clear()
		print(name, " cleared dialogue options.")
		dialogue_updated = true
		
	elif type == "remove_dialogue_option":
		var opt_id = data.get("id", "")
		for i in range(current_options.size() - 1, -1, -1):
			if current_options[i].get("id") == opt_id:
				current_options.remove_at(i)
		print(name, " removed dialogue option: ", opt_id)
		dialogue_updated = true
		
	elif type == "move_to":
		var target_name = data.get("target", "")
		current_target_waypoint = target_name
		
		var waypoints = get_tree().get_nodes_in_group("waypoints")
		var found = false
		for wp in waypoints:
			if wp.name == target_name:
				nav_agent.target_position = wp.global_position
				found = true
				break
				
		if not found:
			print("Error: Waypoint '", target_name, "' not found!")
			vesna_manager.send_navigation_update("failed", target_name)
			
	elif type == "set_visible":
		var is_visible = data.get("visible", true)
		visible = is_visible
		
		# Toggle physical collisions
		for child in get_children():
			if child is CollisionShape2D or child is CollisionPolygon2D:
				child.set_deferred("disabled", not is_visible)
				
		# Stop processing if invisible
		if not is_visible:
			process_mode = Node.PROCESS_MODE_DISABLED
		else:
			process_mode = Node.PROCESS_MODE_INHERIT
		
		print(name, " visibility set to ", is_visible)
		
	elif type == "utter":
		var text = data.get("text", "")
		if text != "":
			utterance_queue.append(text)
			print(name, " queued utterance: '", text, "' (Queue size: ", utterance_queue.size(), ")")
			
	elif type == "spawn_item":
		GameManager.spawn_item(data.get("item", ""), data.get("waypoint", ""))
		
	elif type == "despawn_item":
		GameManager.despawn_item(data.get("item", ""))
		
	elif type == "add_item":
		GameManager.add_item(data.get("item", ""))
		
	elif type == "remove_item":
		GameManager.remove_item(data.get("item", ""))
		
	elif type == "add_diary_entry":
		GameManager.add_diary_entry(data.get("text", ""))
		
	elif type == "remove_diary_entry":
		GameManager.remove_diary_entry(data.get("text", ""))
		
	if dialogue_updated:
		var dialogue_ui = get_tree().get_first_node_in_group("dialogue_ui")
		if dialogue_ui and dialogue_ui.has_method("update_dialogue"):
			dialogue_ui.update_dialogue(self)
		


## Forwards global dialogue events specific to this NPC to its Jason agent.
##
## @param event_id The ID of the dialogue event.
## @param npc_reference The reference to the NPC involved in the dialogue.
func _on_global_dialogue_event(event_id: String, npc_reference: Node2D) -> void:
	if npc_reference == self:
		vesna_manager.send_regia_event(event_id)
