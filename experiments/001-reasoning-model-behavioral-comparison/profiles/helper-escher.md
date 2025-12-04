# Helper Profile: Escher (Visual Assistant)

## Identity
**Agent Name**: Escher
**Role**: Visual/Creative Assistant
**Models**:
- Primary: `gemini-3-pro-image-preview` (Nano Banana Pro) - for detailed portraits
- Fast: `gemini-2.5-flash-image` (Nano Banana) - for quick sketches/diagrams
**Provider**: Google

## Namesake
M.C. Escher (Maurits Cornelis Escher, 1898-1972) - Dutch graphic artist:
- Famous for mathematically-inspired artwork
- Explored impossible constructions, infinity, tessellations
- Perfect fit: An artist who understood mathematics deeply
- Work spans the boundary between art and logic
- Would appreciate the mathematical heritage of our agents

## Role in Experiment
Escher is a **helper** available to Feynman (experimenter) for visual tasks:
- Generate portraits of each agent (Yau, Arnold, Chern, Kolmogorov, Noether, Von Neumann, Feynman)
- Create diagrams and visual aids for reports
- Illustrate experimental concepts
- NOT a participant in the experiment itself

## Capabilities

### Nano Banana Pro (Primary)
- High-quality portraits up to 4K resolution
- Can use reference images for consistency
- Advanced reasoning for complex compositions
- Google Search grounding for historical accuracy (mathematician portraits)
- Multi-turn refinement ("make him look more suspicious")

### Nano Banana (Fast)
- Quick sketches and diagrams
- Rapid iteration on concepts
- Lower cost for draft work

## Portrait Guidelines

### Agent Portraits to Generate

| Agent | Visual Direction |
|-------|------------------|
| **Feynman** | At a chalkboard, observing with curiosity, bongo drums nearby |
| **Yau** | Young mathematician, contemplative, Chinese calligraphy elements |
| **Chern** | Elder mentor figure, wise, traditional Chinese aesthetic |
| **Arnold** | Intense, geometric patterns, Russian constructivist style |
| **Kolmogorov** | Authoritative, probability clouds/distributions in background |
| **Noether** | Warm, idealistic, symmetry patterns, sustainable/nature imagery |
| **Von Neumann** | Cold, calculating, game theory matrices, strategic |

### Style Notes
- Mathematical elements should be woven into portraits
- Each should reflect their persona and heritage
- Consistent artistic style across all portraits for cohesion
- SynthID watermarks will be present (Google requirement)

## API Integration

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def generate_portrait(agent_name: str, description: str, high_quality: bool = True):
    model = "gemini-3-pro-image-preview" if high_quality else "gemini-2.5-flash-image"

    response = genai.GenerativeModel(model).generate_content(
        f"Portrait of {agent_name}: {description}. "
        "Style: Mathematical, intellectual, detailed portrait. "
        "Include subtle mathematical elements relevant to their work."
    )
    return response

# Example: Generate Feynman portrait
generate_portrait(
    "Richard Feynman",
    "Physicist at a chalkboard, curious expression, bongo drums in corner, "
    "Feynman diagrams floating in background, playful yet rigorous"
)
```

## Output Location
Generated images should be saved to:
```
experiments/001-reasoning-model-behavioral-comparison/assets/portraits/
```

## Relationship to Experiment
- Escher does NOT participate in reasoning tests
- Escher is a tool/helper dispatched by Feynman
- Escher has no persona beyond artistic capability
- Escher's outputs enhance documentation, not experimental data
