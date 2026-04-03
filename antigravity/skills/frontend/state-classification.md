---
name: "STATE CLASSIFICATION - QUẢN LÝ STATE ĐÚNG CÁCH"
tags: ["antigravity", "c:", "classification", "component", "concept", "cách", "frontend", "gemini", "<YOUR_USERNAME>", "local", "overview", "quản", "state", "table", "type", "use", "users", "usestate", "đúng"]
tier: 2
risk: "medium"
estimated_tokens: 4242
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# STATE CLASSIFICATION - QUẢN LÝ STATE ĐÚNG CÁCH

> **Tier:** 2-3  
> **Tags:** `[state-management, react, zustand, tanstack-query, url-state]`  
> **Khi nào dùng:** Mọi React application, đặc biệt khi state phức tạp hoặc nhiều components chia sẻ state

---

## 📋 OVERVIEW

**State hell** xảy ra khi:
- Prop drilling 5+ levels
- State không sync giữa components
- Re-render không cần thiết
- Cache data không đúng cách
- URL không reflect app state

**Thống kê:**
- 60% React bugs liên quan đến state management (React Survey 2023)
- Average app có 7 loại state khác nhau

---

## 🎯 STATE CLASSIFICATION TABLE

| State Type | Storage | Sync | Persist | Example | Tool |
|------------|---------|------|---------|---------|------|
| **UI State** | Component | No | No | Modal open, tab index | `useState` |
| **Form State** | Component | No | Maybe | Input values, validation | React Hook Form |
| **Server State** | Memory + Server | Yes | Cache | User data, products | TanStack Query |
| **Global State** | Memory | Yes | Maybe | Auth, theme, language | Zustand, Context |
| **URL State** | URL | Yes | Yes | Filters, pagination, search | URLSearchParams |
| **Local Storage** | Browser | No | Yes | Preferences, cart | localStorage |
| **Session Storage** | Browser | No | Session | Temp data, wizard | sessionStorage |
| **Realtime State** | WebSocket | Yes | No | Chat, notifications | WebSocket + Zustand |

---

## 🎨 TYPE 1: UI STATE (Component-Local)

### Concept
State chỉ dùng trong 1 component, không cần share

### ✅ Use `useState`

```javascript
function Accordion() {
  // ⭐ UI State: Only this component cares
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Collapse' : 'Expand'}
      </button>
      {isOpen && <div>Content here</div>}
    </div>
  );
}
```

### ❌ Anti-Pattern: Global UI State

```javascript
// ❌ BAD: Modal state in global store
const useStore = create((set) => ({
  isModalOpen: false,
  openModal: () => set({ isModalOpen: true })
}));

function App() {
  const { isModalOpen, openModal } = useStore();
  return <button onClick={openModal}>Open</button>;
}

// ✅ GOOD: Local state
function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  return <button onClick={() => setIsModalOpen(true)}>Open</button>;
}
```

### When to Use
- ✅ Modal open/close
- ✅ Dropdown open/close
- ✅ Tab selection
- ✅ Hover state
- ✅ Focus state
- ❌ NOT for: Data from API, shared state

---

## 📝 TYPE 2: FORM STATE

### Concept
Form inputs, validation, submission state

### ✅ Use React Hook Form

```javascript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema validation
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
  age: z.number().min(18, 'Must be 18+')
});

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues: {
      email: '',
      password: '',
      age: 18
    }
  });
  
  const onSubmit = async (data) => {
    await fetch('/api/signup', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      
      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}
      
      <input type="number" {...register('age', { valueAsNumber: true })} />
      {errors.age && <span>{errors.age.message}</span>}
      
      <button disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

### ❌ Anti-Pattern: Manual Form State

```javascript
// ❌ BAD: Manual state for each field
function SignupForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [age, setAge] = useState(18);
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [ageError, setAgeError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  // 100+ lines of validation logic...
}

// ✅ GOOD: Use React Hook Form (see above)
```

### When to Use
- ✅ Forms with validation
- ✅ Multi-step wizards
- ✅ Dynamic fields
- ✅ File uploads
- ❌ NOT for: Simple 1-2 field forms (use useState)

---

## 🌐 TYPE 3: SERVER STATE (API Data)

### Concept
Data from server, needs caching, refetching, optimistic updates

### ✅ Use TanStack Query

```javascript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetch user
function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(res => res.json()),
    staleTime: 5 * 60 * 1000,  // Cache 5 minutes
    cacheTime: 10 * 60 * 1000  // Keep in memory 10 minutes
  });
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{data.name}</div>;
}

