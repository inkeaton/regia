## VesnaManager
##
## Body-side WebSocket bridge used by agents to communicate with the Godot engine.
## Manages TCP connections and JSON-based messaging protocols for "signal", "sight",
## "navigation", and custom events.
extends Node
class_name VesnaManager

# ==============================================================================
# SIGNALS
# ==============================================================================
signal command_received(intention: Dictionary)
signal connection_established()
signal connection_lost()

# ==============================================================================
# CONFIGURATION
# ==============================================================================
@export var PORT : int = 9080

# ==============================================================================
# STATE
# ==============================================================================
var tcp_server := TCPServer.new()
var ws := WebSocketPeer.new()

# Track if we were open last frame to detect changes
var _was_open_last_frame : bool = false

# ==============================================================================
# LIFECYCLE
# ==============================================================================
func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS  # Must keep running while tree is paused
	if tcp_server.listen(PORT) != OK:
		Warnings.print_warning("Unable to start server on port " + str(PORT), "NetworkManager")
		set_process(false)
	else:
		Messages.print_message("Listening on port " + str(PORT), "NetworkManager")
		
	GameManager.item_picked_up_in_world.connect(_on_item_picked_up)

# ==============================================================================
# POLLING & CONNECTION
# ==============================================================================
func _process(_delta: float) -> void:
	# 1. Accept new TCP connections.
	if tcp_server.is_connection_available():
		var conn : StreamPeerTCP = tcp_server.take_connection()
		if conn:
			# If a prior connection exists, accept and override with the new one.
			ws.accept_stream(conn)
			Messages.print_message("New TCP connection accepted. Handshaking...", "NetworkManager")

	# 2. Poll WebSocket.
	ws.poll()
	var state = ws.get_ready_state()

	# 3. Handle state changes.
	if state == WebSocketPeer.STATE_OPEN:
		if not _was_open_last_frame:
			_was_open_last_frame = true
			connection_established.emit()
			Messages.print_message("WebSocket Handshake complete. Channel OPEN.", "NetworkManager")
			
		# 4. Read incoming packets (only when open).
		while ws.get_available_packet_count():
			var msg : String = ws.get_packet().get_string_from_ascii()
			
			var intention = JSON.parse_string(msg)
			if intention:
				Messages.print_json(intention, "Received Raw Message")
				if intention.get("type") == "trigger_game_over":
					var reason = intention.get("data", {}).get("reason", "Unknown")
					print("=========================================")
					print("GAME OVER! Reason: ", reason)
					print("=========================================")
					_show_game_over_screen(reason)
				else:
					command_received.emit(intention)
			else:
				Warnings.print_warning("Failed to parse JSON message", "NetworkManager")
				
	elif state == WebSocketPeer.STATE_CLOSED:
		if _was_open_last_frame:
			_was_open_last_frame = false
			connection_lost.emit()
			Warnings.print_warning("Connection lost or closed.", "NetworkManager")

# ==============================================================================
# OUTBOUND MESSAGE HELPERS
# ==============================================================================

func _on_item_picked_up(item_name: String) -> void:
	var event_id = "picked_up_" + item_name.replace(" ", "_").to_lower()
	send_regia_event(event_id)

func send_data(data: Dictionary) -> void:
	if ws.get_ready_state() == WebSocketPeer.STATE_OPEN:
		var json_str = JSON.stringify(data)
		ws.send_text(json_str)
		Messages.print_json(data, "Sent Data")
	else:
		Warnings.print_warning("Cannot send data: WebSocket not open", "NetworkManager")

func send_signal(signal_type: String, status: String, reason: String) -> void:
	var data = {
		"sender": "body",
		"receiver": "vesna",
		"type": "signal",
		"data": {
			"type": signal_type,
			"status": status,
			"reason": reason
		}
	}
	send_data(data)

## Sends a parameterless event tailored for Regia Playbooks.
func send_regia_event(event_type: String) -> void:
	var data = {
		"sender": "body",
		"receiver": "vesna",
		"type": "regia_event",
		"data": {
			"type": event_type
		}
	}
	send_data(data)

func send_navigation_update(status: String, waypoint_name: String):
	var data = {
		"sender": "body",
		"receiver": "vesna",
		"type": "navigation",
		"data": {
			"status": status,
			"waypoint": waypoint_name
		}
	}
	send_data(data)

func send_custom_event(event_type: String, event_data: Dictionary) -> void:
	var data = {
		"sender": "body",
		"receiver": "vesna",
		"type": event_type,
		"data": event_data
	}
	send_data(data)

## Sends an event to the mind using `signal` message type.
## `event_type` is injected into the outgoing `data` payload.
func send_event(event_type: String, event_data: Dictionary) -> void:
	var data = {
		"sender": "body",
		"receiver": "vesna",
		"type": "signal",
		"data": event_data.duplicate()
	}
	# Add the event type to the data.
	data["data"]["type"] = event_type
	send_data(data)

# ==============================================================================
# CONNECTION STATUS
# ==============================================================================

func is_mind_connected() -> bool:
	return ws.get_ready_state() == WebSocketPeer.STATE_OPEN

# ==============================================================================
# CLEANUP
# ==============================================================================
func _exit_tree() -> void:
	ws.close()
	tcp_server.stop()

# ==============================================================================
# UI HELPERS
# ==============================================================================

func _show_game_over_screen(reason: String) -> void:
	var game_over_scene = load("res://ui/game_over_ui.tscn") as PackedScene
	if game_over_scene:
		var game_over_instance = game_over_scene.instantiate()
		get_tree().root.add_child(game_over_instance)
		
		# If you add a script to the root of game_over_ui with a setup(reason) function:
		if game_over_instance.has_method("setup"):
			game_over_instance.setup(reason)
		
		get_tree().paused = true
	else:
		print("GAME OVER! Reason: ", reason)
		get_tree().quit()
