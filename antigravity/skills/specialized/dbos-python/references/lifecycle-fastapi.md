---
name: "Integrate DBOS with FastAPI"
tags: ["fastapi, http, server, integration"]
tier: 2
risk: "medium"
estimated_tokens: 371
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.59
impact: "CRITICAL"
impactDescription: "Proper integration ensures workflows survive server restarts"
title: "Integrate DBOS with FastAPI"
---
## Integrate DBOS with FastAPI

When using DBOS with FastAPI, configure and launch DBOS inside the main function before starting uvicorn.

**Incorrect (configuration at module level):**

```python
from fastapi import FastAPI
from dbos import DBOS, DBOSConfig

app = FastAPI()

# Don't configure at module level!
config: DBOSConfig = {"name": "my-app"}
DBOS(config=config)

@app.get("/")
@DBOS.workflow()
def endpoint():
    return {"status": "ok"}

if __name__ == "__main__":
    DBOS.launch()
    uvicorn.run(app)
```

**Correct (configuration in main):**

```python
import os
from fastapi import FastAPI
from dbos import DBOS, DBOSConfig
import uvicorn

app = FastAPI()

@DBOS.step()
def process_data():
    return "processed"

@app.get("/")
@DBOS.workflow()
def endpoint():
    result = process_data()
    return {"result": result}

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

The workflow decorator can be combined with FastAPI route decorators. The FastAPI decorator should come first (outermost).

Reference: [DBOS with FastAPI](https://docs.dbos.dev/python/tutorials/workflow-tutorial)
