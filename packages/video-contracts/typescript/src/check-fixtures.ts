import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateContract} from './validate.js';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../..');
let failures=0;
for(const name of fs.readdirSync(path.join(root,'fixtures/valid/end-to-end')).filter((x)=>x.endsWith('.json')).sort()){
  const doc=JSON.parse(fs.readFileSync(path.join(root,'fixtures/valid/end-to-end',name),'utf8')) as Record<string,unknown>;
  const errors=validateContract(doc);
  if(errors.length){console.error('FAIL',name,errors);failures++;}else console.log('PASS TypeScript schema fixture',name);
}
process.exitCode=failures?1:0;
