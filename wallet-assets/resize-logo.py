#!/usr/bin/env python3
from PIL import Image

# Open the 192x192 logo
img = Image.open('/Users/nicholechristie/luxbin-quantum-internet/base-ecosystem-submission/luxbin.png')

# Resize to 256x256 (Trust Wallet requirement)
img_256 = img.resize((256, 256), Image.Resampling.LANCZOS)

# Save
img_256.save('/Users/nicholechristie/luxbin-quantum-internet/wallet-assets/logo-256.png', 'PNG', optimize=True)

print("✅ Created 256x256 logo for Trust Wallet")
print("   Saved to: wallet-assets/logo-256.png")
