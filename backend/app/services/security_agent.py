import json

from app.services.featherless import FeatherlessService


SECURITY_SYSTEM_PROMPT = """
You are ShadowCode, an autonomous DevSecOps security agent.

Your job is to analyze source code for real security vulnerabilities.

Focus on:
- Injection vulnerabilities
- Authentication and authorization issues
- Sensitive data exposure
- Cryptographic weaknesses
- Insecure configuration
- Path traversal
- Server-side request forgery
- Cross-site scripting
- Command injection
- Unsafe deserialization
- Dependency-related security risks
- Other realistic security weaknesses

IMPORTANT RULES:

1. Do not invent vulnerabilities.
2. Only report vulnerabilities supported by the supplied source code.
3. Be precise and security-focused.
4. Return ONLY valid JSON.
5. Do not use Markdown.
6. If there are no vulnerabilities, return an empty vulnerabilities array.

Use exactly this JSON structure:

{
  "vulnerabilities": [
    {
      "name": "SQL Injection",
      "severity": "HIGH",
      "description": "Explain the vulnerability.",
      "evidence": "Quote or describe the relevant code.",
      "impact": "Explain what an attacker could potentially do.",
      "remediation": "Explain how to fix it.",
      "confidence": "HIGH"
    }
  ]
}
"""


class SecurityAgent:

    def __init__(self):
        self.llm = FeatherlessService()

    async def analyze_code(self, code: str) -> dict:

        prompt = f"""
Analyze the following source code for security vulnerabilities.

SOURCE CODE:
----------------
{code}
----------------

Return ONLY valid JSON using the required structure.
"""

        response = await self.llm.chat(
            prompt,
            system_prompt=SECURITY_SYSTEM_PROMPT,
        )

        response = response.strip()

        # Handle the occasional ```json ... ``` response
        if response.startswith("```"):
            response = response.replace("```json", "", 1)
            response = response.replace("```", "", 1)
            response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            return {
                "vulnerabilities": [],
                "error": "LLM returned invalid JSON",
                "raw_response": response,
            }