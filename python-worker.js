import { loadPyodide } from './vendor/pyodide/pyodide.mjs';
let outputLength=0;
function stream(type,text){outputLength+=text.length;if(outputLength>20000)throw new Error('Output limit reached (20,000 characters).');self.postMessage({type,text});}
let runtime;
try {
  runtime=await loadPyodide({indexURL:new URL('./vendor/pyodide/',import.meta.url).href,stdout:text=>stream('stdout',text),stderr:text=>stream('stderr',text),stdin:()=>null});
  self.postMessage({type:'ready'});
} catch(error) {self.postMessage({type:'error',error:String(error)});}
self.onmessage=async({data})=>{
  if(data.type!=='run'||!runtime)return;
  try {
    const globals=runtime.toPy({__name__:'__main__'});
    try {
      const result=await runtime.runPythonAsync(data.code,{globals});
      if(result&&typeof result.destroy==='function')result.destroy();
      self.postMessage({type:'done'});
    } finally {globals.destroy();}
  } catch(error) {self.postMessage({type:'error',error:String(error)});}
};
