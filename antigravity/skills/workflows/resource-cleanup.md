---
name: "RESOURCE CLEANUP - NGĂN CHẶN RÒ RỈ BỘ NHỚ"
tags: ["angular", "antigravity", "backend", "c:", "checklist", "chặn", "cleanup", "frontend", "gemini", "<YOUR_USERNAME>", "ngăn", "nhớ", "node", "overview", "pattern", "python", "react", "resource", "useeffect", "users"]
tier: 2
risk: "medium"
estimated_tokens: 3479
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# RESOURCE CLEANUP - NGĂN CHẶN RÒ RỈ BỘ NHỚ

> **Tier:** 2-3  
> **Tags:** `[memory-leak, cleanup, useEffect, connections, file-handles]`  
> **Khi nào dùng:** Mọi component/function sử dụng external resources (timers, subscriptions, connections, event listeners)

---

## 📋 OVERVIEW

**Memory leak** xảy ra khi resources không được giải phóng, dẫn đến:
- RAM tăng dần → Server crash
- File handles hết → Cannot open file
- Database connections hết → Connection pool exhausted
- Event listeners chồng chất → Performance degradation

**Thống kê:** 
- 40% production crashes do memory leaks (New Relic 2023)
- Average leak: 50MB/hour → crash sau 8 hours

---

## 🎯 RESOURCE CLEANUP CHECKLIST

### Frontend (React/Vue/Angular)

```markdown
[ ] useEffect cleanup (timers, subscriptions, listeners)
[ ] WebSocket connections closed
[ ] Event listeners removed
[ ] Intervals/timeouts cleared
[ ] AbortController for fetch requests
[ ] IntersectionObserver disconnected
[ ] ResizeObserver disconnected
[ ] MutationObserver disconnected
[ ] Canvas contexts released
[ ] IndexedDB connections closed
```

### Backend (Node.js/Python)

```markdown
[ ] Database connections closed
[ ] File handles closed (fs.close)
[ ] HTTP connections closed
[ ] Child processes killed
[ ] Streams destroyed
[ ] Redis connections quit
[ ] Message queue consumers closed
[ ] Temporary files deleted
[ ] Cron jobs stopped
[ ] Memory caches cleared
```

---

## ⚛️ PATTERN 1: REACT useEffect CLEANUP

### ❌ BAD: Memory Leak

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    // ❌ Fetch without cleanup
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data));  // ⚠️ Component unmounted → leak!
    
    // ❌ Timer without cleanup
    const timer = setInterval(() => {
      console.log('Polling...');
    }, 1000);  // ⚠️ Runs forever!
    
    // ❌ Event listener without cleanup
    window.addEventListener('resize', handleResize);  // ⚠️ Never removed!
    
  }, [userId]);
  
  return <div>{user?.name}</div>;
}
```

**Problem:** 
- Component unmounts → fetch still running → `setUser` on unmounted component
- Timer keeps running → memory leak
- Event listener accumulates → performance degradation

### ✅ GOOD: Proper Cleanup

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    let isMounted = true;  // ⭐ Track mount status
    const abortController = new AbortController();  // ⭐ Cancel fetch
    
    // Fetch with abort signal
    fetch(`/api/users/${userId}`, { 
      signal: abortController.signal 
    })
      .then(res => res.json())
      .then(data => {
        if (isMounted) {  // ⭐ Only update if mounted
          setUser(data);
        }
      })
      .catch(error => {
        if (error.name !== 'AbortError') {
          console.error(error);
        }
      });
    
    // Timer with cleanup
    const timer = setInterval(() => {
      console.log('Polling...');
    }, 1000);
    
    // Event listener with cleanup
    const handleResize = () => console.log('Resized');
    window.addEventListener('resize', handleResize);
    
    // ⭐ CLEANUP FUNCTION
    return () => {
      isMounted = false;  // Prevent state updates
      abortController.abort();  // Cancel fetch
      clearInterval(timer);  // Stop timer
      window.removeEventListener('resize', handleResize);  // Remove listener
    };
    
  }, [userId]);
  
  return <div>{user?.name}</div>;
}
```

---

## 🔌 PATTERN 2: WEBSOCKET CLEANUP

### ❌ BAD: Connection Leak

