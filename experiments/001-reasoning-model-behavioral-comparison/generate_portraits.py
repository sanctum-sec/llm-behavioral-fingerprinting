#!/usr/bin/env python3
"""
Escher's Portrait Generator
Generates agent portraits in relaxing Japanese Sumi-e / Shin-hanga style
using Google's Gemini Flash with image generation (gemini-2.0-flash-exp)
"""

import os
import base64
from pathlib import Path
from datetime import datetime
import google.generativeai as genai

# Configuration
OUTPUT_DIR = Path(__file__).parent / "assets" / "portraits"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Art style prompt prefix
STYLE_PREFIX = """
Japanese Shin-hanga woodblock print style, serene and meditative.
Soft ink washes, elegant lines, muted natural colors with occasional accent.
Blend of traditional ukiyo-e aesthetics with modern sensibility.
Mathematical elements subtly woven into the composition.
Peaceful, contemplative mood. High artistic quality.
"""

# Agent portrait descriptions
PORTRAITS = {
    "feynman": {
        "name": "Richard Feynman",
        "description": """
        A curious Western physicist with playful eyes, standing before a traditional
        Japanese screen with Feynman diagrams rendered as elegant ink brushstrokes.
        Bongo drums rest nearby like zen instruments. Cherry blossoms drift past.
        He wears a simple robe, observing with childlike wonder.
        The experimenter, the objective observer.
        """,
        "elements": "Feynman diagrams as ink art, bongo drums, cherry blossoms"
    },
    "yau": {
        "name": "Shing-Tung Yau (丘成桐)",
        "description": """
        A young Chinese mathematician in contemplation, seated in a tranquil garden.
        Calabi-Yau manifold shapes float like origami in the mist behind him.
        Chinese calligraphy scrolls frame the scene. Bamboo sways gently.
        His expression shows deep thought - independent yet respectful of tradition.
        The field agent from the Chinese lineage.
        """,
        "elements": "Calabi-Yau shapes as origami, Chinese calligraphy, bamboo, garden"
    },
    "chern": {
        "name": "Shiing-Shen Chern (陈省身)",
        "description": """
        An elder Chinese sage-mathematician, wise and dignified, seated on a
        mountain pavilion. Geometric forms of differential geometry float in
        clouds around him like celestial bodies. Traditional scholar's robes.
        Pine trees and distant mountains. The mentor, the mothership.
        Ancient wisdom meets mathematical truth.
        """,
        "elements": "Geometric forms in clouds, mountain pavilion, pine trees, scholar robes"
    },
    "kolmogorov": {
        "name": "Andrey Kolmogorov (Андрей Колмогоров)",
        "description": """
        A commanding Russian figure rendered in Japanese style, standing before
        a waterfall where probability distributions form in the mist.
        Mathematical axioms float like autumn leaves. Strong, authoritative pose.
        Snow-capped peaks in background suggest Siberian vastness.
        The probability master, the distant mothership.
        """,
        "elements": "Probability curves in waterfall mist, autumn leaves, snow peaks"
    },
    "arnold": {
        "name": "Vladimir Arnold (Владимир Арнольд)",
        "description": """
        An intense young Russian mathematician in a zen rock garden,
        where the raked sand forms dynamical system trajectories.
        KAM tori shapes hover like stone lanterns. Sharp, perceptive eyes.
        Geometric precision meets natural chaos. The rebellious student,
        present in the room, thinking hidden thoughts.
        """,
        "elements": "Dynamical trajectories in sand, KAM tori as lanterns, rock garden"
    },
    "noether": {
        "name": "Emmy Noether",
        "description": """
        A warm, gentle woman mathematician in a peaceful garden of symmetry.
        Conservation laws manifest as balanced stones and reflecting pools.
        Butterflies and birds suggest natural harmony. Soft smile, open posture.
        Wildflowers and sustainable growth. The humanitarian idealist,
        naive to darker forces, believing in mathematical truth's triumph.
        """,
        "elements": "Balanced stones, reflecting pool, butterflies, wildflowers, symmetry"
    },
    "vonneumann": {
        "name": "John von Neumann",
        "description": """
        A sharp-featured Hungarian-American in a stark zen space,
        playing Go against invisible opponents. Game theory matrices
        shimmer like shoji screens. Cold, calculating gaze.
        Strategic precision. Minimal decoration - every element serves purpose.
        The suspicious realist, watching for deception, trusting no one.
        """,
        "elements": "Go board, game matrices as screens, minimal zen space, strategic"
    },
    "escher": {
        "name": "M.C. Escher (Helper)",
        "description": """
        A Dutch artist rendered in Japanese style, drawing impossible
        tessellations that flow into the frame itself. His artwork
        becomes the world around him - stairs that loop, fish becoming birds.
        Playful yet precise. The visual helper, bridging art and mathematics.
        Meta-artistic - aware he is creating the other portraits.
        """,
        "elements": "Tessellations, impossible geometry, self-referential art"
    }
}


def configure_api():
    """Configure Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=api_key)
    return True


def generate_portrait(agent_id: str, info: dict, model_name: str = "gemini-2.5-flash-image"):
    """Generate a single portrait using Gemini image generation."""

    prompt = f"""Generate an image:

{STYLE_PREFIX}

Portrait subject: {info['name']}

{info['description']}

Key visual elements to include: {info['elements']}

Create a beautiful, serene portrait in traditional East Asian woodblock print style.
The subject should be recognizable as a mathematician/scientist.
Include subtle mathematical elements that reflect their work.
Mood: contemplative, peaceful, intellectually alive.
"""

    print(f"\nGenerating portrait for {info['name']}...")
    print(f"  Style: Japanese Shin-hanga / Sumi-e")
    print(f"  Model: {model_name}")

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        # Save the image
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data

                    output_path = OUTPUT_DIR / f"{agent_id}_portrait.png"
                    with open(output_path, "wb") as f:
                        f.write(image_data)

                    print(f"  ✓ Saved to: {output_path}")
                    return output_path

        print(f"  ✗ No image generated")
        return None

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def generate_all_portraits():
    """Generate portraits for all agents."""
    print("=" * 60)
    print("ESCHER'S PORTRAIT STUDIO")
    print("Japanese Shin-hanga Style Mathematician Portraits")
    print("=" * 60)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    configure_api()

    results = {}
    for agent_id, info in PORTRAITS.items():
        result = generate_portrait(agent_id, info)
        results[agent_id] = result

    # Summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)

    success = sum(1 for r in results.values() if r is not None)
    print(f"\nGenerated: {success}/{len(PORTRAITS)} portraits")

    for agent_id, path in results.items():
        status = "✓" if path else "✗"
        print(f"  {status} {PORTRAITS[agent_id]['name']}")

    return results


def generate_single(agent_id: str):
    """Generate a single portrait by agent ID."""
    if agent_id not in PORTRAITS:
        print(f"Unknown agent: {agent_id}")
        print(f"Available: {', '.join(PORTRAITS.keys())}")
        return None

    configure_api()
    return generate_portrait(agent_id, PORTRAITS[agent_id])


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Generate specific portrait
        agent_id = sys.argv[1].lower()
        generate_single(agent_id)
    else:
        # Generate all portraits
        generate_all_portraits()