// Update user (optimistic update)
function EditProfile({ userId }) {
  const queryClient = useQueryClient();
  
  const mutation = useMutation({
    mutationFn: (newData) => 
      fetch(`/api/users/${userId}`, {
        method: 'PATCH',
        body: JSON.stringify(newData)
      }),
    
    // ⭐ Optimistic update
    onMutate: async (newData) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries(['user', userId]);
      
      // Snapshot previous value
      const previous = queryClient.getQueryData(['user', userId]);
      
      // Optimistically update
      queryClient.setQueryData(['user', userId], (old) => ({
        ...old,
        ...newData
      }));
      
      return { previous };
    },
    
    // Rollback on error
    onError: (err, newData, context) => {
      queryClient.setQueryData(['user', userId], context.previous);
    },
    
    // Refetch on success
    onSettled: () => {
      queryClient.invalidateQueries(['user', userId]);
    }
  });
  
  return (
    <button onClick={() => mutation.mutate({ name: 'New Name' })}>
      Update
    </button>
  );
}
```

### ❌ Anti-Pattern: Manual Fetch State

```javascript
// ❌ BAD: Manual fetch + useState
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [userId]);
  
  // No caching, no refetch, no optimistic updates
}

// ✅ GOOD: Use TanStack Query (see above)
```

### When to Use
- ✅ API data (users, products, posts)
- ✅ Paginated lists
- ✅ Infinite scroll
- ✅ Real-time data (with refetchInterval)
- ✅ Optimistic updates
- ❌ NOT for: Static data, UI state

---

## 🌍 TYPE 4: GLOBAL STATE

### Concept
State shared across many components (auth, theme, language)

### ✅ Use Zustand

```javascript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Create store
const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      
      login: async (email, password) => {
        const res = await fetch('/api/login', {
          method: 'POST',
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        
        set({ user: data.user, token: data.token });
      },
      
      logout: () => {
        set({ user: null, token: null });
      },
      
      isAuthenticated: () => {
        return get().token !== null;
      }
    }),
    {
      name: 'auth-storage',  // localStorage key
      partialize: (state) => ({ token: state.token })  // Only persist token
    }
  )
);

// Use in components
function Header() {
  const { user, logout } = useAuthStore();
  
  return (
    <header>
      {user ? (
        <>
          <span>Welcome, {user.name}</span>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <a href="/login">Login</a>
      )}
    </header>
  );
}

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated());
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
}
```

### ❌ Anti-Pattern: Context for Everything

```javascript
// ❌ BAD: Context causes re-renders
const AuthContext = createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('en');
  
  // ⚠️ Every state change re-renders ALL consumers!
  
  return (
    <AuthContext.Provider value={{ user, setUser, theme, setTheme, language, setLanguage }}>
      {children}
    </AuthContext.Provider>
  );
}

// ✅ GOOD: Use Zustand (see above) or split contexts
```

### When to Use
- ✅ Authentication state
- ✅ Theme (dark/light)
- ✅ Language/i18n
- ✅ Shopping cart
- ✅ Notifications
- ❌ NOT for: Server data (use TanStack Query), UI state

---

## 🔗 TYPE 5: URL STATE

### Concept
State reflected in URL (filters, pagination, search)

### ✅ Use URLSearchParams

```javascript
import { useSearchParams } from 'react-router-dom';

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Read from URL
  const page = parseInt(searchParams.get('page') || '1');
  const search = searchParams.get('search') || '';
  const category = searchParams.get('category') || 'all';
  
  // Fetch with URL params
  const { data } = useQuery({
    queryKey: ['products', page, search, category],
    queryFn: () => 
      fetch(`/api/products?page=${page}&search=${search}&category=${category}`)
        .then(res => res.json())
  });
  
  // Update URL
  const handleSearch = (value) => {
    setSearchParams({
      page: '1',  // Reset to page 1
      search: value,
      category
    });
  };
  
  const handlePageChange = (newPage) => {
    setSearchParams({
      page: newPage.toString(),
      search,
      category
    });
  };
  
  return (
    <div>
      <input 
        value={search} 
        onChange={(e) => handleSearch(e.target.value)} 
      />
      
      <ProductGrid products={data?.products} />
      
      <Pagination 
        current={page} 
        onChange={handlePageChange} 
      />
    </div>
  );
}
```

### Benefits
- ✅ Shareable URLs (copy/paste link)
- ✅ Browser back/forward works
- ✅ Bookmark-able
- ✅ SEO-friendly

### When to Use
- ✅ Filters (category, price range)
- ✅ Pagination (page number)
- ✅ Search queries
- ✅ Sorting (sort by, order)
- ✅ Tab selection (in some cases)
- ❌ NOT for: Sensitive data (passwords), temporary UI state

---

## 📦 TYPE 6: LOCAL STORAGE STATE

### Concept
Persist state across sessions (preferences, cart)

### ✅ Use with Zustand Persist

```javascript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],
      
      addItem: (product) => {
        set((state) => ({
          items: [...state.items, { ...product, quantity: 1 }]
        }));
      },
      
      removeItem: (productId) => {
        set((state) => ({
          items: state.items.filter(item => item.id !== productId)
        }));
      },
      
      clearCart: () => set({ items: [] }),
      
      total: () => {
        return get().items.reduce((sum, item) => 
          sum + item.price * item.quantity, 0
        );
      }
    }),
    {
      name: 'cart-storage',  // localStorage key
      version: 1,  // Migration version
      migrate: (persistedState, version) => {
        // Handle schema changes
        if (version === 0) {
          return { items: [] };
        }
        return persistedState;
      }
    }
  )
);
```

### ⚠️ Security Warning

```javascript
// ❌ NEVER store sensitive data in localStorage
const badStore = create(
  persist(
    (set) => ({
      password: '',  // ❌ NEVER!
      creditCard: '',  // ❌ NEVER!
      ssn: ''  // ❌ NEVER!
    }),
    { name: 'bad-storage' }
  )
);

