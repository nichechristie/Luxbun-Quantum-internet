import type { AppProps } from "next/app";
import dynamic from "next/dynamic";

const CDPWrapper = dynamic(
  () => import("../components/CDPWrapper"),
  { ssr: false }
);

export default function App({ Component, pageProps }: AppProps) {
  return (
    <CDPWrapper>
      <Component {...pageProps} />
    </CDPWrapper>
  );
}
