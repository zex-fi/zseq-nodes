import click
from random import randbytes
import json
import time

from eigensdk.chainio.clients.builder import BuildAllConfig, build_all
from eigensdk.crypto.bls import attestation
from eth_account import Account


@click.group()
def cli():
    """ZSequencer Operator Registration CLI."""
    pass


@cli.command()
@click.option(
    "--rpc-node",
    required=True,
    help="RPC Url",
)
@click.option(
    "--registry-coordinator",
    required=True,
    help="registry coordinator contract address",
)
@click.option(
    "--operator-state-retriever",
    required=True,
    help="operator state retriever contract address",
)
@click.option(
    "--bls-key-file",
    required=True,
    help="Path to the BLS key file.",
    type=click.Path(exists=True),
)
@click.option(
    "--bls-key-password", required=True, help="Password for the BLS key file."
)
@click.option(
    "--ecdsa-key-file",
    required=True,
    help="Path to the ECDSA key file.",
    type=click.Path(exists=True),
)
@click.option(
    "--ecdsa-key-password",
    required=True,
    help="Password for the ECDSA key file.",
)
@click.option(
    "--sequencer-register-socket", required=True, help="IP:Port of the operator."
)
def register(
    rpc_node,
    registry_coordinator,
    operator_state_retriever,
    bls_key_file,
    bls_key_password,
    ecdsa_key_file,
    ecdsa_key_password,
    sequencer_register_socket,
):
    """Register an operator with the provided BLS and ECDSA keys."""
    # Load BLS key pair
    bls_key_pair = attestation.KeyPair.read_from_file(bls_key_file, bls_key_password)

    # Load ECDSA private key
    with open(ecdsa_key_file) as f:
        encrypted_json = json.loads(f.read())
    ecdsa_private_key = Account.decrypt(encrypted_json, ecdsa_key_password)

    # Register the operator
    register_operator(
        rpc_node,
        registry_coordinator,
        operator_state_retriever,
        ecdsa_private_key,
        bls_key_pair,
        sequencer_register_socket,
    )
    click.echo("Operator registered successfully!")


@cli.command()
@click.option(
    "--rpc-node",
    required=True,
    help="RPC Url",
)
@click.option(
    "--registry-coordinator",
    required=True,
    help="registry coordinator contract address",
)
@click.option(
    "--operator-state-retriever",
    required=True,
    help="operator state retriever contract address",
)
@click.option(
    "--ecdsa-key-file",
    required=True,
    help="Path to the ECDSA key file.",
    type=click.Path(exists=True),
)
@click.option(
    "--ecdsa-key-password",
    required=True,
    help="Password for the ECDSA key file.",
)
@click.option("--sequencer-new-socket", required=True, help="IP:Port of the operator.")
def update(
    rpc_node,
    registry_coordinator,
    operator_state_retriever,
    ecdsa_key_file,
    ecdsa_key_password,
    sequencer_new_socket,
):
    """Update an operator's socket address."""

    # Load ECDSA private key
    with open(ecdsa_key_file) as f:
        encrypted_json = json.loads(f.read())
    ecdsa_private_key = Account.decrypt(encrypted_json, ecdsa_key_password)

    # Register the operator
    update_socket(
        rpc_node,
        registry_coordinator,
        operator_state_retriever,
        ecdsa_private_key,
        sequencer_new_socket,
    )
    click.echo("Operator registered successfully!")


def update_socket(
    rpc_node,
    registry_coordinator,
    operator_state_retriever,
    ecdsa_private_key,
    sequencer_new_socket,
):
    config = BuildAllConfig(
        eth_http_url=rpc_node,
        registry_coordinator_addr=registry_coordinator,
        operator_state_retriever_addr=operator_state_retriever,
    )

    clients = build_all(config, ecdsa_private_key)
    clients.avs_registry_writer.update_socket(
        socket=sequencer_new_socket,
    )


def register_operator(
    rpc_node,
    registry_coordinator,
    operator_state_retriever,
    ecdsa_private_key,
    bls_key_pair,
    sequencer_register_socket,
) -> None:
    config = BuildAllConfig(
        eth_http_url=rpc_node,
        registry_coordinator_addr=registry_coordinator,
        operator_state_retriever_addr=operator_state_retriever,
    )

    clients = build_all(config, ecdsa_private_key)
    clients.avs_registry_writer.register_operator_in_quorum_with_avs_registry_coordinator(
        operator_ecdsa_private_key=ecdsa_private_key,
        operator_to_avs_registration_sig_salt=randbytes(32),
        operator_to_avs_registration_sig_expiry=int(time.time()) + 60,
        bls_key_pair=bls_key_pair,
        quorum_numbers=[0],
        socket=sequencer_register_socket,
    )


if __name__ == "__main__":
    cli()
