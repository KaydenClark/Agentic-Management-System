import { execFileSync } from "node:child_process";
import type { NextConfig } from "next";

// The commit shown in every page's footer, fixed at build time: Vercel's
// build variable, else the checkout's HEAD, else "unknown".
function commitSha(): string {
  if (process.env.VERCEL_GIT_COMMIT_SHA) return process.env.VERCEL_GIT_COMMIT_SHA;
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
  } catch {
    return "unknown";
  }
}

const nextConfig: NextConfig = {
  env: { AMS_COMMIT_SHA: commitSha() },
};

export default nextConfig;
