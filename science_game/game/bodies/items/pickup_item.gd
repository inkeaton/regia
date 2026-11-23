## PickupItem
##
## Represents a generic item in the game world that the player can interact with.
## When interacted with, it adds itself to the GameManager's inventory,
## notifies the Coordinator via a signal, and removes itself from the scene.
class_name PickupItem
extends Area2D

# ==============================================================================
# CONFIGURATION
# ==============================================================================

## The unique identifier for this item, used in inventory and Jason signals.
@export var item_name: String = "mystery_item"

# ==============================================================================
# LIFECYCLE
# ==============================================================================

## Initializes the item and adds it to the global "items" group for easy querying.
func _ready() -> void:
	add_to_group("items")

# ==============================================================================
# INTERACTION
# ==============================================================================

## Called when the player interacts with this object using the RayCast2D.
##
## @param _player The Node2D representing the player.
func interact(_player: Node2D) -> void:
	# Add to local inventory logic
	GameManager.add_item(item_name)
	
	# Signal the Coordinator/VEsNA that an item was picked up
	GameManager.item_picked_up_in_world.emit(item_name)
	
	# Remove the item from the world
	queue_free()
