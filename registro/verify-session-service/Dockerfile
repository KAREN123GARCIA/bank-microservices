FROM rust:1.82

WORKDIR /app
COPY . .

RUN cargo build --release

EXPOSE 8097

CMD ["./target/release/verify-session-service"]