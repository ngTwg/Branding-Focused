---
name: "microservices-patterns"
tags: ["antigravity", "c:", "frontend", "gemini", "instructions", "<YOUR_USERNAME>", "microservices", "not", "patterns", "resources", "skill", "specialized", "this", "use", "users", "when"]
tier: 3
risk: "medium"
estimated_tokens: 343
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.60
date_added: "2026-02-27"
description: "Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems."
source: "community"
---
# Microservices Patterns

Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems.

## Use this skill when

- Decomposing monoliths into microservices
- Designing service boundaries and contracts
- Implementing inter-service communication
- Managing distributed data and transactions
- Building resilient distributed systems
- Implementing service discovery and load balancing
- Designing event-driven architectures

## Do not use this skill when

- The system is small enough for a modular monolith
- You need a quick prototype without distributed complexity
- There is no operational support for distributed systems

## Instructions

1. Identify domain boundaries and ownership for each service.
2. Define contracts, data ownership, and communication patterns.
3. Plan resilience, observability, and deployment strategy.
4. Provide migration steps and operational guardrails.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

## Runnable Patterns (Wave 3)

### 1) SAGA orchestration with compensation (Node.js)

```typescript
type SagaStep = {
	name: string;
	execute: () => Promise<void>;
	compensate: () => Promise<void>;
};

export async function runSaga(steps: SagaStep[]) {
	const completed: SagaStep[] = [];

	try {
		for (const step of steps) {
			await step.execute();
			completed.push(step);
		}
		return { ok: true };
	} catch (error) {
		for (const step of completed.reverse()) {
			await step.compensate().catch(() => undefined);
		}
		return { ok: false, error };
	}
}

// Example usage
await runSaga([
	{
		name: 'reserve-inventory',
		execute: () => inventory.reserve(orderId, items),
		compensate: () => inventory.release(orderId),
	},
	{
		name: 'charge-payment',
		execute: () => payments.charge(orderId, amount),
		compensate: () => payments.refund(orderId),
	},
	{
		name: 'create-shipment',
		execute: () => shipping.create(orderId),
		compensate: () => shipping.cancel(orderId),
	},
]);
```

### 2) CQRS command/query split (TypeScript)

```typescript
// Command model (write side)
export async function createOrder(cmd: {
	orderId: string;
	customerId: string;
	lines: Array<{ sku: string; qty: number; price: number }>;
}) {
	await events.append(cmd.orderId, {
		type: 'OrderCreated',
		payload: cmd,
		at: Date.now(),
	});
}

// Query model (read side projection)
type OrderView = {
	orderId: string;
	customerId: string;
	total: number;
	status: 'CREATED' | 'PAID' | 'SHIPPED';
};

export async function applyEventToProjection(event: any) {
	if (event.type === 'OrderCreated') {
		const total = event.payload.lines.reduce((sum: number, l: any) => sum + l.qty * l.price, 0);
		await readDb.upsertOrderView({
			orderId: event.payload.orderId,
			customerId: event.payload.customerId,
			total,
			status: 'CREATED',
		} satisfies OrderView);
	}
}
```

### 3) Event sourcing replay (Python)

```python
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class OrderState:
		order_id: str
		status: str = "CREATED"
		paid: bool = False

def evolve(state: OrderState, event: Dict[str, Any]) -> OrderState:
		t = event["type"]
		if t == "OrderPaid":
				state.paid = True
				state.status = "PAID"
		elif t == "OrderShipped":
				state.status = "SHIPPED"
		elif t == "OrderCancelled":
				state.status = "CANCELLED"
		return state

def replay(order_id: str, event_stream: List[Dict[str, Any]]) -> OrderState:
		state = OrderState(order_id=order_id)
		for event in event_stream:
				state = evolve(state, event)
		return state

# Example
final_state = replay("ord_123", [
		{"type": "OrderPaid"},
		{"type": "OrderShipped"},
])
print(final_state)
```

### 4) Contract compatibility guardrail

```yaml
rules:
	- name: no-breaking-removal
		check: response_schema_fields_removed == 0
	- name: additive-only-optional-fields
		check: new_fields_are_optional == true
	- name: versioned-path-for-breaking
		check: breaking_change_implies_new_api_version == true
```
