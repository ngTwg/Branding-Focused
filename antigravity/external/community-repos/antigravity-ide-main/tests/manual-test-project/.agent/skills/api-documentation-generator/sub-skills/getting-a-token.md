# Getting a Token

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
\`\`\`json
{
  "email": "user@example.com",
  "password": "your-password"
}
\`\`\`

**Response:**
\`\`\`json
{
  "token": "<YOUR_TOKEN>",
  "expiresIn": 3600,
  "refreshToken": "refresh_token_here"
}
\`\`\`