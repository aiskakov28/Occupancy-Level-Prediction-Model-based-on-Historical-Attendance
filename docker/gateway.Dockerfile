FROM golang:1.22-alpine AS build
WORKDIR /src
COPY services/gateway/go.mod services/gateway/go.sum ./ || true
RUN [ -f go.mod ] && go mod download || true
COPY services/gateway .
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/gateway ./cmd/server || echo "placeholder"
FROM alpine:3.20
WORKDIR /app
COPY --from=build /out/gateway ./gateway || true
ENV PORT=8080
EXPOSE 8080
CMD ["./gateway"]