```javascript
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  
  useEffect(() => {
    const ws = new WebSocket(`wss://api.com/chat/${roomId}`);
    
    ws.onmessage = (event) => {
      setMessages(prev => [...prev, JSON.parse(event.data)]);
    };
    
    // ❌ No cleanup → connection stays open!
    
  }, [roomId]);
  
  return <MessageList messages={messages} />;
}
```

### ✅ GOOD: Close Connection

```javascript
function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  
  useEffect(() => {
    const ws = new WebSocket(`wss://api.com/chat/${roomId}`);
    let isMounted = true;
    
    ws.onopen = () => console.log('Connected');
    
    ws.onmessage = (event) => {
      if (isMounted) {
        setMessages(prev => [...prev, JSON.parse(event.data)]);
      }
    };
    
    ws.onerror = (error) => console.error('WebSocket error:', error);
    
    ws.onclose = () => console.log('Disconnected');
    
    // ⭐ CLEANUP
    return () => {
      isMounted = false;
      
      if (ws.readyState === WebSocket.OPEN) {
        ws.close(1000, 'Component unmounted');  // ⭐ Close gracefully
      }
    };
    
  }, [roomId]);
  
  return <MessageList messages={messages} />;
}
```

---

## 📡 PATTERN 3: SUBSCRIPTION CLEANUP

### ❌ BAD: Subscription Leak

```javascript
function StockTicker({ symbol }) {
  const [price, setPrice] = useState(0);
  
  useEffect(() => {
    // ❌ Subscribe without unsubscribe
    const subscription = stockService.subscribe(symbol, (newPrice) => {
      setPrice(newPrice);
    });
    
    // ❌ No cleanup!
    
  }, [symbol]);
  
  return <div>${price}</div>;
}
```

### ✅ GOOD: Unsubscribe

```javascript
function StockTicker({ symbol }) {
  const [price, setPrice] = useState(0);
  
  useEffect(() => {
    let isMounted = true;
    
    const subscription = stockService.subscribe(symbol, (newPrice) => {
      if (isMounted) {
        setPrice(newPrice);
      }
    });
    
    // ⭐ CLEANUP
    return () => {
      isMounted = false;
      subscription.unsubscribe();  // ⭐ Stop receiving updates
    };
    
  }, [symbol]);
  
  return <div>${price}</div>;
}
```

---

## 🗄️ PATTERN 4: DATABASE CONNECTION CLEANUP

### ❌ BAD: Connection Leak (Node.js)

```javascript
// ❌ BAD: Connection never closed
async function getUser(userId) {
  const connection = await mysql.createConnection({
    host: 'localhost',
    user: 'root',
    database: 'mydb'
  });
  
  const [rows] = await connection.query(
    'SELECT * FROM users WHERE id = ?',
    [userId]
  );
  
  return rows[0];  // ❌ Connection still open!
}

// After 100 requests → connection pool exhausted
```

### ✅ GOOD: Always Close

```javascript
// ✅ GOOD: Close in finally
async function getUser(userId) {
  let connection;
  
  try {
    connection = await mysql.createConnection({
      host: 'localhost',
      user: 'root',
      database: 'mydb'
    });
    
    const [rows] = await connection.query(
      'SELECT * FROM users WHERE id = ?',
      [userId]
    );
    
    return rows[0];
    
  } finally {
    if (connection) {
      await connection.end();  // ⭐ Always close
    }
  }
}
```

### ✅ BETTER: Use Connection Pool

```javascript
// Create pool once (app startup)
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  database: 'mydb',
  connectionLimit: 10,
  waitForConnections: true,
  queueLimit: 0
});

// Use pool (auto-release)
async function getUser(userId) {
  const connection = await pool.getConnection();
  
  try {
    const [rows] = await connection.query(
      'SELECT * FROM users WHERE id = ?',
      [userId]
    );
    return rows[0];
    
  } finally {
    connection.release();  // ⭐ Return to pool
  }
}

// Cleanup on app shutdown
process.on('SIGTERM', async () => {
  await pool.end();  // ⭐ Close all connections
  process.exit(0);
});
```

---

## 📁 PATTERN 5: FILE HANDLE CLEANUP

### ❌ BAD: File Handle Leak (Node.js)

```javascript
// ❌ BAD: File never closed
async function readConfig() {
  const fd = await fs.open('config.json', 'r');
  const buffer = Buffer.alloc(1024);
  
  await fd.read(buffer, 0, 1024, 0);
  
  return JSON.parse(buffer.toString());  // ❌ File still open!
}

// After 1000 calls → "Too many open files" error
```

### ✅ GOOD: Close File

```javascript
// ✅ GOOD: Close in finally
async function readConfig() {
  let fd;
  
  try {
    fd = await fs.open('config.json', 'r');
    const buffer = Buffer.alloc(1024);
    
    await fd.read(buffer, 0, 1024, 0);
    
    return JSON.parse(buffer.toString());
    
  } finally {
    if (fd) {
      await fd.close();  // ⭐ Always close
    }
  }
}
```

### ✅ BETTER: Use High-Level API

```javascript
// ✅ BEST: Auto-cleanup
async function readConfig() {
  const content = await fs.readFile('config.json', 'utf-8');
  return JSON.parse(content);  // ⭐ File auto-closed
}
```

---

## 🐍 PATTERN 6: PYTHON CONTEXT MANAGERS

### ❌ BAD: Resource Leak

```python
# ❌ BAD: File never closed
def read_config():
    file = open('config.json', 'r')
    content = file.read()
    return json.loads(content)  # ❌ File still open!
