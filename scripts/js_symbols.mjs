// What a JavaScript file declares, uses and says in its comments, read by the TypeScript compiler's parser (not by
// word matching), for scripts/code_graph.py:   node scripts/js_symbols.mjs <typescript dir> < files.json > out.json
// files.json is [{"key": "...", "text": "...", "line0": 0}] (line0: where an HTML page's inline script starts).
// Writes, per key: {decls: [{name, kind, line, end}], uses: {name: [lines]}, comments: [{line, text}], error}.
import { createRequire } from 'module';
import { readFileSync } from 'fs';

const ts = createRequire(import.meta.url)(process.argv[2]);
const files = JSON.parse(readFileSync(0, 'utf8'));
const out = {};
for (const f of files) {
  const r = { decls: [], uses: Object.create(null), comments: [], error: null };   // no prototype: a name like `constructor` is a name
  out[f.key] = r;
  let src;
  try {
    src = ts.createSourceFile(f.key + '.js', f.text, ts.ScriptTarget.Latest, true, ts.ScriptKind.JS);
  } catch (e) { r.error = String(e); continue; }
  const line = (pos) => src.getLineAndCharacterOfPosition(pos).line + 1 + f.line0;
  const declNames = new Set();      // identifier nodes that are a declaration's own name, not a use of it
  const decl = (nameNode, kind, node) => {
    if (!nameNode || !ts.isIdentifier(nameNode)) return;
    declNames.add(nameNode);
    r.decls.push({ name: nameNode.text, kind, line: line(node.getStart(src)), end: line(node.end) });
  };
  const visit = (n) => {
    if (ts.isFunctionDeclaration(n)) decl(n.name, 'function', n);
    else if (ts.isClassDeclaration(n)) decl(n.name, 'class', n);
    else if (ts.isMethodDeclaration(n)) decl(n.name, 'method', n);
    else if (ts.isVariableDeclaration(n) && ts.isIdentifier(n.name)) {
      const i = n.initializer;
      const fn = i && (ts.isArrowFunction(i) || ts.isFunctionExpression(i));
      // functions held in a const, and constants at the top of the file (a nested `let` is a local, not a piece of code)
      if (fn) decl(n.name, 'function', n);
      else if (n.parent && n.parent.parent && ts.isVariableStatement(n.parent.parent) && ts.isSourceFile(n.parent.parent.parent)) decl(n.name, 'const', n);
    }
    if (ts.isIdentifier(n) && !declNames.has(n)) (r.uses[n.text] ||= []).push(line(n.getStart(src)));
    if ((ts.isStringLiteral(n) || ts.isNoSubstitutionTemplateLiteral(n)) && /^[A-Za-z_$][\w$]*$/.test(n.text)) (r.uses[n.text] ||= []).push(line(n.getStart(src)));
    ts.forEachChild(n, visit);
  };
  visit(src);
  // comments: the ones the parser attaches before and after each node, each read once
  const seen = new Set();
  const grab = (ranges) => (ranges || []).forEach((c) => {
    if (seen.has(c.pos)) return;
    seen.add(c.pos);
    r.comments.push({ line: line(c.pos), text: f.text.slice(c.pos, c.end) });
  });
  const each = (n) => { grab(ts.getLeadingCommentRanges(f.text, n.pos)); grab(ts.getTrailingCommentRanges(f.text, n.end)); ts.forEachChild(n, each); };
  each(src);
  grab(ts.getLeadingCommentRanges(f.text, src.endOfFileToken.pos));
}
process.stdout.write(JSON.stringify(out));
