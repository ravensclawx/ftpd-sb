const fs=require('node:fs/promises'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict'),{execFileSync}=require('node:child_process');
(async()=>{const root=path.resolve(process.env.HBLAUNCHER_ROOT||process.argv[2]||''),dir=await fs.mkdtemp(path.join(os.tmpdir(),'ftpd-check-')),base=0x7f0000;
for(const [name,buttons,status,sequence,ack,previous,action,exit]of [['start',1,0,0,0,0,1,0],['stop',1,1,0,0,0,2,0],['busy',1,1,2,1,0,0,0],['held',1,0,0,0,1,0,0],['back',2,1,0,0,0,0,1]]){
 const state=Buffer.alloc(8*1024*1024);state.writeUInt32LE(previous,84);state.writeUInt32LE(0x46545031,base+8192);state.writeUInt32LE(status,base+8196);state.writeUInt32LE(sequence,base+8448);state.writeUInt32LE(ack,base+8236);const input=Buffer.alloc(64);input.writeUInt32LE(buttons,8);input.writeUInt32LE(1,32);await fs.writeFile(path.join(dir,'state'),state);await fs.writeFile(path.join(dir,'input'),input);
 execFileSync(path.join(root,'homebrew-launcher/game-compute-check'),[path.join(dir,'state'),path.join(dir,'out'),path.join(__dirname,'app.comp.spv'),path.join(dir,'input'),'1'],{env:{...process.env,HB_FULL_OUTPUT:'1'},stdio:'pipe'});
 const out=await fs.readFile(path.join(dir,'out'));assert.equal(out.readUInt32LE(base+8452),action,name);assert.equal(out.readUInt32LE(1016),exit,name);
}
await require(path.join(root,'homebrew-launcher/app-catalog.cjs')).readApp(__dirname);console.log('ftpd-sb: package validation and start/stop/busy/held/exit GPU checks passed.');})().catch(e=>{console.error(e.message);process.exitCode=1;});
