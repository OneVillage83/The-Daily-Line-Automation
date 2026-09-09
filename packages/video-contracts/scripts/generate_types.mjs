#!/usr/bin/env node
import {compileFromFile} from 'json-schema-to-typescript';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const catalog=JSON.parse(await fs.readFile(path.join(root,'schema-catalog.json'),'utf8'));
const out=path.join(root,'generated/typescript');
await fs.mkdir(out,{recursive:true});
for(const row of catalog.schemas){
 const ts=await compileFromFile(path.join(root,'schemas',row.filename),{bannerComment:'/* GENERATED from canonical JSON Schema. Do not edit by hand. */',cwd:path.join(root,'schemas')});
 await fs.writeFile(path.join(out,row.filename.replace('.schema.json','.d.ts')),ts,'utf8');
}
