extends CanvasLayer

@onready var reason_label: Label = $ColorRect/VBoxContainer/ReasonLabel
@onready var quit_button: Button = $ColorRect/VBoxContainer/QuitButton

func _ready() -> void:
	# Wire the quit button
	quit_button.pressed.connect(func(): get_tree().quit())

# This is called by vesnaManager.gd to pass in the reason (e.g., "Arrested by Cop")
func setup(reason: String) -> void:
	if reason_label:
		reason_label.text = reason
