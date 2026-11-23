shader_type canvas_item;

// --- Tunables (shown in Inspector on the ShaderMaterial) ---
uniform float walk_speed : hint_range(0.0, 10.0) = 4.0;     // cycles per second-ish
uniform float bob_amount : hint_range(0.0, 20.0) = 4.0;     // vertical bounce, in pixels
uniform float sway_amount : hint_range(0.0, 20.0) = 3.0;    // horizontal lean, in pixels
uniform float squash_amount : hint_range(0.0, 0.2) = 0.05;  // stretch/squeeze factor (0 = off)
uniform float tilt_amount : hint_range(0.0, 0.2) = 0.05;    // rotation lean, in radians
uniform bool is_walking = true;                              // toggle from GDScript when the character moves

void vertex() {
	if (is_walking) {
		float t = TIME * walk_speed;

		// Two little bounces per stride (feels like footsteps), always moving up from rest
		float bob = abs(sin(t)) * bob_amount;

		// Side-to-side sway, one full cycle per stride
		float sway = sin(t) * sway_amount;

		// Slight rotation "wobble" so it doesn't feel like it's sliding on rails
		float tilt = sin(t) * tilt_amount;

		// Subtle squash/stretch: taller+thinner at the top of the bounce, shorter+wider at the bottom
		float squeeze = sin(t * 2.0) * squash_amount;

		vec2 v = VERTEX;

		// Apply squash/stretch around the sprite's local center (VERTEX is in local pixel space,
		// origin usually at the sprite's pivot -- adjust if your pivot isn't centered).
		v.y *= (1.0 - squeeze);
		v.x *= (1.0 + squeeze * 0.5);

		// Apply rotation (tilt) manually since we're in vertex space
		float c = cos(tilt);
		float s = sin(tilt);
		v = vec2(v.x * c - v.y * s, v.x * s + v.y * c);

		// Apply bob and sway as translation
		v.y -= bob;
		v.x += sway;

		VERTEX = v;
	}
}
