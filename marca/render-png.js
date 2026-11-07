// Renderiza el isotipo de titanio (como en el hero) y el nombre en PNG con fondo transparente.
const {chromium}=require('playwright');
const OUT=process.argv[2];
const S=4096; // se renderiza grande y luego se reduce para suavizar bordes
const html=`<!doctype html><html><body style="margin:0;background:transparent">
<canvas id="c" width="${S}" height="${S}"></canvas>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}</script>
<script type="module">
import * as THREE from 'three';
const cv=document.getElementById('c');
const r=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,preserveDrawingBuffer:true});
r.setPixelRatio(1);r.setSize(${S},${S},false);r.outputColorSpace=THREE.SRGBColorSpace;r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=1.05;r.setClearColor(0x000000,0);
// el mismo estudio de luz que el hero
const s=new THREE.Scene();s.background=new THREE.Color(0);
const pan=(w,h,x,y,z,k)=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({color:new THREE.Color(k,k,k),side:THREE.DoubleSide}));m.position.set(x,y,z);m.lookAt(0,0,0);s.add(m);};
pan(7,7,0,7,1,1.1);pan(14,6,0,3,9,.55);pan(6,10,-7,1,-2,.35);pan(6,10,7,1,-2,.3);pan(1.1,9,-6,1,1.5,2.2);pan(.5,9,6,.5,2.5,2.6);pan(12,4,0,2.4,7,1.05);pan(3,7,-5,0,5,.5);pan(9,1.2,0,-2.5,7,.35);pan(9,.35,0,2.2,-6,2);pan(.35,6,3.5,1,-5,1.6);pan(2.5,.25,-2,4.2,4,2);
const pm=new THREE.PMREMGenerator(r);const env=pm.fromScene(s,0).texture;
const scene=new THREE.Scene();scene.environment=env;
const P=(x,y)=>[(x-100)/152,(96-y)/152];
const LT=[[24,20],[60,20],[96.2,172]],RT=[[176,20],[140,20],[103.8,172]];
const shape=pts=>{const sh=new THREE.Shape();pts.forEach((p,i)=>{const [x,y]=P(p[0],p[1]);i?sh.lineTo(x,y):sh.moveTo(x,y);});sh.closePath();return sh;};
const DEP=.2,EX={depth:DEP,bevelEnabled:true,bevelThickness:.012,bevelSize:.012,bevelSegments:6,curveSegments:1};
const mat=new THREE.MeshPhysicalMaterial({color:new THREE.Color().setRGB(.80,.79,.76,THREE.SRGBColorSpace),metalness:1,roughness:.2,clearcoat:.5,clearcoatRoughness:.1,envMapIntensity:1.35});
const g=new THREE.Group();[LT,RT].forEach(T=>{const ge=new THREE.ExtrudeGeometry(shape(T),EX);ge.translate(0,0,-DEP/2);ge.computeVertexNormals();g.add(new THREE.Mesh(ge,mat));});scene.add(g);
const key=new THREE.DirectionalLight(0xffffff,.7);key.position.set(-3,3,3);scene.add(key);
const cam=new THREE.PerspectiveCamera(30,1,.02,100);
window.shot=(yaw,pit)=>{const R=3.2;cam.position.set(Math.sin(yaw)*Math.cos(pit)*R,Math.sin(pit)*R,Math.cos(yaw)*Math.cos(pit)*R);cam.lookAt(0,0,0);r.render(scene,cam);return cv.toDataURL('image/png');};
// el nombre en titanio: los trazados del logotipo, extruidos con el mismo material
const WMD=['M0 0H15V43H63V0H78V100H63V57H15V100H0Z','M102 100L146 -3L190 100H173.6L146 37.3L118.4 100Z','M214 0H229V85H276V100H214Z','M268 0H284.4L312 62.7L339.6 0H356L312 103Z','M378 0H440V15H393V42.5H434V57.5H393V85H440V100H378Z','M464 0H482L508 37.14L534 0H552L517 50L552 100H534L508 62.86L482 100H464L499 50Z'];
const toShape=d=>{const t=d.match(/[MHVLZ]|-?[0-9.]+/g);const sh=new THREE.Shape();let x=0,y=0,c='',i=0,first=true;const pt=()=>{const X=(x-276)/100,Y=(50-y)/100;if(first){sh.moveTo(X,Y);first=false;}else sh.lineTo(X,Y);};
  while(i<t.length){const k=t[i];if(/[MHVLZ]/.test(k)){c=k;i++;if(c==='Z'){sh.closePath();}continue;}
    if(c==='M'||c==='L'){x=+t[i];y=+t[i+1];i+=2;}else if(c==='H'){x=+t[i];i++;}else if(c==='V'){y=+t[i];i++;}pt();}
  return sh;};
const WD=.1,WEX={depth:WD,bevelEnabled:true,bevelThickness:.012,bevelSize:.008,bevelSegments:6,curveSegments:1};
const wg=new THREE.Group();WMD.forEach(d=>{const ge=new THREE.ExtrudeGeometry(toShape(d),WEX);ge.translate(0,0,-WD/2);ge.computeVertexNormals();wg.add(new THREE.Mesh(ge,mat));});
const ws=new THREE.Scene();ws.environment=env;ws.add(wg);const k2=key.clone();ws.add(k2);
window.shotName=()=>{r.setSize(${S},${S/4},false);const c2=new THREE.PerspectiveCamera(11,4,.02,100);const yaw=0,pit=.025,R=8.2;c2.position.set(Math.sin(yaw)*Math.cos(pit)*R,Math.sin(pit)*R,Math.cos(yaw)*Math.cos(pit)*R);c2.lookAt(0,0,0);r.render(ws,c2);return cv.toDataURL('image/png');};
window.ready=true;
</script></body></html>`;
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const p=await b.newPage({viewport:{width:800,height:800}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.setContent(html);await p.waitForFunction(()=>window.ready,null,{timeout:120000});
  const fs=require('fs');
  {const d=await p.evaluate(()=>window.shotName());fs.writeFileSync(`${OUT}/nombre-titanio-raw.png`,Buffer.from(d.split(',')[1],'base64'));}
  for(const [n,yaw,pit] of [['frontal',-.06,.03],['tres-cuartos',.32,.1]]){const d=await p.evaluate(([y,q])=>window.shot(y,q),[yaw,pit]);fs.writeFileSync(`${OUT}/iso-${n}-raw.png`,Buffer.from(d.split(',')[1],'base64'));}
  // el nombre, desde los trazados del logotipo
  const WM='<path d="M0 0H15V43H63V0H78V100H63V57H15V100H0Z"/><path d="M102 100L146 -3L190 100H173.6L146 37.3L118.4 100Z"/><path d="M214 0H229V85H276V100H214Z"/><path d="M268 0H284.4L312 62.7L339.6 0H356L312 103Z"/><path d="M378 0H440V15H393V42.5H434V57.5H393V85H440V100H378Z"/><path d="M464 0H482L508 37.14L534 0H552L517 50L552 100H534L508 62.86L482 100H464L499 50Z"/>';
  for(const [n,col] of [['blanco','#ffffff'],['negro','#000000']]){
    await p.setViewportSize({width:2760,height:540});
    await p.setContent(`<body style="margin:0;background:transparent"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -4 552 108" width="2760" height="540" fill="${col}" style="display:block">${WM}</svg></body>`);
    await p.screenshot({path:`${OUT}/nombre-${n}-raw.png`,omitBackground:true});}
  console.log(errs.join('\n')||'ok');await b.close();})();
