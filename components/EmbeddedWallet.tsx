import { SignIn, SignOutButton } from "@coinbase/cdp-react";
import { useIsSignedIn, useEvmAddress, useSolanaAddress } from "@coinbase/cdp-hooks";

export function EmbeddedWalletAuth() {
  const { isSignedIn } = useIsSignedIn();

  if (isSignedIn) {
    return <EmbeddedWalletDashboard />;
  }

  return (
    <div style={{ padding: "24px", maxWidth: "440px" }}>
      <SignIn authMethods={["email", "sms"]} />
      <p style={{ marginTop: "12px", fontSize: "12px", color: "#999", textAlign: "center" }}>
        A wallet will be created automatically when you sign in.
        No extensions or seed phrases needed.
      </p>
    </div>
  );
}

function EmbeddedWalletDashboard() {
  const { evmAddress } = useEvmAddress();
  const { solanaAddress } = useSolanaAddress();

  return (
    <div style={{ padding: "24px", maxWidth: "400px" }}>
      <h2 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "16px" }}>
        Your Embedded Wallet
      </h2>

      {evmAddress && (
        <div style={{ marginBottom: "16px" }}>
          <label style={{ fontSize: "12px", color: "#999", display: "block", marginBottom: "4px" }}>
            EVM Address (Base)
          </label>
          <code style={{
            display: "block",
            padding: "8px",
            background: "#111",
            borderRadius: "8px",
            fontSize: "13px",
            wordBreak: "break-all",
          }}>
            {evmAddress}
          </code>
        </div>
      )}

      {solanaAddress && (
        <div style={{ marginBottom: "16px" }}>
          <label style={{ fontSize: "12px", color: "#999", display: "block", marginBottom: "4px" }}>
            Solana Address
          </label>
          <code style={{
            display: "block",
            padding: "8px",
            background: "#111",
            borderRadius: "8px",
            fontSize: "13px",
            wordBreak: "break-all",
          }}>
            {solanaAddress}
          </code>
        </div>
      )}

      <SignOutButton
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "8px",
          background: "transparent",
          color: "#ff4444",
          border: "1px solid #ff4444",
          cursor: "pointer",
          marginTop: "8px",
        }}
      >
        Sign Out
      </SignOutButton>
    </div>
  );
}
