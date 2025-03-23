# setup
copy `zsequencer.env.example` to each `node*` folder and change the key path and the password. modify other keys if needed and run:

```bash
docker compose up
```

# Register AVS
```bash
docker build zseq-node-initializer:dev .

docker run -it --rm \
  -v <$(pwd)/ecdsa_key.json>:/app/ecdsa_key.json \
  -v <$(pwd)/bls_key.json>:/app/bls_key.json \
  zseq-node-initializer:dev register \
  --rpc-node <rpc node url> \
  --registry-coordinator <0x1234> \
  --operator-state-retriever <0x1234> \
  --bls-key-file /app/bls_key.json \
  --bls-key-password <bls_password> \
  --ecdsa-key-file /app/ecdsa_key.json \
  --ecdsa-key-password <ecdsa_password> \
  --sequencer-register-socket <ip:port>
```
