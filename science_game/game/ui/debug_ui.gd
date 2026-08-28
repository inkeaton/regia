extends CanvasLayer

var v_manager: VesnaManager

func _ready():
	v_manager = VesnaManager.new()
	v_manager.PORT = 9004
	v_manager.command_received.connect(_on_command_received)
	add_child(v_manager)
	
	var vbox = VBoxContainer.new()
	add_child(vbox)
	
	var btn_door = Button.new()
	btn_door.text = "Open Garden Door (garden_door_opened)"
	btn_door.focus_mode = Control.FOCUS_NONE
	btn_door.pressed.connect(func(): v_manager.send_regia_event("garden_door_opened"))
	vbox.add_child(btn_door)
	
	var btn_potion = Button.new()
	btn_potion.text = "Drop Item in Potion (item_in_potion)"
	btn_potion.focus_mode = Control.FOCUS_NONE
	btn_potion.pressed.connect(func(): v_manager.send_regia_event("item_in_potion"))
	vbox.add_child(btn_potion)

func _on_command_received(intention: Dictionary) -> void:
	var type = intention.get("type", "")
	var data = intention.get("data", {})
	if type == "spawn_item":
		GameManager.spawn_item(data.get("item", ""), data.get("waypoint", ""))
	elif type == "despawn_item":
		GameManager.despawn_item(data.get("item", ""))
