# --- Build stage ---
FROM node:20-alpine AS builder

WORKDIR /app

# Install all dependencies (including devDependencies)
COPY package.json package-lock.json* ./
RUN npm ci

# Copy all files
COPY . .

# Build Next.js app
RUN npm run build

# --- Production stage ---
FROM node:20-alpine AS runner

WORKDIR /app

# Copy only production dependencies
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

# Copy built app and necessary files from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/next.config.* ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/app ./app

EXPOSE 3000

CMD ["npm", "start"]
