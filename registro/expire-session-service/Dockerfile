FROM rust:1.82-slim

WORKDIR /usr/src/app
COPY . .

RUN apt-get update && apt-get install -y pkg-config libssl-dev &&     cargo build --release

CMD ["./target/release/expire-session-service"]
