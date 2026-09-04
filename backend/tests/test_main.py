from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "online"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_analyze_endpoint(monkeypatch):
    from app.services.security_agent import SecurityAgent

    async def fake_analyze_code(self, code):
        return {
            "vulnerabilities": [
                {
                    "name": "SQL Injection",
                    "severity": "HIGH",
                    "description": "User input is directly used in a SQL query.",
                    "evidence": "query = 'SELECT * FROM users WHERE id=' + user_id",
                    "impact": "An attacker may execute arbitrary SQL queries.",
                    "remediation": "Use parameterized queries.",
                    "confidence": "HIGH",
                }
            ]
        }

    monkeypatch.setattr(
        SecurityAgent,
        "analyze_code",
        fake_analyze_code,
    )

    response = client.post(
        "/analyze",
        json={
            "code": "query = 'SELECT * FROM users WHERE id=' + user_id"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "vulnerabilities" in data
    assert len(data["vulnerabilities"]) == 1
    assert data["vulnerabilities"][0]["name"] == "SQL Injection"
    assert data["vulnerabilities"][0]["severity"] == "HIGH"


def test_repository_analysis(monkeypatch, tmp_path):
    from app.services.repository_service import RepositoryService
    from app.services.security_agent import SecurityAgent

    fake_repo = tmp_path / "fake_repo"
    fake_repo.mkdir()

    test_file = fake_repo / "test.py"
    test_file.write_text("print('hello')")

    def fake_clone_repository(self, repository_url):
        return fake_repo

    def fake_collect_source_files(self, repository_path):
        return [test_file]

    def fake_read_file_chunks(self, file_path):
        return [file_path.read_text()]

    async def fake_analyze_code(self, code):
        return {
            "vulnerabilities": [
                {
                    "name": "SQL Injection",
                    "severity": "HIGH",
                    "description": "Unsafe SQL query.",
                    "evidence": "user input used in query",
                    "impact": "Database compromise.",
                    "remediation": "Use parameterized queries.",
                    "confidence": "HIGH",
                }
            ]
        }

    def fake_cleanup(self, repository_path):
        pass

    monkeypatch.setattr(
        RepositoryService,
        "clone_repository",
        fake_clone_repository,
    )

    monkeypatch.setattr(
        RepositoryService,
        "collect_source_files",
        fake_collect_source_files,
    )

    monkeypatch.setattr(
        RepositoryService,
        "read_file_chunks",
        fake_read_file_chunks,
    )

    monkeypatch.setattr(
        RepositoryService,
        "cleanup",
        fake_cleanup,
    )

    monkeypatch.setattr(
        SecurityAgent,
        "analyze_code",
        fake_analyze_code,
    )

    response = client.post(
        "/analyze/repository",
        json={
            "repository_url": "https://github.com/example/test.git"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["files_analyzed"] == 1
    assert data["total_vulnerabilities"] == 1
    assert data["severity_summary"]["HIGH"] == 1
    assert len(data["vulnerabilities"]) == 1
    assert data["vulnerabilities"][0]["name"] == "SQL Injection"