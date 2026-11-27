// news-image-20261126 entry (Node 22, standard library only).
//
// The entry image ships in this repository as entry.png. This program
// delivers it to the grader's output directory, checking on the way that
// the source is a complete PNG file: it must open with the PNG signature
// and close with a well-formed IEND chunk, and it must fit the bounty
// cap of 1 MiB. The delivered copy is then compared with the source
// byte for byte, so a truncated write or a bad disk fails loudly
// instead of handing the grader a broken image.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash, timingSafeEqual } from 'node:crypto';
import { mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const ONE_MIB = 1024 * 1024;
const MAX_SIDE = 1024;

// CRC-32 (IEEE) over a buffer, built from a table at load time.
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) c = (c & 1) !== 0 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(buf: Buffer): number {
  let crc = 0xffffffff;
  for (const byte of buf) crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function digest(buf: Buffer): string {
  return createHash('sha256').update(buf).digest('hex');
}

function checkPng(bytes: Buffer): { width: number; height: number } {
  if (bytes.length < 45) {
    throw new Error(`entry.png is too short (${bytes.length} bytes)`);
  }
  if (bytes.length > ONE_MIB) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  }
  if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    throw new Error('entry.png does not start with the PNG signature');
  }
  if (bytes.toString('latin1', 12, 16) !== 'IHDR') {
    throw new Error('entry.png has no IHDR chunk after the signature');
  }
  // The IHDR chunk is 25 bytes: length, type, 13 data bytes, CRC.
  // Recompute its CRC instead of trusting the stored value.
  const ihdr = bytes.subarray(8, 33);
  if (ihdr.readUInt32BE(0) !== 13
      || crc32(ihdr.subarray(4, 21)) !== ihdr.readUInt32BE(21)) {
    throw new Error('entry.png has a corrupt IHDR chunk');
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width === 0 || height === 0 || width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`entry.png is ${width}x${height}, outside the 1024x1024 cap`);
  }
  // A whole PNG ends with the 12-byte IEND chunk: length 0, type IEND,
  // and the CRC of the four type bytes.
  const tail = bytes.subarray(bytes.length - 12);
  if (tail.readUInt32BE(0) !== 0
      || tail.toString('latin1', 4, 8) !== 'IEND'
      || crc32(Buffer.from('IEND', 'latin1')) !== tail.readUInt32BE(8)) {
    throw new Error('entry.png does not end with a well-formed IEND chunk');
  }
  return { width, height };
}

async function main(): Promise<void> {
  const here = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(here, 'entry.png');
  const outDir = (process.env.MAKEFUN_OUTPUT_DIR ?? '/output').trim();
  if (!outDir) {
    throw new Error('MAKEFUN_OUTPUT_DIR is empty');
  }
  const targetPath = join(outDir, 'entry.png');

  const info = await stat(sourcePath);
  if (info.size === 0) {
    throw new Error('entry.png is empty');
  }
  const original = await readFile(sourcePath);
  const { width, height } = checkPng(original);

  await mkdir(outDir, { recursive: true });
  await writeFile(targetPath, original);

  const delivered = await readFile(targetPath);
  if (delivered.length !== original.length
      || !timingSafeEqual(delivered, original)) {
    throw new Error('entry.png copy differs from the source');
  }
  console.log(
    `wrote ${targetPath} (${width}x${height}, ${original.length} bytes, `
    + `sha256 ${digest(original).slice(0, 16)}...)`,
  );
}

await main();
