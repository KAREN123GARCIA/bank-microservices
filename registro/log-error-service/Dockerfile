# Etapa de compilación
FROM rust:1.82-bookworm as builder
WORKDIR /usr/src/app
COPY . .
RUN cargo build --release

# Etapa de producción
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/src/app/target/release/log-error-service /usr/local/bin/log-error-service
CMD ["log-error-service"]
