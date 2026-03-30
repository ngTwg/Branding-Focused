# ANTI-HALLUCINATION PROTOCOL V2.0

> **Tier:** 1-4 (Critical for all tiers)  
> **Tags:** `[hallucination, verification, library, api, validation]`  
> **Khi nào dùng:** TRƯỚC KHI sử dụng bất kỳ thư viện, API, hoặc logic phức tạp nào

---

## 🎯 OVERVIEW

AI "hallucination" là hiện tượng AI tự tin sinh ra code với:
- Thư viện không tồn tại
- API signature sai
- Logic giải thích sai nhưng nghe thuyết phục
- Config options không có thật

**Tỷ lệ:** ~18.5% code Python và ~7% code TypeScript có hallucination nghiêm trọng.

**Mục tiêu:** Giảm hallucination xuống < 2% bằng 4-layer verification protocol.

---

## 🔴 VẤN ĐỀ THƯỜNG GẶP

### ❌ Hallucination Examples

#### 1. Library không tồn tại
```python
# AI sinh
from fastapi.security import AutoTokenVerifier  # KHÔNG TỒN TẠI
import pandas.ai_utils  # BỊA
from sklearn.advanced_preprocessing import SmartScaler  # KHÔNG CÓ
```

#### 2. API signature sai
```typescript
// AI sinh - params sai thứ tự
fs.writeFile(data, 'file.txt', 'utf8');  // WRONG

// Đúng
fs.writeFile('file.txt', data, 'utf8');
```

#### 3. Method không tồn tại trên version
```typescript
// AI sinh
const result = await prisma.user.createManyAndReturn({...});
// createManyAndReturn chỉ có từ Prisma 5.14.0+
```

---

## 📋 4-LAYER VERIFICATION PROTOCOL

### LAYER 1: LIBRARY/PACKAGE VERIFICATION

#### Protocol
```markdown
TRƯỚC KHI import/require bất kỳ package nào:
1. VERIFY package tồn tại
2. CHECK version compatibility
3. READ official documentation
4. TEST import trước khi viết code
```


#### Commands

**Node.js/npm:**
```bash
# Check if package exists
npm view react versions
npm view @tanstack/react-query versions

# Check specific version
npm view react@18.2.0

# Check what's installed
npm list react
npm list --depth=0  # Top-level only
```

**Python/pip:**
```bash
# Check if package exists
pip show pandas
pip index versions pandas

# Check installed version
pip list | grep pandas

# Search package
pip search fastapi  # (deprecated, use pypi.org)
```

**Verification Checklist:**
- [ ] Package name chính xác (không typo)
- [ ] Package tồn tại trên registry (npm, pypi)
- [ ] Version tương thích với project
- [ ] Package không deprecated
- [ ] Package có documentation chính thức

---

### LAYER 2: API SIGNATURE VERIFICATION

#### Protocol
```markdown
TRƯỚC KHI sử dụng function/method:
1. COPY exact signature từ official docs
2. VERIFY parameter order
3. CHECK return type
4. READ examples từ docs
5. NEVER rely on memory
```

#### Common Hallucinations

**Example 1: fs.writeFile**
```typescript
❌ AI hallucinate - params sai thứ tự
fs.writeFile(data, 'file.txt', 'utf8', callback);

✅ Đúng - check docs
fs.writeFile('file.txt', data, 'utf8', callback);
//           ^path      ^data  ^encoding
```

**Example 2: Array.prototype.includes**
```typescript
❌ AI hallucinate - không có param thứ 3
array.includes(value, fromIndex, caseSensitive);

✅ Đúng
array.includes(value, fromIndex);
// Chỉ có 2 params
```

**Example 3: Prisma methods**
```typescript
❌ AI hallucinate - method không tồn tại
await prisma.user.findManyAndCount();

✅ Đúng - phải dùng 2 queries riêng
const users = await prisma.user.findMany();
const count = await prisma.user.count();
```

#### Verification Checklist:
- [ ] Function/method tồn tại trong version đang dùng
- [ ] Parameter order đúng
- [ ] Parameter types đúng
- [ ] Return type đúng
- [ ] Optional vs required params đúng

---

### LAYER 3: LOGIC HALLUCINATION DETECTION

#### Protocol
```markdown
KHI AI giải thích logic phức tạp:
1. YÊU CẦU dry-run với input cụ thể
2. TRACE từng bước execution
3. VERIFY kết quả với expected output
4. KHÔNG tin explanation, chỉ tin execution
```

#### Example: Sorting Algorithm

**AI claim:**
```typescript
// AI: "This sorts array in O(n) time"
function quickSort(arr: number[]): number[] {
  if (arr.length <= 1) return arr;
  const pivot = arr[0];
  const left = arr.filter(x => x < pivot);
  const right = arr.filter(x => x > pivot);
  return [...quickSort(left), pivot, ...quickSort(right)];
}
```

