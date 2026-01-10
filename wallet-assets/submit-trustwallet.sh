#!/bin/bash
# Submit LUXBIN token logo to Trust Wallet Assets
# This makes the logo appear in MetaMask, Coinbase Wallet, Trust Wallet, etc.

set -e

echo "🎨 LUXBIN Token - Trust Wallet Assets Submission"
echo "=" | tr '\n' '=' | head -c 60 && echo ""
echo ""

# Configuration
TRUST_WALLET_REPO="trustwallet/assets"
FORK_OWNER="mermaidnicheboutique-code"
BRANCH_NAME="add-luxbin-token-$(date +%s)"
TOKEN_ADDRESS="0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0"
WORK_DIR="/tmp/trust-wallet-fork-$$"

echo "📋 Configuration:"
echo "   Token: LUXBIN Quantum Token (LUX)"
echo "   Address: $TOKEN_ADDRESS"
echo "   Chain: Base (8453)"
echo ""

# Step 1: Fork repository if needed
echo "Step 1: Checking/Creating fork of Trust Wallet Assets..."
if gh repo view "$FORK_OWNER/assets" >/dev/null 2>&1; then
    echo "✅ Fork already exists"
else
    echo "🔄 Creating fork..."
    gh repo fork "$TRUST_WALLET_REPO" --clone=false --remote=false
    echo "✅ Fork created"
    sleep 5
fi
echo ""

# Step 2: Clone fork
echo "Step 2: Cloning fork..."
git clone "https://github.com/$FORK_OWNER/assets.git" "$WORK_DIR"
cd "$WORK_DIR"
echo "✅ Fork cloned"
echo ""

# Step 3: Create branch
echo "Step 3: Creating branch..."
git checkout -b "$BRANCH_NAME"
echo "✅ Branch created: $BRANCH_NAME"
echo ""

# Step 4: Create directory structure
echo "Step 4: Setting up directory structure..."
ASSET_DIR="blockchains/base/assets/$TOKEN_ADDRESS"
mkdir -p "$ASSET_DIR"
echo "✅ Directory created: $ASSET_DIR"
echo ""

# Step 5: Copy logo
echo "Step 5: Adding logo..."
cp /Users/nicholechristie/luxbin-quantum-internet/wallet-assets/logo-256.png "$ASSET_DIR/logo.png"
git add "$ASSET_DIR/logo.png"
echo "✅ Logo added (256x256 PNG)"
echo ""

# Step 6: Copy token info
echo "Step 6: Adding token info..."
cp /Users/nicholechristie/luxbin-quantum-internet/wallet-assets/token-info.json "$ASSET_DIR/info.json"
git add "$ASSET_DIR/info.json"
echo "✅ Token info added"
echo ""

# Step 7: Commit
echo "Step 7: Committing changes..."
git config user.name "mermaidnicheboutique-code"
git config user.email "nicholechristie555@gmail.com"
git commit -m "Add LUXBIN Quantum Token (LUX) on Base

- Token: LUXBIN Quantum Token
- Symbol: LUX
- Chain: Base (8453)
- Contract: $TOKEN_ADDRESS
- First quantum-powered DeFi token
- 445 qubits from IBM quantum computers"
echo "✅ Changes committed"
echo ""

# Step 8: Push
echo "Step 8: Pushing to fork..."
git push origin "$BRANCH_NAME"
echo "✅ Pushed to fork"
echo ""

# Step 9: Create Pull Request
echo "Step 9: Creating Pull Request..."

PR_BODY=$(cat <<'EOF'
## Token Information

**Name**: LUXBIN Quantum Token
**Symbol**: LUX
**Type**: ERC20
**Decimals**: 18
**Chain**: Base (8453)
**Contract**: 0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0

## Links

- **BaseScan**: https://basescan.org/token/0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0
- **GitHub**: https://github.com/mermaidnicheboutique-code/luxbin-quantum-internet
- **DOI**: https://doi.org/10.5281/zenodo.18198505

## Description

LUXBIN Quantum Token is the first cryptocurrency powered by 445 qubits from IBM quantum computers. It brings quantum-secured DeFi to Base with:

- Quantum entropy oracle (real quantum randomness)
- Staking with quantum-boosted rewards (20-140% APY)
- Quantum lottery (provably fair)
- Gasless transactions via Coinbase Paymaster

## Verification

- ✅ Contract verified on BaseScan
- ✅ Open-source (MIT License)
- ✅ Deployed on Base mainnet
- ✅ Active development
- ✅ Logo: 256x256 PNG

## Files Added

- `blockchains/base/assets/0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0/logo.png`
- `blockchains/base/assets/0xbB5bf2139CbACDeE52991cf32f9c4d558B9464d0/info.json`

Thank you for reviewing!
EOF
)

gh pr create \
    --repo "$TRUST_WALLET_REPO" \
    --base master \
    --head "$FORK_OWNER:$BRANCH_NAME" \
    --title "Add LUXBIN Quantum Token (LUX) on Base" \
    --body "$PR_BODY"

PR_URL=$(gh pr list --repo "$TRUST_WALLET_REPO" --head "$FORK_OWNER:$BRANCH_NAME" --json url --jq '.[0].url')

echo "✅ Pull Request created!"
echo ""
echo "=" | tr '\n' '=' | head -c 60 && echo ""
echo "🎉 SUBMISSION COMPLETE!"
echo "=" | tr '\n' '=' | head -c 60 && echo ""
echo ""
echo "📝 Pull Request URL:"
echo "   $PR_URL"
echo ""
echo "⏰ Timeline:"
echo "   - PR Review: 1-7 days"
echo "   - After merge: Logo appears in wallets within 24 hours"
echo ""
echo "💡 Your logo will appear in:"
echo "   - MetaMask"
echo "   - Coinbase Wallet"
echo "   - Trust Wallet"
echo "   - Rainbow Wallet"
echo "   - And more!"
echo ""

# Cleanup
cd /
rm -rf "$WORK_DIR"

echo "✨ All done! Check your PR at: $PR_URL"
