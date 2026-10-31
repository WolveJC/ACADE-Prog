/**
 * @typedef {Object} GeminiPRResponse
 * @property {string} title
 * @property {string} body
 */

/**
 * Modelo de Gemini usado por el script.
 * Si Google lo retira, solo hay que cambiar esta línea.
 * Estado de modelos: https://ai.google.dev/gemini-api/docs/deprecations
 * @type {string}
 */
const MODEL_NAME = 'gemini-3.1-flash-lite';

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
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${geminiApiKey}`;

  const apiResponse = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { responseMimeType: 'application/json' }
    })
  });

  if (!apiResponse.ok) {
    /** @type {string} */
    const errorBody = await apiResponse.text();
    throw new Error(
      `Gemini API falló (${apiResponse.status}) con modelo "${MODEL_NAME}": ${errorBody}`
    );
  }

  const data = await apiResponse.json();
  /** @type {string | undefined} */
  const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text;

  if (!rawText) {
    throw new Error(
      `Gemini no devolvió texto (modelo "${MODEL_NAME}"). Respuesta: ${JSON.stringify(data)}`
    );
  }

  /** @type {GeminiPRResponse} */
  let result;
  try {
    result = JSON.parse(rawText);
  } catch (error) {
    throw new Error(`Gemini devolvió un JSON inválido (modelo "${MODEL_NAME}"): ${rawText}`);
  }

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
