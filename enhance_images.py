#!/usr/bin/env python3
"""
Industrias Maral — Batch Image Enhancer
Descarga imágenes originales de WordPress y las mejora con Gemini API.

REQUISITOS:
  pip install google-generativeai requests pillow

ANTES DE CORRER:
  Activa billing en https://aistudio.google.com/apikey
  (cuesta ~$0.04 por imagen con Imagen 4 Fast = ~$1.40 para las 35 fotos)
"""

import os, time, base64, requests, json
from pathlib import Path

# ── CONFIG ──────────────────────────────────────────────────────────────
API_KEY      = "AIzaSyALkv-vxbmjH7tcze0y9M-WTEA6OIBBZqI"
SOURCE_BASE  = "https://industriasmaral.com/wp-content/uploads/2023/03/"
OUT_DIR      = Path(__file__).parent / "img"
DELAY_SEC    = 4   # pausa entre requests para no saturar la API

IMAGES = [
    "101.png", "101-1.png", "103.png", "103-3.png", "104.png",
    "106.png", "119.png",  "111.png", "108.png",   "107.png",
    "105.png", "109.png",  "110.png", "117.png",
    "201.png", "203.png",  "205.png", "206.png",   "207.png",
    "301.png", "301-3.png","302.png", "305.png",   "307.png",
    "308.png", "315-PL.png",
    "mr801.png","mr801b.png","mr802.png","mr803.png","mr805.png",
    "mr415.png","mr416.png","mr430-2.png","mr430.png",
]

ENHANCEMENT_PROMPT = """
You are an expert commercial product photographer and retoucher.
I will give you a product photo of a radio antenna (MAXANT / MARAL brand).

Your task: Re-render the same exact antenna with dramatically improved studio quality.

STRICT RULES — do NOT violate these:
- Keep the EXACT same antenna model, geometry, proportions and brand markings
- Do NOT change the antenna shape, connector, or any identifying feature
- Do NOT add or remove parts, labels, or accessories

BACKGROUND:
- Replace the current white/plain background with a dark charcoal gradient (#1a1a1a center, #0a0a0a edges)
- Subtle radial highlight beneath the antenna (floor reflection)
- No props, no context, pure product shot

LIGHTING (cinematic studio):
- Primary light: directional from upper-left, warm 5600K, specular highlights on metallic parts
- Fill light: soft cool-toned from right, ratio 3:1
- Rim light: subtle backlight to separate antenna from background
- No flat lighting, no blown-out highlights, no harsh shadows

RENDERING QUALITY:
- Sony A1 equivalent: 85mm f/1.4 at f/2.0, ISO 100, 1/200s
- Deep dynamic range, micro-contrast on metallic textures
- Real material texture: chrome shows brushed/polished detail, plastic shows engineering-grade finish
- Subtle film grain (ISO-equivalent), 10-bit color, cinematic contrast curve
- 4K equivalent resolution, sharp focus on antenna body and connector

OUTPUT: Same framing/crop as input, vertical portrait product shot.
No watermarks. No text additions.
"""

# ── HELPERS ──────────────────────────────────────────────────────────────
def download_image(filename: str) -> bytes | None:
    url = SOURCE_BASE + filename
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        print(f"  ↓ Downloaded {filename} ({len(r.content):,} bytes)")
        return r.content
    except Exception as e:
        print(f"  ✗ Could not download {filename}: {e}")
        return None

def enhance_with_gemini(img_bytes: bytes, filename: str) -> bytes | None:
    """Send image to Gemini gemini-2.5-flash-image for enhancement."""
    b64 = base64.b64encode(img_bytes).decode()
    # Detect mime type
    mime = "image/png" if filename.lower().endswith(".png") else "image/jpeg"

    payload = {
        "contents": [{
            "parts": [
                {"text": ENHANCEMENT_PROMPT},
                {"inlineData": {"mimeType": mime, "data": b64}}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
    try:
        r = requests.post(url, json=payload, timeout=120)
        data = r.json()
        if "error" in data:
            print(f"  ✗ API error: {data['error']['message'][:120]}")
            return None
        parts = data["candidates"][0]["content"]["parts"]
        for p in parts:
            if "inlineData" in p:
                return base64.b64decode(p["inlineData"]["data"])
        print("  ✗ No image in response")
        return None
    except Exception as e:
        print(f"  ✗ Request failed: {e}")
        return None

# ── MAIN ─────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(exist_ok=True)
    total = len(IMAGES)
    success = 0
    skipped = 0

    print(f"\n{'─'*55}")
    print(f"  Industrias Maral — Image Enhancer")
    print(f"  Processing {total} product images")
    print(f"{'─'*55}\n")

    for i, filename in enumerate(IMAGES, 1):
        out_path = OUT_DIR / filename
        print(f"[{i:02d}/{total}] {filename}")

        # Skip if already processed
        if out_path.exists() and out_path.stat().st_size > 10_000:
            print(f"  ✓ Already exists, skipping")
            skipped += 1
            continue

        # Download original
        img_bytes = download_image(filename)
        if not img_bytes:
            continue

        # Save original as fallback
        orig_path = OUT_DIR / f"_orig_{filename}"
        orig_path.write_bytes(img_bytes)

        # Enhance
        print(f"  ✦ Enhancing with Gemini...")
        enhanced = enhance_with_gemini(img_bytes, filename)

        if enhanced:
            out_path.write_bytes(enhanced)
            print(f"  ✓ Saved enhanced → img/{filename} ({len(enhanced):,} bytes)")
            success += 1
        else:
            # Fallback: save original
            out_path.write_bytes(img_bytes)
            print(f"  ⚠ Using original as fallback → img/{filename}")

        # Rate limit
        if i < total:
            time.sleep(DELAY_SEC)

    print(f"\n{'─'*55}")
    print(f"  Done: {success} enhanced, {skipped} skipped, {total-success-skipped} fallback")
    print(f"  Images saved to: {OUT_DIR}")
    print(f"\n  Next step: in tienda.html change IMG path from")
    print(f"    '../Maral/wp-content/uploads/2023/03/'")
    print(f"  to './img/'")
    print(f"{'─'*55}\n")

if __name__ == "__main__":
    main()
