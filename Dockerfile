FROM python:3.12

RUN pip3 install cmake && \
    git clone https://github.com/herumi/mcl.git && \
    cd mcl && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j8 && \
    make install

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the application dependencies.
WORKDIR /app

# Copy the application into the container.
COPY .python-version pyproject.toml uv.lock register_avs.py  ./

RUN uv sync --frozen --no-cache

# Set the entrypoint to run the script using Click
ENTRYPOINT ["/app/.venv/bin/python", "register_avs.py"]