**Verification:**
```markdown
Q: "Trace execution với input [3, 1, 4, 1, 5]"

AI trace:
1. pivot = 3
2. left = [1, 1], right = [4, 5]
3. Recurse on left: [1, 1]
4. Recurse on right: [4, 5]
...

RESULT: O(n log n) average, NOT O(n)
→ AI hallucinated về complexity
```

#### Verification Checklist:
- [ ] Dry-run với ít nhất 2 test cases
- [ ] Edge cases (empty, single element, duplicates)
- [ ] Complexity analysis đúng
- [ ] Logic explanation match với execution

---

### LAYER 4: CONFIGURATION HALLUCINATION

#### Protocol
```markdown
TRƯỚC KHI sử dụng config file:
1. VALIDATE config với schema/docs
2. CHECK options tồn tại
3. VERIFY default values
4. TEST config bằng CLI tool
```

#### Common Config Hallucinations

**Example 1: tsconfig.json**
```json
❌ AI hallucinate - options không tồn tại
{
  "compilerOptions": {
    "enableAutoImports": true,        // KHÔNG TỒN TẠI
    "strictFunctionTypes": "error",   // Sai type (phải boolean)
    "moduleResolution": "modern"      // Không có giá trị "modern"
  }
}

✅ Verify bằng command
npx tsc --showConfig
// Sẽ báo lỗi nếu options sai
```

**Example 2: ESLint config**
```json
❌ AI hallucinate
{
  "rules": {
    "no-console": "always",           // Sai value (phải "error"/"warn"/"off")
    "max-lines": 100,                 // Thiếu object wrapper
    "custom-rule": "error"            // Rule không tồn tại
  }
}

✅ Verify
npx eslint --print-config .
// Check output có lỗi không
```

**Example 3: Docker Compose**
```yaml
❌ AI hallucinate
version: '3.8'
services:
  app:
    image: node:18
    auto_restart: true              # KHÔNG TỒN TẠI (phải "restart")
    memory_limit: "512M"            # Sai format (phải "512m")
    depends_on:
      - db
      wait_for: healthy             # Sai syntax
```

#### Verification Commands:
```bash
# TypeScript
npx tsc --showConfig

# ESLint
npx eslint --print-config .

# Docker Compose
docker-compose config

# Prettier
npx prettier --check .prettierrc.json

# Package.json scripts
npm run <script> --dry-run
```

#### Verification Checklist:
- [ ] Config file syntax valid (JSON/YAML)
- [ ] All options tồn tại trong docs
- [ ] Value types đúng (string/number/boolean/array)
- [ ] Required fields đầy đủ
- [ ] Validate bằng CLI tool

---

## 🛠️ ANTI-HALLUCINATION TOOLS

### 1. Package Verification Script
```bash
#!/bin/bash
# verify-package.sh

PACKAGE=$1
MANAGER=${2:-npm}  # npm or pip

if [ "$MANAGER" = "npm" ]; then
  npm view "$PACKAGE" 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "❌ Package '$PACKAGE' KHÔNG TỒN TẠI trên npm"
    exit 1
  fi
  echo "✅ Package '$PACKAGE' tồn tại"
elif [ "$MANAGER" = "pip" ]; then
  pip show "$PACKAGE" 2>/dev/null
  if [ $? -ne 0 ]; then
    echo "❌ Package '$PACKAGE' KHÔNG TỒN TẠI hoặc chưa cài"
    exit 1
  fi
  echo "✅ Package '$PACKAGE' tồn tại"
fi
```

### 2. API Signature Checker (TypeScript)
```typescript
// check-api.ts
import * as fs from 'fs';

// Get function signature
const signature = fs.writeFile.toString();
console.log('fs.writeFile signature:', signature);

// Check parameter count
console.log('Parameter count:', fs.writeFile.length);

// Expected: 3 (path, data, callback) or 4 (path, data, options, callback)
```

### 3. Config Validator
```typescript
// validate-config.ts
import { z } from 'zod';

const tsconfigSchema = z.object({
  compilerOptions: z.object({
    target: z.enum(['ES5', 'ES6', 'ES2015', 'ES2016', 'ES2017', 'ES2018', 'ES2019', 'ES2020', 'ESNext']),
    module: z.enum(['commonjs', 'amd', 'umd', 'system', 'es6', 'es2015', 'esnext', 'none']),
    strict: z.boolean().optional(),
    // ... more options
  }),
});

// Validate
try {
  const config = JSON.parse(fs.readFileSync('tsconfig.json', 'utf8'));
  tsconfigSchema.parse(config);
  console.log('✅ tsconfig.json valid');
} catch (error) {
  console.error('❌ tsconfig.json invalid:', error);
}
```

---

## 📊 COMMON HALLUCINATIONS CATALOG

### Top 20 Hallucinations

