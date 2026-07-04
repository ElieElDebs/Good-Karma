# Morlana Frontend

<p align="center">
   <img src="../images/transparent-logo.png" alt="Good Karma logo" width="140" />
</p>

<p align="center">
   <strong>Modern React frontend for Good Karma Reddit post analysis</strong>
</p>

<p align="center">
   <img src="https://img.shields.io/badge/react-19-blue.svg" alt="React 19" />
   <img src="https://img.shields.io/badge/next.js-16-black.svg" alt="Next.js 16" />
   <img src="https://img.shields.io/badge/typescript-5-blue.svg" alt="TypeScript 5" />
   <img src="https://img.shields.io/badge/tailwind-4-06B6D4.svg" alt="Tailwind CSS 4" />
   <img src="https://img.shields.io/badge/license-AGPL--3.0-blue.svg" alt="License: AGPL-3.0" />
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Development](#development)
- [Building & Deployment](#building--deployment)
- [Project Structure](#project-structure)
- [Components](#components)
- [Styling](#styling)
- [API Integration](#api-integration)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

**Morlana Frontend** is a modern, responsive web interface for the Good Karma Reddit post analysis platform. Built with **Next.js 16**, **React 19**, and **TypeScript**, it provides a seamless user experience for analyzing Reddit drafts and receiving actionable feedback.

The frontend handles:
- 📝 User input for Reddit draft (title, body, subreddit selection)
- 📊 Real-time visualization of KPIs and engagement scores
- 📈 Interactive charts and metrics (Recharts, custom visualizations)
- 💡 Display of AI-generated advice and recommendations
- 🔍 Similar posts comparison from the knowledge base
- ⚡ Responsive, mobile-friendly UI with Tailwind CSS

## Features

- ✨ **Modern UI** - Clean, intuitive interface built with React 19
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- 📊 **Rich Visualizations** - KPI charts, gauges, spider diagrams, and more
- ⚡ **Real-time Analysis** - Instant feedback as users type/submit drafts
- 🎨 **Tailwind CSS** - Utility-first styling with PostCSS and Tailwind 4
- 🔐 **Secure** - API key authentication with X-API-Key headers
- ♿ **Accessibility** - WCAG-compliant components (in progress)
- 🎯 **Type-Safe** - Full TypeScript throughout for better DX
- 📦 **Optimized** - Next.js optimizations for performance
- 🐳 **Docker Ready** - Multi-stage Dockerfile for production

## Architecture

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Framework** | Next.js | 16 | React framework with server/client components |
| **UI Library** | React | 19 | Component-based UI development |
| **Language** | TypeScript | 5 | Type-safe JavaScript |
| **Styling** | Tailwind CSS | 4 | Utility-first CSS framework |
| **Charts** | Recharts | 3.8+ | Interactive data visualization |
| **Dropdowns** | react-select | 5.2+ | Accessible multi-select component |
| **Linting** | ESLint | 9 | Code quality and consistency |

### Component Hierarchy

```
├── app/
│   ├── layout.tsx
│   │   └── Navbar
│   │
│   └── page.tsx (Main Application)
│       ├── Input Section
│       │   ├── Title input
│       │   ├── Body textarea
│       │   └── Subreddit multi-select
│       │
│       ├── Results Panel
│       │   ├── ScoreGauge (Overall engagement score)
│       │   │
│       │   ├── KpiSection
│       │   │   ├── KpiBar (Individual KPI)
│       │   │   ├── KpiBar (Readability)
│       │   │   ├── KpiBar (Sentiment)
│       │   │   └── KpiBar (Structure)
│       │   │
│       │   ├── SpiderChart (Multi-dimensional comparison)
│       │   │
│       │   ├── RedditPostsList
│       │   │   └── RedditPostCard (Similar posts)
│       │   │
│       │   ├── WordsToAddSection (Recommendations)
│       │   │
│       │   ├── AdvicesSection (AI-generated advice)
│       │   │
│       │   └── KpiBar (Best posting times)
│       │
│       └── Loading & Error States
```

### Data Flow

```
User Input (title, body, subreddits)
           ↓
Form Validation
           ↓
API Request to Backend (/search endpoint)
           ├─ X-API-Key authentication
           └─ URL-encoded query parameters
           ↓
Backend Processing
           └─ KPI calculation + Semantic search
           ↓
Response Parsing
           ├─ KPIs (readability, sentiment, structure)
           ├─ Engagement scores
           ├─ Similar posts
           ├─ Advice
           └─ Best posting times
           ↓
Component Rendering
           ├─ ScoreGauge
           ├─ KpiBar components
           ├─ SpiderChart
           ├─ RedditPostCards
           └─ Advice display
           ↓
Interactive UI
           └─ User refines draft
```

## Prerequisites

### System Requirements

- **Node.js** 18.17+ or 20+
- **npm** 9+ (or yarn, pnpm, bun)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Backend API** running at http://localhost:8000 (or configured URL)

### Knowledge of

- React and React hooks (useState, useEffect, useTransition)
- TypeScript basics
- CSS and Tailwind CSS
- Next.js app router fundamentals

## Installation

### Quick Start with Docker

```bash
# From repository root
docker-compose up frontend

# The frontend will be available at http://localhost:3000
# Make sure backend is running at http://localhost:8000
```

### Local Development Setup

#### 1. Navigate to Frontend Directory

```bash
cd Morlana_frontend
```

#### 2. Install Dependencies

```bash
npm install
# or
yarn install
# or
pnpm install
```

#### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env.local

# Edit with your backend URL
nano .env.local  # or your preferred editor
```

**Required Configuration** (`.env.local`):

```env
# Backend API URL (must match your backend deployment)
NEXT_PUBLIC_API_URL = http://localhost:8000/

# Optional: API Key (if using hardcoded key)
# NEXT_PUBLIC_API_KEY = your_api_key_here
```

#### 4. Start Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

#### 5. Build for Production

```bash
npm run build
npm start
```

## Configuration

### Environment Variables

#### Development (`.env.local`)

```env
# Backend API endpoint (Required)
NEXT_PUBLIC_API_URL = http://localhost:8000/

# API Key for authentication (Required)
NEXT_PUBLIC_API_KEY = your_api_key_here

# Optional: Analytics or monitoring
# NEXT_PUBLIC_ANALYTICS_ID = ua-xxxx-x
```

#### Production (Environment at deployment)

Set these variables in your hosting platform (Vercel, Netlify, AWS, etc.):

```env
NEXT_PUBLIC_API_URL = https://api.goodkarma.com/
NEXT_PUBLIC_API_KEY = your_production_api_key
```

**Security Note:** While `NEXT_PUBLIC_` variables are exposed to the client, API keys should still be treated securely. Consider using environment-specific keys and rotating them regularly.

### Backend URL & Authentication

The frontend communicates with the backend via `NEXT_PUBLIC_API_URL`. Ensure:
1. **Backend is running** at the configured URL
2. **API_KEY is configured** in `.env` - it's **required** for `/search` endpoint
3. **CORS is configured** on the backend (if on different domain)
4. **X-API-Key header** is automatically added to all requests to `/search`

## Development

### Running the Dev Server

```bash
npm run dev

# Specify port (default 3000)
npm run dev -- -p 3001
```

Features:
- Hot module reloading (changes instantly)
- Fast refresh (preserves component state)
- Error overlay for quick debugging
- TypeScript error checking

### Code Quality

#### Linting

```bash
# Check all files
npm run lint .

# Lint specific directory
npm run lint app/

# Lint specific file
npm run lint app/page.tsx
```

Uses ESLint with Next.js and TypeScript configurations.

#### Fixing Linting Issues

```bash
# Auto-fix common issues
npm run lint . -- --fix

# Manual fixes may be needed for:
# - Unused imports
# - Missing alt text on images
# - Accessibility issues
```

#### Code Formatting

```bash
# Format with Prettier (optional)
npx prettier --write app/
```

### Creating New Components

#### Component Template

```typescript
// app/components/MyComponent.tsx
'use client';

import React from 'react';

interface MyComponentProps {
  title: string;
  onAction?: () => void;
}

export default function MyComponent({ title, onAction }: MyComponentProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <h3 className="text-lg font-bold text-gray-900">{title}</h3>
      {onAction && (
        <button
          onClick={onAction}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Action
        </button>
      )}
    </div>
  );
}
```

#### Adding to Main Page

```typescript
// In app/page.tsx
import MyComponent from './components/MyComponent';

// Inside component JSX:
<MyComponent title="My Title" onAction={() => handleAction()} />
```

### API Integration

#### Making API Calls

```typescript
// Example in app/page.tsx
async function analyzePost(title: string, body: string, subreddits: string[]) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const apiKey = process.env.NEXT_PUBLIC_API_KEY;

  // Validate API key is configured
  if (!apiKey) {
    throw new Error('API_KEY is not configured. Check your .env file.');
  }

  const params = new URLSearchParams({
    title,
    body,
  });

  // Add subreddits as repeated query parameters
  subreddits.forEach(sub => {
    params.append('subreddits', sub);
  });

  try {
    const response = await fetch(
      `${apiUrl}/search?${params.toString()}`,
      {
        method: 'GET',
        headers: {
          'X-API-Key': apiKey, // Required authentication header
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('Authentication failed: Invalid API key');
      }
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to analyze post:', error);
    throw error;
  }
}
```

### Using React Hooks

#### State Management

```typescript
const [title, setTitle] = useState('');
const [body, setBody] = useState('');
const [isLoading, setIsLoading] = useState(false);
const [results, setResults] = useState<AnalysisResults | null>(null);
```

#### Async Operations with useTransition

```typescript
const [isPending, startTransition] = useTransition();

const handleSubmit = () => {
  startTransition(async () => {
    try {
      const data = await analyzePost(title, body, subreddits);
      setResults(data);
    } catch (error) {
      setError(error.message);
    }
  });
};
```

## Building & Deployment

### Build for Production

```bash
npm run build

# Output: .next/ directory with optimized production bundle
```

### Static Export (if needed)

For static hosting (GitHub Pages, etc.):

```bash
# In next.config.ts
export const nextConfig = {
  output: 'export', // Enable static export
};

npm run build
```

Output will be in `out/` directory.

### Docker Deployment

The frontend includes a multi-stage Dockerfile:

```dockerfile
# Build stage
FROM node:20-alpine AS builder
# ... (see Dockerfile for details)

# Production stage
FROM node:20-alpine AS runner
# ... minimal production image
```

#### Build and Run Docker Image

```bash
# Build
docker build -t good-karma-frontend .

# Run
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://backend:8000 good-karma-frontend
```

#### Or use Docker Compose

```bash
docker-compose up frontend
```

### Deployment Platforms

#### Vercel (Recommended for Next.js)

```bash
npm install -g vercel
vercel login
vercel
```

Then set environment variables in Vercel dashboard.

#### Netlify

```bash
npm install -g netlify-cli
netlify deploy
```

Configure build command: `npm run build`

#### AWS/GCP/Azure

See platform-specific Next.js deployment guides.

## Project Structure

```
Morlana_frontend/
│
├── app/
│   ├── components/
│   │   ├── AdvicesSection.tsx        # AI advice display
│   │   ├── KpiBar.tsx                # Individual KPI metric
│   │   ├── KpiSection.tsx            # All KPIs grouped
│   │   ├── Navbar.tsx                # Top navigation
│   │   ├── RedditPostCard.tsx        # Similar post card
│   │   ├── RedditPostsList.tsx       # List of similar posts
│   │   ├── ScoreGauge.tsx            # Overall engagement gauge
│   │   ├── SpiderChart.tsx           # Multi-dimensional chart
│   │   └── WordsToAddSection.tsx     # Recommendations
│   │
│   ├── api/
│   │   └── (Optional API route handlers)
│   │
│   ├── layout.tsx                    # Root layout
│   ├── page.tsx                      # Main application page
│   ├── globals.css                   # Global styles
│   └── favicon.ico
│
├── public/
│   └── (Static assets)
│
├── .next/                            # Build output (generated)
├── node_modules/                     # Dependencies (generated)
│
├── package.json                      # Dependencies and scripts
├── tsconfig.json                     # TypeScript configuration
├── next.config.ts                    # Next.js configuration
├── eslint.config.mjs                 # ESLint configuration
├── postcss.config.mjs                # PostCSS configuration
├── tailwind.config.ts                # Tailwind CSS configuration
├── Dockerfile                        # Container configuration
├── .env.example                      # Environment template
├── .gitignore
└── README.md                         # This file
```

## Components

### ScoreGauge

Circular gauge showing overall engagement score.

```typescript
<ScoreGauge score={0.75} label="Good" color="green" />
```

**Props:**
- `score: number` - Score 0-1
- `label: string` - Label text (Bad, Medium, Good, Really Good)
- `color: string` - Color theme

### KpiBar

Horizontal bar showing individual KPI metric.

```typescript
<KpiBar
  label="Readability"
  value={72}
  min={0}
  max={100}
  average={65}
/>
```

**Props:**
- `label: string` - KPI name
- `value: number` - Current value
- `min: number` - Minimum value
- `max: number` - Maximum value
- `average: number` - Average reference

### SpiderChart

Multi-dimensional radar/spider chart.

```typescript
<SpiderChart data={kpis} />
```

**Data Format:**
```typescript
{
  readability: 72,
  sentiment: 65,
  structure: 80,
  engagement: 78,
}
```

### RedditPostCard

Card displaying similar Reddit post.

```typescript
<RedditPostCard
  title="Similar Post Title"
  subreddit="r/test"
  score={2500}
  similarity={0.89}
/>
```

### Advanced Features

#### Dynamic Imports

Charts are dynamically imported to avoid SSR issues:

```typescript
const SpiderChart = dynamic(() => import("./components/SpiderChart"), {
  ssr: false,
});
```

#### React Transitions

For async operations with loading states:

```typescript
const [isPending, startTransition] = useTransition();

const handleAnalyze = () => {
  startTransition(async () => {
    const data = await fetchAnalysis();
    setResults(data);
  });
};
```

## Styling

### Tailwind CSS

All styling uses Tailwind utility classes. No custom CSS needed for most cases.

#### Common Utilities

```tsx
// Spacing
className="p-4 m-2"       // padding, margin
className="gap-4"         // grid/flex gap

// Colors
className="bg-blue-500"   // background
className="text-gray-900" // text color
className="border-red-500" // border

// Layout
className="flex flex-col"     // flexbox column
className="grid grid-cols-3"  // CSS grid
className="w-full h-screen"   // width/height

// Responsive
className="md:flex sm:grid"   // breakpoints
className="hover:bg-blue-600" // states
```

#### Custom CSS Variables

See `app/globals.css` for CSS custom properties:

```css
:root {
  --color-primary: #3b82f6;
  --color-success: #10b981;
  --color-danger: #ef4444;
  --color-warning: #f59e0b;
  /* ... more colors ... */
}
```

Use in components:

```tsx
<div style={{ color: "var(--color-primary)" }}>
  Styled text
</div>
```

### Dark Mode Support (Optional)

Tailwind supports dark mode. To add:

1. Update `tailwind.config.ts`:
```typescript
export default {
  darkMode: 'class', // or 'media'
  // ...
};
```

2. Use dark: prefix:
```tsx
<div className="bg-white dark:bg-gray-900">
  Adapts to dark mode
</div>
```

## API Integration

### Base URL & Authentication

All API calls use `NEXT_PUBLIC_API_URL` environment variable with `X-API-Key` header authentication:

```typescript
const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const apiKey = process.env.NEXT_PUBLIC_API_KEY;

const headers = {
  'Content-Type': 'application/json',
  'X-API-Key': apiKey, // Required for /search endpoint
};
```

### Endpoints

```typescript
// Health check (no auth required)
GET {baseUrl}/

// Analyze draft (requires X-API-Key header)
GET {baseUrl}/search?title=...&body=...&subreddits=r/test
Headers: X-API-Key: <your_api_key>

// List subreddits
GET {baseUrl}/subreddits
```

### Error Handling

```typescript
try {
  const response = await fetch(url, {
    headers: {
      'X-API-Key': apiKey,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    if (response.status === 403) {
      throw new Error('Authentication failed: Invalid or missing API key');
    }
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return await response.json();
} catch (error) {
  console.error('API call failed:', error);
  setError(error.message);
  // Show user-friendly error message
}
```

## Performance

### Optimization Techniques

1. **Code Splitting** - Next.js auto-splits by route
2. **Image Optimization** - Use Next.js `Image` component
3. **Dynamic Imports** - Load charts only on client
4. **Lazy Loading** - Load components when needed
5. **Memoization** - Use React.memo() for expensive components

### Metrics to Monitor

- **Largest Contentful Paint (LCP)** - < 2.5s
- **First Input Delay (FID)** - < 100ms
- **Cumulative Layout Shift (CLS)** - < 0.1

Run: `npm run build` and check `.next/static/` output.

## Troubleshooting

### Backend Connection Issues

**Error:** `Failed to fetch from http://localhost:8000`

**Solutions:**
```bash
# 1. Verify backend is running
curl http://localhost:8000/

# 2. Check NEXT_PUBLIC_API_URL in .env.local
cat .env.local | grep NEXT_PUBLIC_API_URL

# 3. If backend on different machine, update URL
NEXT_PUBLIC_API_URL = http://192.168.1.100:8000/

# 4. For CORS issues on backend, enable CORS headers
```

### API Key Authentication

**Error:** `403 Forbidden - Invalid or missing X-API-Key`

**Solutions:**
```bash
# 1. Verify API_KEY is configured in .env
cat .env | grep NEXT_PUBLIC_API_KEY

# 2. Set API key in .env
NEXT_PUBLIC_API_KEY = your_api_key_here

# 3. Ensure it matches the backend API_KEY
# Backend and frontend must use the same key

# 4. Restart dev server after changing .env
npm run dev

# 5. Check browser console for authentication errors
# Open DevTools > Console to see error messages
```

**Tip:** If 403 errors persist, verify:
- API key is not empty or whitespace
- API key matches exactly (case-sensitive)
- Backend has the same API_KEY configured
- Backend is running and accessible

### Build Errors

**Error:** `Module not found` or `TypeScript errors`

**Solutions:**
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build

# Check TypeScript
npx tsc --noEmit

# Check ESLint
npm run lint .
```

### Hot Reload Not Working

**Solution:**
```bash
# Kill dev server and restart
npm run dev

# If still not working, clear cache
rm -rf .next
npm run dev
```

## Contributing

Contributions are welcome! Focus areas:

- 🎨 **UI/UX** - Improve design and user experience
- ♿ **Accessibility** - Better a11y support
- ⚡ **Performance** - Optimize bundle size and render times
- 📱 **Mobile** - Better mobile responsiveness
- 📊 **Visualizations** - New charts and metrics displays
- 📝 **Documentation** - Clearer guides and examples

### Development Workflow

1. Create a feature branch
2. Make changes and test locally
3. Run linting: `npm run lint .`
4. Commit with clear messages
5. Submit pull request with description

## License

GNU Affero General Public License v3.0 (AGPL-3.0)

See [LICENSE](../LICENSE) for details.

## Support

- **Issues:** https://github.com/ElieElDebs/Good-Karma/issues
- **Email:** elie.eldebs@outlook.fr
- **Main README:** [../README.md](../README.md)

---

<p align="center">
  <strong>Built with ❤️ for the Good Karma community</strong>
  <br>
  <a href="https://github.com/ElieElDebs/Good-Karma">⭐ Star us on GitHub</a>
</p>