```

### ✅ GOOD: Use `with` Statement

```python
# ✅ GOOD: Auto-cleanup
def read_config():
    with open('config.json', 'r') as file:  # ⭐ Auto-close
        content = file.read()
        return json.loads(content)
    # File automatically closed here
```

### ✅ Custom Context Manager

```python
from contextlib import contextmanager
import psycopg2

@contextmanager
def get_db_connection():
    """Context manager for database connection"""
    conn = None
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='mydb',
            user='postgres'
        )
        yield conn  # ⭐ Provide connection
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()  # ⭐ Always close

# Usage
def get_user(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        return cursor.fetchone()
    # Connection auto-closed
```

---

## 🧪 MEMORY LEAK DETECTION

### Tool 1: Chrome DevTools (Frontend)

```javascript
// Take heap snapshot before/after
// 1. Open DevTools → Memory tab
// 2. Take snapshot
// 3. Perform action (mount/unmount component 10 times)
// 4. Take another snapshot
// 5. Compare → look for detached DOM nodes, event listeners

// Example: Detect listener leak
function LeakyComponent() {
  useEffect(() => {
    const handler = () => console.log('Click');
    document.addEventListener('click', handler);
    // ❌ No cleanup → leak!
  }, []);
  
  return <div>Leaky</div>;
}
```

### Tool 2: Node.js Heap Dump

```javascript
// Install: npm install heapdump
const heapdump = require('heapdump');

// Take snapshot
heapdump.writeSnapshot((err, filename) => {
  console.log('Heap dump written to', filename);
});

// Compare snapshots with Chrome DevTools
```

### Tool 3: Memory Profiling (Python)

```python
# Install: pip install memory_profiler
from memory_profiler import profile

@profile
def leaky_function():
    data = []
    for i in range(1000000):
        data.append(i)  # ⚠️ Never released
    # data still in memory after function returns

# Run: python -m memory_profiler script.py
```

---

## 📊 QUICK REFERENCE

| Resource | Cleanup Method | Example |
|----------|----------------|---------|
| **Timer** | `clearInterval/clearTimeout` | `clearInterval(timerId)` |
| **Event Listener** | `removeEventListener` | `window.removeEventListener('resize', handler)` |
| **WebSocket** | `ws.close()` | `ws.close(1000, 'Done')` |
| **Fetch** | `AbortController.abort()` | `controller.abort()` |
| **DB Connection** | `connection.close()` | `await conn.end()` |
| **File Handle** | `fd.close()` | `await fd.close()` |
| **Subscription** | `subscription.unsubscribe()` | `sub.unsubscribe()` |
| **Observer** | `observer.disconnect()` | `observer.disconnect()` |

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: Async Cleanup

```javascript
// ❌ BAD: Cleanup function cannot be async
useEffect(() => {
  return async () => {  // ❌ ERROR!
    await cleanup();
  };
}, []);

// ✅ GOOD: Call async inside sync cleanup
useEffect(() => {
  return () => {
    cleanup().catch(console.error);  // ⭐ Fire and forget
  };
}, []);
```

### ❌ Mistake 2: Conditional Cleanup

```javascript
// ❌ BAD: Cleanup not always called
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  
  if (condition) {
    return () => clearInterval(timer);  // ❌ Only cleans if condition true
  }
}, []);

// ✅ GOOD: Always cleanup
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  
  return () => {
    clearInterval(timer);  // ⭐ Always called
  };
}, []);
```

### ❌ Mistake 3: Forgetting Dependencies

```javascript
// ❌ BAD: Stale closure
function Timer({ delay }) {
  useEffect(() => {
    const timer = setInterval(() => {
      console.log(delay);  // ⚠️ Always logs initial delay
    }, 1000);
    
    return () => clearInterval(timer);
  }, []);  // ❌ Missing delay dependency

// ✅ GOOD: Include dependencies
function Timer({ delay }) {
  useEffect(() => {
    const timer = setInterval(() => {
      console.log(delay);  // ⭐ Logs current delay
    }, 1000);
    
    return () => clearInterval(timer);
  }, [delay]);  // ⭐ Re-run when delay changes
}
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Create React component that:
- Fetches user data on mount
- Polls every 5 seconds
- Listens to window resize
- Connects to WebSocket
- Include proper cleanup for ALL resources
- Handle component unmount during async operations"
```

### AI Should

1. ✅ Add cleanup function to useEffect
2. ✅ Use AbortController for fetch
3. ✅ Clear intervals/timeouts
4. ✅ Remove event listeners
5. ✅ Close WebSocket connections
6. ✅ Track mount status (isMounted flag)
7. ✅ Handle errors in cleanup

---

## 🔗 RELATED SKILLS

- `error-handling-patterns.md` - Handle cleanup errors
- `concurrency-patterns.md` - Cleanup in concurrent scenarios
- `frontend/react-patterns.md` - React-specific cleanup

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** Medium  
**Impact:** Critical (prevents crashes)
