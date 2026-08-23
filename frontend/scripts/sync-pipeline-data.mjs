import fs from 'node:fs';
import path from 'node:path';

const projectRoot = path.resolve(new URL('..', import.meta.url).pathname);
const outputDir = path.join(projectRoot, '..', 'output');
const frontendPublicDir = path.join(projectRoot, 'public');

const ensureDir = (dirPath) => {
  fs.mkdirSync(dirPath, { recursive: true });
};

const copyIfExists = (sourceFile, targetFile) => {
  if (!fs.existsSync(sourceFile)) return;
  ensureDir(path.dirname(targetFile));
  fs.copyFileSync(sourceFile, targetFile);
};

ensureDir(frontendPublicDir);
copyIfExists(path.join(outputDir, 'summary.json'), path.join(frontendPublicDir, 'etl', 'summary.json'));
copyIfExists(path.join(outputDir, 'processed.csv'), path.join(frontendPublicDir, 'etl', 'processed.csv'));
