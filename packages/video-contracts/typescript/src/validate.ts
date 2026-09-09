import Ajv2020, {type ErrorObject, type ValidateFunction} from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {semanticDigest, DIGEST_FIELDS} from './canonical.js';

type JsonObject = Record<string, unknown>;
export type ContractValidationError = {code: string; message: string; path: string};

const here = path.dirname(fileURLToPath(import.meta.url));
const packageRoot = path.resolve(here, '../..');
const schemaDir = path.join(packageRoot, 'schemas');
const catalog = JSON.parse(fs.readFileSync(path.join(packageRoot, 'schema-catalog.json'), 'utf8')) as {
  schemas: Array<{schema_version: string; filename: string; digest_field: string | null}>;
};

const ajv = new Ajv2020({allErrors: true, strict: true});
addFormats(ajv);
for (const filename of fs.readdirSync(schemaDir).filter((name) => name.endsWith('.schema.json'))) {
  ajv.addSchema(JSON.parse(fs.readFileSync(path.join(schemaDir, filename), 'utf8')));
}

const validators = new Map<string, ValidateFunction>();
for (const row of catalog.schemas) {
  const schema = JSON.parse(fs.readFileSync(path.join(schemaDir, row.filename), 'utf8'));
  validators.set(row.schema_version, ajv.getSchema(schema.$id) ?? ajv.compile(schema));
}

export function validateContract(document: JsonObject, verifyDigest = true): ContractValidationError[] {
  const version = String(document.schema_version ?? '');
  const validator = validators.get(version);
  if (!validator) return [{code: 'SCHEMA_VERSION_UNSUPPORTED', message: `unsupported schema_version ${version}`, path: '$'}];
  if (!validator(document)) {
    return (validator.errors ?? []).map((error: ErrorObject) => ({code: 'JSON_SCHEMA', message: error.message ?? 'schema error', path: error.instancePath || '$'}));
  }
  if (verifyDigest) {
    const field = DIGEST_FIELDS[version];
    if (document[field] !== semanticDigest(document)) return [{code: 'DIGEST_MISMATCH', message: `${field} does not match canonical digest`, path: `$.${field}`}];
  }
  return [];
}
