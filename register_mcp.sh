#!/bin/bash

MCP_ID="mcp-audio"
HELP_FILE="mcp_audio_registration.json"
CANISTER="endpoint_registry"
NETWORK="local"

if ! command -v jq &> /dev/null
then
    echo "jq is not installed. Please install jq first."
    exit 1
fi

JSON_PAYLOAD=$(cat "$HELP_FILE" | jq -c .)

echo "Registering MCP [$MCP_ID] to [$CANISTER] on [$NETWORK]..."

dfx canister --network "$NETWORK" call "$CANISTER" register_mcp "(\"$JSON_PAYLOAD\")"
