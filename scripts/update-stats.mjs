#!/usr/bin/env node
// Refreshes the dynamic values in the README neofetch block:
//   - Uptime  : years since the 2020 start, computed from today
//   - Repos   : current public repository count from the GitHub API
// Run: node scripts/update-stats.mjs   (no dependencies, Node 18+)

import { readFileSync, writeFileSync } from "node:fs";

const USER = "muneebnawaz018";
const START_YEAR = 2020;
const README = new URL("../README.md", import.meta.url);

const years = new Date().getFullYear() - START_YEAR;

let repos = null;
try {
  const res = await fetch(`https://api.github.com/users/${USER}`, {
    headers: {
      "User-Agent": USER,
      ...(process.env.GITHUB_TOKEN
        ? { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` }
        : {}),
    },
  });
  if (res.ok) repos = (await res.json()).public_repos;
} catch {
  // offline or rate-limited: leave the repo count untouched
}

let md = readFileSync(README, "utf8");
const before = md;

md = md.replace(
  /(Uptime\s+)\d+\+ years in production/,
  `$1${years}+ years in production`
);

if (typeof repos === "number") {
  md = md.replace(
    /(Repos\s+)\d+ public repositories on GitHub/,
    `$1${repos} public repositories on GitHub`
  );
}

if (md === before) {
  console.log("Stats already current. No change.");
} else {
  writeFileSync(README, md);
  console.log(`Updated stats: ${years}+ years` + (repos != null ? `, ${repos} repos` : ""));
}
