extends CanvasLayer
class_name HUD

@export var diary_container: VBoxContainer
@export var inventory_container: HBoxContainer

func _ready() -> void:
	# Connect to GameManager signals
	GameManager.diary_changed.connect(_on_diary_changed)
	GameManager.inventory_changed.connect(_on_inventory_changed)
	
	# Initial draw
	_on_diary_changed()
	_on_inventory_changed()

func _on_diary_changed() -> void:
	# Clear old labels
	if diary_container:
		for child in diary_container.get_children():
			child.queue_free()
			
		# Add title
		var title = Label.new()
		title.text = "--- DIARY ---"
		diary_container.add_child(title)
		
		# Draw active entries
		for entry in GameManager.diary_entries:
			var lbl = Label.new()
			lbl.text = "- " + entry
			lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			diary_container.add_child(lbl)

func _on_inventory_changed() -> void:
	# Clear old labels
	if inventory_container:
		for child in inventory_container.get_children():
			child.queue_free()
			
		# Add title
		var title = Label.new()
		title.text = "INVENTORY: "
		inventory_container.add_child(title)
		
		# Draw active items
		for item in GameManager.inventory:
			var lbl = Label.new()
			lbl.text = "[" + item.to_upper() + "] "
			inventory_container.add_child(lbl)
