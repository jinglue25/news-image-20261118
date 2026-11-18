// Copy the bundled news infographic into MAKEFUN_OUTPUT_DIR (default: /output).
// Run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFile, mkdir, access } from 'node:fs/promises';
import { constants } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const source = fileURLToPath(new URL('./entry.png', import.meta.url));
const outputDirectory = resolve(process.env.MAKEFUN_OUTPUT_DIR || '/output');

try {
  await access(source, constants.R_OK);
} catch {
  console.error(`Error: entry.png is missing or unreadable next to main.ts (${source}). Run python3 draw.py first.`);
  process.exit(1);
}

try {
  await mkdir(outputDirectory, { recursive: true });
  const destination = join(outputDirectory, 'entry.png');
  if (resolve(dirname(source)) !== outputDirectory) {
    await copyFile(source, destination);
  }
  console.log(`Saved ${destination}`);
} catch (error) {
  console.error(`Error: could not copy entry.png: ${error.message}`);
  process.exit(1);
}
