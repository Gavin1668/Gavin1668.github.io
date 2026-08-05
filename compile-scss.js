const sass = require('sass');
const fs = require('fs');
const path = require('path');

const scssDir = path.join(__dirname, 'themes', 'hugo-theme-stack', 'assets', 'scss');
const inputFile = path.join(scssDir, 'style.scss');
const outputDir = path.join(__dirname, 'assets', 'css');
const outputFile = path.join(outputDir, 'style.css');

// Ensure output directory exists
fs.mkdirSync(outputDir, { recursive: true });

try {
    const result = sass.compile(inputFile, {
        loadPaths: [scssDir],
        style: 'compressed',
        sourceMap: false
    });

    fs.writeFileSync(outputFile, result.css);
    console.log('SCSS compiled successfully to', outputFile);
    console.log('CSS size:', (result.css.length / 1024).toFixed(2), 'KB');
} catch (error) {
    console.error('SCSS compilation failed:', error.message);
    process.exit(1);
}
