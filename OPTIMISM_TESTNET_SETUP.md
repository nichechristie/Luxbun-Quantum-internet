# Optimism Local Testnet Setup

This guide helps you set up your own local Optimism testnet for development and testing.

## Installation

Run the following command to install the `op-up` tool:

```bash
curl https://raw.githubusercontent.com/ethereum-optimism/optimism/develop/op-up/install.sh | sh
```

## Reload Shell Configuration

Reload your shell configuration to recognize the `op-up` command:

```bash
source ~/.bashrc  # or ~/.zshrc on macOS
```

## Start the Local Chain

Run the following command to start your local Optimism testnet:

```bash
op-up
```

## Testnet Details

Once running, your testnet will provide:

- **Test Account Address**: `0x5D284fe6D6AEb73857960a0D041CF394b1198392`
- **Test Account Private Key**: `0xd9fb56b9574ed61ab0478a607166eeb3a80b1b91ab1bf00f45932105d07b5e11`
- **EL Node URL**: `http://localhost:8545`

The chain will start producing L2 blocks automatically.

## Usage

Connect your applications, wallets, or scripts to `http://localhost:8545` to interact with the testnet. The test account is pre-funded for testing transactions.