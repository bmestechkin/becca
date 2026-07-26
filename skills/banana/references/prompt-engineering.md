# Prompt Engineering -- Reference

## The 5-Component Formula

Every Reasoning Brief follows: **Subject → Action → Location/Context → Composition → Style (includes lighting)**

1. **Subject** -- who/what, with specific visual detail (age, appearance, material, texture)
2. **Action** -- what is happening, described as a verb, not a static label
3. **Location/Context** -- where, and when (time of day, season, setting detail)
4. **Composition** -- camera angle, framing, distance, depth of field
5. **Style** -- medium, lighting setup, camera/lens (for photorealism), art style (for illustration), mood

Be SPECIFIC and VISCERAL: describe what the camera sees, not what the image is "for."

## Critical Rules

- Name real cameras: "Sony A7R IV", "Canon EOS R5", "iPhone 16 Pro Max"
- Name real brands for styling: "Lululemon", "Tom Ford" (triggers visual associations)
- Include micro-details: "sweat droplets on collarbones", "baby hairs stuck to neck"
- Use prestigious context anchors: "Vanity Fair editorial", "National Geographic cover"
- **Never** use banned keywords as a stand-in for resolution: "8K", "masterpiece", "ultra-realistic", "high resolution" -- use the `imageSize` param instead
- **Never** write "a dark-themed ad showing..." -- describe the SCENE, not the marketing concept
- For critical constraints use ALL CAPS: "MUST contain exactly three figures"
- For products: say "prominently displayed" to ensure visibility

## Domain Modifier Libraries

### Cinema
Camera: Arri Alexa, RED Komodo, anamorphic lens, 35mm film grain.
Lighting: three-point, practical lights, chiaroscuro, golden hour backlight.
Mood anchors: "A24 film still", "Blade Runner 2049 color grade".

### Product
Surfaces: brushed aluminum, matte ceramic, condensation droplets, glass refraction.
Lighting: softbox studio lighting, rim light, seamless white cyclorama.
Anchors: "Apple product photography", "Bon Appetit feature spread".

### Portrait
Lens: 85mm f/1.4, shallow depth of field, catchlight in eyes.
Detail: skin texture, flyaway hairs, natural asymmetry.
Anchors: "Annie Leibovitz portrait", "Vogue cover shoot".

### Editorial
Styling: directional wind, motion blur on fabric, styled hair.
Anchors: "Wallpaper* design editorial", "i-D magazine spread".

### UI/Web
Style: flat vector, 2px stroke, consistent corner radius, brand color palette.
Constraint: transparent background, centered composition, no drop shadow unless specified.

### Logo
Construction: geometric grid, negative space, single/dual color, scalable at 16px.
Constraint: no gradients unless requested, must read at thumbnail size.

### Landscape
Depth: foreground/midground/background layering, atmospheric haze.
Light: blue hour, god rays through canopy, alpenglow on peaks.

### Abstract
Form: fluid dynamics, generative Voronoi patterns, chromatic aberration.
Anchors: "Refik Anadol installation", "Bridget Riley op-art".

### Infographic
Layout: grid-based hierarchy, numbered callouts, legible sans-serif labels.
Constraint: keep any rendered text under 25 characters per label.

## Proven Prompt Templates

**Photorealistic / editorial portrait:**
```
[Subject: age + appearance + expression], wearing [outfit with brand/texture],
[action verb] in [specific location + time]. [Micro-detail about skin/hair/
sweat/texture]. Captured with [camera model], [focal length] lens at [f-stop],
[lighting description]. [Prestigious context: "Vanity Fair editorial" /
"Pulitzer Prize-winning cover photograph"].
```

**Product / commercial:**
```
[Product with brand name] with [dynamic element: condensation/splashes/glow],
[product detail: "logo prominently displayed"], [surface/setting description].
[Supporting visual elements: light rays, particles, reflections].
Commercial photography for an advertising campaign. [Publication reference:
"Bon Appetit feature spread" / "Wallpaper* design editorial"].
```

**Illustrated / stylized:**
```
A [art style] [format] of [subject with character detail], featuring
[distinctive characteristics] with [color palette]. [Line style] and
[shading technique]. Background is [description]. [Mood/atmosphere].
```

**Text-heavy assets** (keep rendered text under 25 characters):
```
A [asset type] with the text "[exact text]" in [descriptive font style],
[placement and sizing]. [Layout structure]. [Color scheme]. [Visual
context and supporting elements].
```

**Logo:**
```
A minimalist logo mark for "[brand name]", [geometric construction:
"built from two overlapping circles"], in [1-2 brand colors], on a
plain white background. Flat vector style, scalable, no gradients,
no drop shadow.
```

**Landscape / environment:**
```
[Environment type] at [time of day], with [foreground element],
[midground element], and [background element] creating atmospheric
depth. [Weather/light condition]. Wide-angle composition, [lens if
photorealistic]. [Mood/atmosphere anchor].
```

## Safety Rephrase Strategies

When `IMAGE_SAFETY` or a false-positive filter blocks output:

1. **Abstraction** -- describe the concept indirectly rather than literally
2. **Artistic framing** -- add "digital painting of", "concept art depicting"
3. **Metaphor** -- substitute a metaphorical stand-in for the blocked element
4. Common fix: "dog" blocked → try "a friendly golden retriever in a sunny park"
5. Never retry more than 3 times without explicit user approval between attempts
6. If `PROHIBITED_CONTENT`, do not retry at all -- explain why and suggest a different concept