#### JavaScript/TypeScript
1. `import { useQuery } from 'react'` → Đúng: `'@tanstack/react-query'`
2. `fs.readFileSync('file.txt', 'utf-8')` → Đúng: `'utf8'` (không có dấu gạch)
3. `axios.get(url, { params: { id } })` → Đúng (nhưng AI hay nhầm với `data`)
4. `Array.prototype.findLast()` → Chỉ có từ ES2023+
5. `Promise.allSettled()` → Chỉ có từ ES2020+
6. `String.prototype.replaceAll()` → Chỉ có từ ES2021+
7. `Object.hasOwn()` → Chỉ có từ ES2022+
8. `Array.prototype.at()` → Chỉ có từ ES2022+
9. `crypto.randomUUID()` → Chỉ có từ Node 15.6.0+
10. `fetch()` → Chỉ có từ Node 18+ (hoặc cần polyfill)

#### Python
11. `from fastapi.security import AutoTokenVerifier` → Không tồn tại
12. `import pandas.ai_utils` → Không tồn tại
13. `from sklearn.advanced_preprocessing import SmartScaler` → Không tồn tại
14. `df.to_excel(index=False, auto_width=True)` → `auto_width` không tồn tại
15. `requests.get(url, verify=False)` → Tắt SSL (BAD PRACTICE)
16. `json.loads(data, strict=False)` → `strict` deprecated từ Python 3.9
17. `dict.iteritems()` → Removed trong Python 3 (dùng `.items()`)
18. `print "hello"` → Python 2 syntax
19. `file.read().decode('utf-8')` → Không cần nếu mở file với encoding
20. `asyncio.run_until_complete()` → Deprecated, dùng `asyncio.run()`

---

## ✅ VERIFICATION CHECKLIST

### Before Using Any Library
- [ ] Package name verified (npm view / pip show)
- [ ] Version compatible với project
- [ ] Official documentation read
- [ ] Import tested successfully

### Before Using Any API
- [ ] Function/method exists in current version
- [ ] Parameter order verified from docs
- [ ] Parameter types correct
- [ ] Return type correct
- [ ] Example code from docs tested

### Before Trusting Logic Explanation
- [ ] Dry-run với concrete input
- [ ] Trace execution step-by-step
- [ ] Verify output matches expected
- [ ] Edge cases tested

### Before Using Config
- [ ] Config syntax valid
- [ ] All options exist in docs
- [ ] Value types correct
- [ ] Validated with CLI tool

---

## 🎯 AI LEVERAGE

### Verification Prompt Template
```markdown
Trước khi viết code, verify:

1. Package/Library:
   - Package name: [NAME]
   - Check: npm view [NAME] hoặc pip show [NAME]
   - Version: [VERSION]
   - Link docs: [URL]

2. API Signature:
   - Function: [FUNCTION_NAME]
   - Signature từ docs: [EXACT_SIGNATURE]
   - Parameters: [LIST_WITH_TYPES]
   - Return type: [TYPE]

3. Logic:
   - Input example: [EXAMPLE]
   - Expected output: [OUTPUT]
   - Trace execution: [STEP_BY_STEP]

4. Config:
   - File: [CONFIG_FILE]
   - Validate command: [COMMAND]
   - Schema: [SCHEMA_URL]

Chỉ proceed nếu TẤT CẢ verifications pass.
```

### Review Prompt
```markdown
Review code này cho hallucinations:

1. List tất cả imports/requires
2. Verify mỗi package tồn tại
3. Check API signatures với docs
4. Trace logic với example input
5. Validate config files

Report:
- ✅ Verified items
- ❌ Hallucinations found
- 🔧 Suggested fixes
```

---

## 🚨 EMERGENCY PROTOCOL

### Khi phát hiện hallucination:

1. **STOP immediately** - Không proceed với code
2. **VERIFY** - Check docs chính thức
3. **FIX** - Sửa code với info đúng
4. **TEST** - Chạy thử để confirm
5. **DOCUMENT** - Ghi lại hallucination để tránh lặp lại

### Red Flags (Dấu hiệu hallucination):
- 🚩 AI quá tự tin về API không phổ biến
- 🚩 Syntax trông "quá tiện" (too good to be true)
- 🚩 Method name nghe hợp lý nhưng chưa từng thấy
- 🚩 Config option "perfect" cho use case
- 🚩 AI không cung cấp link docs khi hỏi

---

## 📚 QUICK REFERENCE

| Layer | What to Verify | Tool |
|-------|----------------|------|
| 1. Library | Package exists, version | npm view, pip show |
| 2. API | Signature, params, return | Official docs, TypeScript |
| 3. Logic | Execution trace, output | Dry-run, debugger |
| 4. Config | Options exist, syntax | CLI validators |

---

## 🔗 RELATED SKILLS

- `workflows/debug-protocol.md` - Debugging hallucinated code
- `workflows/documentation-standards.md` - Documenting verified APIs
- `workflows/testing-strategies.md` - Testing for hallucinations
- `backend/api-design-standards.md` - API design to prevent confusion

---

**Version:** 2.0.0  
**Last Updated:** 2026-03-30  
**Status:** ✅ CRITICAL - Must verify before using any external code
