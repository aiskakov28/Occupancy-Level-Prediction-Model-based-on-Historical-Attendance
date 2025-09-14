FROM node:20-alpine AS build
WORKDIR /app
RUN corepack enable
COPY apps/dashboard/package.json apps/dashboard/pnpm-lock.yaml* ./apps/dashboard/
WORKDIR /app/apps/dashboard
RUN pnpm install --frozen-lockfile || pnpm install
COPY apps/dashboard ./
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

FROM node:20-alpine
WORKDIR /app
RUN corepack enable
COPY --from=build /app/apps/dashboard ./
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
EXPOSE 3000
CMD ["pnpm","start","-p","3000"]
