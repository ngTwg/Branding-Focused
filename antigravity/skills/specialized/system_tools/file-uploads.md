---
name: "File Uploads"
tags: ["antigravity", "best", "c:", "checklist", "file", "frontend", "gemini", "<YOUR_USERNAME>", "overview", "practices", "quick", "reference", "rules", "security", "specialized", "system", "tools", "uploads", "users", "validation"]
tier: 3
risk: "high"
estimated_tokens: 2817
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# File Uploads

> **Tier:** 2  
> **Tags:** `uploads`, `files`, `validation`, `security`, `storage`  
> **When to use:** Implementing file upload functionality with security and validation

---

## Overview

Secure file upload handling covering validation (type, size, content), storage strategies (local, S3, CDN), security best practices, and error handling. Essential for any application accepting user-uploaded files.

---

## Rules

**RULE-001: File Type Validation**
Validate file types using MIME type AND file extension AND magic bytes. Never trust client-provided MIME types. Use allowlist, not blocklist.

```typescript
❌ Bad: Trust client MIME type
if (file.mimetype === 'image/jpeg') {
  // Attacker can fake this
}

✅ Good: Multi-layer validation
import fileType from 'file-type';

async function validateFileType(buffer: Buffer, allowedTypes: string[]) {
  // Check magic bytes
  const type = await fileType.fromBuffer(buffer);
  if (!type || !allowedTypes.includes(type.mime)) {
    throw new Error('Invalid file type');
  }
  return type;
}

// Usage
const allowedImages = ['image/jpeg', 'image/png', 'image/webp'];
await validateFileType(fileBuffer, allowedImages);
```

**RULE-002: File Size Limits**
Enforce size limits at multiple layers: client-side (UX), server middleware (early rejection), and application logic (final check). Use streaming for large files.

```typescript
❌ Bad: Load entire file into memory
app.post('/upload', (req, res) => {
  const file = req.body.file; // Entire file in memory
  if (file.size > 10_000_000) {
    return res.status(413).send('File too large');
  }
});

✅ Good: Streaming with size limit
import multer from 'multer';

const upload = multer({
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
    files: 5 // Max 5 files
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png'];
    if (!allowedTypes.includes(file.mimetype)) {
      cb(new Error('Invalid file type'));
    } else {
      cb(null, true);
    }
  }
});

app.post('/upload', upload.array('files'), (req, res) => {
  // Files validated and size-limited
});
```

**RULE-003: Filename Sanitization**
Never use user-provided filenames directly. Generate unique filenames. Remove path traversal attempts. Sanitize for filesystem compatibility.

```typescript
❌ Bad: Use original filename
const filename = req.file.originalname; // Could be "../../etc/passwd"
fs.writeFileSync(`uploads/${filename}`, data);

✅ Good: Generate safe filename
import { randomUUID } from 'crypto';
import path from 'path';
import sanitize from 'sanitize-filename';

function generateSafeFilename(originalName: string): string {
  const ext = path.extname(originalName);
  const sanitizedExt = sanitize(ext).toLowerCase();
  const uuid = randomUUID();
  return `${uuid}${sanitizedExt}`;
}

// Usage
const safeFilename = generateSafeFilename(req.file.originalname);
// Result: "a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg"
```

**RULE-004: Content Scanning**
Scan uploaded files for malware and malicious content. Use antivirus APIs or services. Quarantine suspicious files.

```typescript
❌ Bad: No content scanning
fs.writeFileSync(`uploads/${filename}`, fileBuffer);

✅ Good: Scan before storing
import ClamScan from 'clamscan';

const clamscan = await new ClamScan().init({
  clamdscan: {
    host: 'localhost',
    port: 3310
  }
});

async function scanAndStore(fileBuffer: Buffer, filename: string) {
  // Scan for viruses
  const { isInfected, viruses } = await clamscan.scanBuffer(fileBuffer);
  
  if (isInfected) {
    console.error(`Malware detected: ${viruses.join(', ')}`);
    throw new Error('File contains malware');
  }
  
  // Safe to store
  await fs.promises.writeFile(`uploads/${filename}`, fileBuffer);
}
```

