const fs = require('fs');
const path = require('path');

const outDir = path.resolve(__dirname, '../out');
const enDir = path.join(outDir, 'en');
const enHtml = path.join(outDir, 'en.html');
const indexHtml = path.join(outDir, 'index.html');

console.log('[prepare_pages] Mirroring English locale output to root...');

// 1. Ensure out/index.html exists from en.html
if (fs.existsSync(enHtml)) {
  fs.copyFileSync(enHtml, indexHtml);
  console.log('[prepare_pages] Copied out/en.html -> out/index.html');
}

// Next's client navigation requests /index.txt for the root route.
// Mirror the English RSC payload alongside the HTML to avoid a home prefetch 404.
const enPayload = path.join(outDir, 'en.txt');
if (fs.existsSync(enPayload)) {
  fs.copyFileSync(enPayload, path.join(outDir, 'index.txt'));
}

// 2. Recursively mirror out/en to out/
function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      if (!fs.existsSync(destPath)) {
        fs.mkdirSync(destPath, { recursive: true });
      }
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

if (fs.existsSync(enDir)) {
  copyRecursive(enDir, outDir);
  console.log('[prepare_pages] Mirrored out/en/* to out/*');
}

// 3. Ensure _headers and _redirects are in out/
const publicDir = path.resolve(__dirname, '../public');
['_headers', '_redirects'].forEach((file) => {
  const src = path.join(publicDir, file);
  const dest = path.join(outDir, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dest);
    console.log(`[prepare_pages] Copied public/${file} -> out/${file}`);
  }
});

// 4. Ensure each .html file also has a folder/index.html for servers without clean-URL rewrite
function ensureDirectoryIndexes(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name !== '_next') {
        ensureDirectoryIndexes(fullPath);
      }
    } else if (entry.name.endsWith('.html') && entry.name !== 'index.html' && entry.name !== '404.html') {
      const baseName = entry.name.slice(0, -5);
      const targetDir = path.join(dir, baseName);
      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
      }
      const targetIndex = path.join(targetDir, 'index.html');
      if (!fs.existsSync(targetIndex)) {
        fs.copyFileSync(fullPath, targetIndex);
      }
    }
  }
}

ensureDirectoryIndexes(outDir);
console.log('[prepare_pages] Directory indexes generated.');

console.log('[prepare_pages] Preparation completed successfully.');
