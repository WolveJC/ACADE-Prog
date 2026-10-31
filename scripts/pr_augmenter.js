/**
 * @typedef {Object} GeminiPRResponse
 * @property {string} title
 * @property {string} body
 */

/**
 * Automatiza la generación del título Conventional Commit y descripción de un PR usando Gemini.
 * 
 * @param {Object} params
 * @param {import('@actions/github/lib/context').Context} params.context
 * @param {InstanceType<typeof import('@actions/github').GitHub>} params.github
 * @param {string} params.geminiApiKey
 */
async function run({ context, github, geminiApiKey }) {
  const { owner, repo } = context.repo;
  const pull_number = context.payload.pull_request?.number;

  if (!pull_number) {
    throw new Error('No se encontró el número del Pull Request en el contexto.');
  }

  console.log(`[AI Augmenter] Analizando PR #${pull_number} para ${owner}/${repo}...`);

  // 1. Obtener la lista de archivos modificados usando el cliente Octokit de github-script
  const filesResponse = await github.rest.pulls.listFiles({
    owner,
    repo,
    pull_number,
  });

  /** @type {string} */
  const changedFiles = filesResponse.data.map(f => f.filename).join('\n');
  /** @type {string} */
  const originalBody = context.payload.pull_request?.body || '';

  // 2. Construir el Prompt Estricto
  const prompt = `
  You are an expert technical assistant for a multi-language academic repository (ACADE-Prog).
  Analyze the following changed files and original description to generate a Conventional Commit title and a structured Markdown description.

  Allowed types: feat, fix, docs, refactor, ci, test
  Allowed scopes: cpp, python, flask, react, web-backend, scripts, ci, styles, docs
  Constraints:
  - Title format: type(scope): short description (max 75 chars, lowercase imperative mood).
  - Description: Clean Markdown explaining changes and academic/business impact.

  Changed files:
  ${changedFiles}

  Original Description:
  ${originalBody}

  Response MUST be strictly valid JSON matching this structure:
  {
    "title": "string",
    "body": "string"
  }
  `;

  // 3. Llamada a la API de Gemini
  const modelName = 'gemini-2.5-flash';
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${geminiApiKey}`;

  const apiResponse = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { responseMimeType: 'application/json' }
    })
  });

  if (!apiResponse.ok) {
    throw new Error(`Gemini API falló con estado ${apiResponse.status}: ${apiResponse.statusText}`);
  }

  const data = await apiResponse.json();
  const rawText = data.candidates[0].content.parts[0].text;
  
  /** @type {GeminiPRResponse} */
  const result = JSON.parse(rawText);

  console.log(`[AI Augmenter] Título generado: "${result.title}"`);

  // 4. Actualización del PR en GitHub
  await github.rest.pulls.update({
    owner,
    repo,
    pull_number,
    title: result.title,
    body: result.body,
  });

  console.log(`[AI Augmenter] PR #${pull_number} actualizado exitosamente.`);
}

module.exports = { run };
