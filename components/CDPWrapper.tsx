import { CDPReactProvider, type Config as CDPConfig } from "@coinbase/cdp-react";

const cdpConfig: CDPConfig = {
  projectId: process.env.NEXT_PUBLIC_COINBASE_PROJECT_ID || "",
  appName: "Luxbin",
  appLogoUrl: "https://quantum-internet.vercel.app/favicon.svg",
};

export default function CDPWrapper({ children }: { children: React.ReactNode }) {
  return (
    <CDPReactProvider config={cdpConfig}>
      {children}
    </CDPReactProvider>
  );
}
