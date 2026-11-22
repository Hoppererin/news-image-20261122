// news-image-20261122 — "The World Today": one image summing up Sunday
// 22 November 2026 — 47 real stories from 7 regions, drawn as a newspaper
// front page.
//
// The image (entry.png, 1024x1024) is drawn in this repo by render.py
// (Python + Pillow + DejaVu, deterministic — running it twice writes
// byte-identical bytes). This program only copies that file to the output
// directory. Node 22, standard library only, no network, no randomness,
// no timestamps. It never deletes the output directory: the grader mounts
// /output, so removing it would fail the run.
// Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoDir, "entry.png"), join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
