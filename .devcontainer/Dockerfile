FROM ubuntu:latest

ENV ZOLA_VERSION=0.20.0

# Install all dependancies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="${HOME}/.cargo/bin:${PATH}"

# Install zola
RUN curl -sSL "https://github.com/getzola/zola/releases/download/v${ZOLA_VERSION}/zola-v${ZOLA_VERSION}-x86_64-unknown-linux-gnu.tar.gz"| tar xz -C /usr/local/bin

USER user

# Workspace
WORKDIR /app

# Copy project
COPY . .

# Default command
CMD ["zola", "serve"]