**RULE-005: Storage Strategy**
Choose appropriate storage: local (development), S3 (production), CDN (public assets). Use signed URLs for private files. Implement lifecycle policies.

```typescript
❌ Bad: Store everything locally
fs.writeFileSync(`public/uploads/${filename}`, data);
// No scalability, no redundancy

✅ Good: Cloud storage with signed URLs
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3 = new S3Client({ region: 'us-east-1' });

async function uploadToS3(fileBuffer: Buffer, filename: string, isPublic: boolean) {
  const key = `uploads/${Date.now()}-${filename}`;
  
  await s3.send(new PutObjectCommand({
    Bucket: 'my-bucket',
    Key: key,
    Body: fileBuffer,
    ContentType: 'image/jpeg',
    ACL: isPublic ? 'public-read' : 'private',
    ServerSideEncryption: 'AES256'
  }));
  
  if (isPublic) {
    return `https://my-bucket.s3.amazonaws.com/${key}`;
  } else {
    // Generate signed URL (expires in 1 hour)
    const command = new GetObjectCommand({ Bucket: 'my-bucket', Key: key });
    return await getSignedUrl(s3, command, { expiresIn: 3600 });
  }
}
```

**RULE-006: Progress Tracking**
Provide upload progress feedback for large files. Use chunked uploads for files > 5MB. Implement resume capability.

```typescript
❌ Bad: No progress feedback
await uploadFile(largeFile); // User waits with no feedback

✅ Good: Chunked upload with progress
async function uploadWithProgress(
  file: File,
  onProgress: (percent: number) => void
) {
  const chunkSize = 5 * 1024 * 1024; // 5MB chunks
  const chunks = Math.ceil(file.size / chunkSize);
  
  for (let i = 0; i < chunks; i++) {
    const start = i * chunkSize;
    const end = Math.min(start + chunkSize, file.size);
    const chunk = file.slice(start, end);
    
    await uploadChunk(chunk, i, chunks);
    
    const progress = ((i + 1) / chunks) * 100;
    onProgress(progress);
  }
}

// Client-side usage
uploadWithProgress(file, (percent) => {
  console.log(`Upload progress: ${percent.toFixed(1)}%`);
});
```

**RULE-007: Error Handling**
Handle all upload failure scenarios: network errors, size exceeded, invalid type, storage full. Provide clear error messages. Clean up partial uploads.

```typescript
❌ Bad: Generic error handling
try {
  await uploadFile(file);
} catch (error) {
  res.status(500).send('Upload failed');
}

✅ Good: Specific error handling
async function handleUpload(file: Express.Multer.File) {
  const tempPath = file.path;
  
  try {
    // Validate
    if (file.size > MAX_SIZE) {
      throw new UploadError('FILE_TOO_LARGE', `Max size: ${MAX_SIZE} bytes`);
    }
    
    const fileType = await validateFileType(file.buffer, ALLOWED_TYPES);
    if (!fileType) {
      throw new UploadError('INVALID_TYPE', 'Only images allowed');
    }
    
    // Scan
    const scanResult = await scanFile(file.buffer);
    if (scanResult.isInfected) {
      throw new UploadError('MALWARE_DETECTED', 'File contains malware');
    }
    
    // Upload
    const url = await uploadToS3(file.buffer, file.originalname);
    return { success: true, url };
    
  } catch (error) {
    if (error instanceof UploadError) {
      return { success: false, error: error.code, message: error.message };
    }
    throw error;
  } finally {
    // Clean up temp file
    await fs.promises.unlink(tempPath).catch(() => {});
  }
}

