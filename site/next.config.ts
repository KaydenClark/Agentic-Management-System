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

// Routes whose draft mark is removed, as a JSON list. Only scripts/build.mjs
// sets it, after matching each built page's content hash against
// approvals.json; unset, every page keeps its mark.
function approvedRoutes(): string {
  const raw = process.env.AMS_APPROVED_ROUTES || "[]";
  const routes: unknown = JSON.parse(raw);
  if (!Array.isArray(routes) || !routes.every((r) => typeof r === "string")) throw new Error("AMS_APPROVED_ROUTES must be a JSON list of routes");
  return JSON.stringify(routes);
}

const nextConfig: NextConfig = {
  env: { AMS_COMMIT_SHA: commitSha(), AMS_APPROVED_ROUTES: approvedRoutes() },
};

export default nextConfig;
