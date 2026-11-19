// Entry program for gta6-meme-x-01 (Node 22, standard library only).
//
// The entry is the X post itself, not this program: the house reads the post
// from X (its first picture and its text) and hands that to the judge. All
// this program does is copy POST.json from the repository root into the
// output directory, where the gate reads it to learn the post's address.
//
// POST.json holds {"url": "https://x.com/<handle>/status/<id>"} once the
// meme has been posted. Until then it carries the starter's placeholder,
// which the gate refuses — fill it in before you submit.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  // Fail loudly on a malformed POST.json instead of copying a bad address.
  const raw = readFileSync(join(BOT_DIR, 'POST.json'), 'utf8');
  const parsed = JSON.parse(raw) as { url?: unknown };
  if (typeof parsed.url !== 'string' || !parsed.url.startsWith('https://')) {
    throw new Error('POST.json has no https url field');
  }
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`could not copy POST.json from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