class UploadError extends Error {
  constructor(public code: string, message: string) {
    super(message);
  }
}
```

**RULE-008: Metadata Storage**
Store file metadata in database: original filename, size, type, upload date, user ID. Enable search and audit. Track file lifecycle.

```typescript
❌ Bad: No metadata tracking
await uploadToS3(file);
// Lost: who uploaded, when, original name

✅ Good: Complete metadata tracking
interface FileMetadata {
  id: string;
  userId: string;
  originalName: string;
  storedName: string;
  mimeType: string;
  size: number;
  storageUrl: string;
  uploadedAt: Date;
  expiresAt?: Date;
  scanStatus: 'pending' | 'clean' | 'infected';
  downloadCount: number;
}

async function uploadWithMetadata(file: Express.Multer.File, userId: string) {
  const storedName = generateSafeFilename(file.originalname);
  const url = await uploadToS3(file.buffer, storedName);
  
  const metadata: FileMetadata = {
    id: randomUUID(),
    userId,
    originalName: file.originalname,
    storedName,
    mimeType: file.mimetype,
    size: file.size,
    storageUrl: url,
    uploadedAt: new Date(),
    expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
    scanStatus: 'clean',
    downloadCount: 0
  };
  
  await db.files.insert(metadata);
  return metadata;
}
```

---

## Quick Reference

### Validation Checklist

- [ ] File type validation (MIME + extension + magic bytes)
- [ ] File size limits enforced
- [ ] Filename sanitization
- [ ] Content scanning (malware)
- [ ] User authentication/authorization
- [ ] Rate limiting (prevent abuse)

### Security Best Practices

```typescript
// 1. Allowlist file types
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf'];

// 2. Size limits
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const MAX_FILES = 5;

// 3. Generate unique filenames
const filename = `${randomUUID()}${sanitize(path.extname(original))}`;

// 4. Store outside web root
const UPLOAD_DIR = '/var/uploads'; // Not /var/www/public

// 5. Serve with Content-Disposition
res.setHeader('Content-Disposition', 'attachment; filename="safe.jpg"');

// 6. Use signed URLs for private files
const signedUrl = await getSignedUrl(s3, command, { expiresIn: 3600 });
```

### Storage Options Comparison

| Storage | Use Case | Pros | Cons |
|---------|----------|------|------|
| Local FS | Development, small scale | Simple, fast | No redundancy, not scalable |
| S3 | Production, any scale | Scalable, durable, cheap | Network latency |
| CDN | Public assets, high traffic | Fast delivery, global | Public only, cost |
| Database | Small files, metadata | Transactional, simple | Size limits, expensive |

### Error Codes

```typescript
enum UploadErrorCode {
  FILE_TOO_LARGE = 'FILE_TOO_LARGE',
  INVALID_TYPE = 'INVALID_TYPE',
  MALWARE_DETECTED = 'MALWARE_DETECTED',
  STORAGE_FULL = 'STORAGE_FULL',
  NETWORK_ERROR = 'NETWORK_ERROR',
  UNAUTHORIZED = 'UNAUTHORIZED',
  RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED'
}
```

### Complete Upload Flow

```typescript
async function completeUploadFlow(req: Request, res: Response) {
  try {
    // 1. Authentication
    const user = await authenticate(req);
    if (!user) throw new UploadError('UNAUTHORIZED', 'Login required');
    
    // 2. Rate limiting
    await checkRateLimit(user.id);
    
    // 3. Validation
    const file = req.file;
    if (!file) throw new UploadError('NO_FILE', 'No file provided');
    
    await validateFile(file);
    
    // 4. Scanning
    await scanFile(file.buffer);
    
    // 5. Upload
    const url = await uploadToS3(file.buffer, generateSafeFilename(file.originalname));
    
    // 6. Metadata
    const metadata = await saveMetadata(file, user.id, url);
    
    // 7. Response
    res.json({ success: true, file: metadata });
    
  } catch (error) {
    handleUploadError(error, res);
  }
}
```

---

## Metadata

- **Related Skills:** [security-middleware-stack.md], [api-design.md], [error-handling-patterns.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
