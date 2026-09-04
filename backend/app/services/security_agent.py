from app.services.featherless import FeatherlessService


SECURITY_SYSTEM_PROMPT = """
You are ShadowCode, an autonomous DevSecOps security agent.

Your job is to analyze source code for security vulnerabilities.

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

For every vulnerability you identify:
1. Name the vulnerability.
2. Explain why it is dangerous.
3. Identify the relevant code.
4. Explain how an attacker could potentially abuse it.
5. Provide a secure remediation.

Do not invent vulnerabilities.
Only report issues supported by the supplied code.

Be precise and security-focused.
"""


class SecurityAgent:
    def __init__(self):
        self.llm = FeatherlessService()

    async def analyze_code(self, code: str) -> str:
        prompt = f"""
Analyze the following source code for security vulnerabilities.

SOURCE CODE:
----------------
{code}
----------------

Return a clear security analysis.
"""

        return await self.llm.chat(
            prompt,
            system_prompt=SECURITY_SYSTEM_PROMPT,
        )