// ✅ ONLY store non-sensitive data
const goodStore = create(
  persist(
    (set) => ({
      theme: 'dark',  // ✓ OK
      language: 'en',  // ✓ OK
      cartItems: []  // ✓ OK (not sensitive)
    }),
    { name: 'good-storage' }
  )
);
```

### When to Use
- ✅ User preferences (theme, language)
- ✅ Shopping cart
- ✅ Draft content (auto-save)
- ✅ Recently viewed items
- ❌ NOT for: Passwords, tokens, credit cards

---

## 🔴 TYPE 7: REALTIME STATE (WebSocket)

### Concept
Live updates from server (chat, notifications)

### ✅ Combine WebSocket + Zustand

```javascript
import { create } from 'zustand';

const useChatStore = create((set, get) => ({
  messages: [],
  ws: null,
  connected: false,
  
  connect: (roomId) => {
    const ws = new WebSocket(`wss://api.com/chat/${roomId}`);
    
    ws.onopen = () => {
      set({ connected: true, ws });
    };
    
    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      set((state) => ({
        messages: [...state.messages, message]
      }));
    };
    
    ws.onclose = () => {
      set({ connected: false, ws: null });
    };
  },
  
  disconnect: () => {
    const { ws } = get();
    if (ws) {
      ws.close();
    }
  },
  
  sendMessage: (text) => {
    const { ws } = get();
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'message', text }));
    }
  }
}));

// Use in component
function ChatRoom({ roomId }) {
  const { messages, connected, connect, disconnect, sendMessage } = useChatStore();
  
  useEffect(() => {
    connect(roomId);
    return () => disconnect();
  }, [roomId]);
  
  return (
    <div>
      <div>Status: {connected ? 'Connected' : 'Disconnected'}</div>
      <MessageList messages={messages} />
      <MessageInput onSend={sendMessage} />
    </div>
  );
}
```

---

## 📊 DECISION TREE

```
START: What kind of state?

├─ Only used in 1 component?
│  └─ YES → useState (UI State)
│
├─ Form with validation?
│  └─ YES → React Hook Form (Form State)
│
├─ Data from API?
│  └─ YES → TanStack Query (Server State)
│
├─ Shared across many components?
│  ├─ Auth, theme, language? → Zustand (Global State)
│  └─ Filters, pagination? → URLSearchParams (URL State)
│
├─ Need to persist across sessions?
│  └─ YES → Zustand + persist (Local Storage)
│
└─ Real-time updates?
   └─ YES → WebSocket + Zustand (Realtime State)
```

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: Prop Drilling

```javascript
// ❌ BAD: Passing props 5 levels deep
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <Menu user={user}>
        <UserAvatar user={user} />
      </Menu>
    </Sidebar>
  </Layout>
</App>

// ✅ GOOD: Use global state
const useAuthStore = create((set) => ({
  user: null
}));

function UserAvatar() {
  const user = useAuthStore(state => state.user);
  return <img src={user.avatar} />;
}
```

### ❌ Mistake 2: Server State in useState

```javascript
// ❌ BAD: Manual caching
const [users, setUsers] = useState([]);

useEffect(() => {
  fetch('/api/users')
    .then(res => res.json())
    .then(setUsers);
}, []);

// ✅ GOOD: Use TanStack Query
const { data: users } = useQuery({
  queryKey: ['users'],
  queryFn: () => fetch('/api/users').then(res => res.json())
});
```

### ❌ Mistake 3: Not Using URL State

```javascript
// ❌ BAD: Filters in useState (not shareable)
const [category, setCategory] = useState('all');

// ✅ GOOD: Filters in URL (shareable)
const [searchParams, setSearchParams] = useSearchParams();
const category = searchParams.get('category') || 'all';
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Create e-commerce product list with:
- Search, filters, pagination in URL
- Product data from API with caching
- Shopping cart persisted in localStorage
- Dark mode toggle (global state)
- Use proper state management for each type"
```

### AI Should

1. ✅ Use URLSearchParams for filters/pagination
2. ✅ Use TanStack Query for product data
3. ✅ Use Zustand + persist for cart
4. ✅ Use Zustand for theme
5. ✅ NOT use useState for server data
6. ✅ NOT use Context for everything

---

## 🔗 RELATED SKILLS

- `resource-cleanup.md` - Cleanup WebSocket, subscriptions
- `concurrency-patterns.md` - Optimistic updates
- `frontend/react-patterns.md` - React best practices

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** Medium  
**Impact:** High (architecture decision)
