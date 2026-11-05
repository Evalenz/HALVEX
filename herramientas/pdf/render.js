// Renderiza los SVG de jobs.json a PNG (transparente o con fondo) y a PDF vectorial
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  for (const j of jobs) {
    const src = fs.readFileSync(j.svg, 'utf8');
    const vb = src.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    const ratio = vb[3] / vb[2];
    if (j.png) {
      const W = j.width, H = Math.round(W * ratio);
      const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
      const s = src.replace(/width="[^"]+" height="[^"]+"/, `width="${W}" height="${H}"`);
      await p.setContent(`<html><body style="margin:0;background:transparent">${s}</body></html>`);
      await p.screenshot({ path: j.png, omitBackground: j.transparent, clip: { x: 0, y: 0, width: W, height: H } });
      await p.close();
    } else if (j.pdf) {
      // PDF a 100 mm de ancho, vectorial
      const wmm = 100, hmm = 100 * ratio;
      const p = await b.newPage();
      const s = src.replace(/width="[^"]+" height="[^"]+"/, `width="${wmm}mm" height="${hmm}mm"`);
      await p.setContent(`<html><head><style>@page{size:${wmm}mm ${hmm}mm;margin:0}html,body{margin:0}svg{display:block}</style></head><body>${s}</body></html>`);
      await p.pdf({ path: j.pdf, width: `${wmm}mm`, height: `${hmm}mm`, printBackground: true, pageRanges: '1' });
      await p.close();
    }
  }
  await b.close();
  console.log('ok', jobs.length);
})();
