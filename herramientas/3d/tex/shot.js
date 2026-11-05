const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:parseFloat(process.argv[4]||'3.2'),viewport:{width:1400,height:1000}});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);
for(const id of ['card_front','card_back','letter','envelope','env_back','notebook','compliment','folder','card_emboss','nb_emboss']){const el=await p.$('#'+id+' > div');await el.screenshot({path:process.argv[3]+'/'+id+'.png'});}
await b.close()})();
