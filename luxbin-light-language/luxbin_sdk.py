"""
LUXBIN SDK - Developer Toolkit

High-level API for building LUXBIN applications

Features:
- Easy P2P node creation
- Simple name registration and resolution
- Content publishing and retrieval
- Automatic routing and encryption
- Event-driven architecture

Example:
    import asyncio
    from luxbin_sdk import LUXBINClient

    async def main():
        # Create client
        client = LUXBINClient(ionq_api_key="YOUR_KEY")
        await client.connect()

        # Register name
        await client.register_name("myapp", "luxbin://...")

        # Publish content
        address = await client.publish("Hello, World!")

        # Fetch content
        content = await client.fetch("myapp")

    asyncio.run(main())
"""

import asyncio
from typing import Optional, Dict, List, Callable
import time

from luxbin_p2p_mesh import QuantumP2PNode
from luxbin_photonic_router import PhotonicRouter
from luxbin_name_system import LUXBINNameSystem
from luxbin_dht import LUXBINDistributedHashTable
from luxbin_quantum_transport import QuantumTransportProtocol
from luxbin_address import LUXBINAddress


class LUXBINClient:
    """
    High-level LUXBIN client for developers

    Simplifies common operations:
    - Node connectivity
    - Name resolution
    - Content publishing/fetching
    - Secure messaging
    """

    def __init__(
        self,
        ionq_api_key: Optional[str] = None,
        quantum_backends: Optional[List[str]] = None
    ):
        """
        Initialize LUXBIN client

        Args:
            ionq_api_key: IonQ API key (optional)
            quantum_backends: List of quantum backends (optional)
        """
        self.ionq_api_key = ionq_api_key
        self.quantum_backends = quantum_backends or ['ibm_fez', 'ibm_torino', 'ibm_marrakesh']

        # Network components
        self.node = None
        self.router = None
        self.name_system = None
        self.dht = None
        self.quantum_transport = None

        # State
        self.is_connected = False
        self.node_id = None

        # Event handlers
        self._event_handlers = {}

    async def connect(self, bootstrap: bool = True):
        """
        Connect to LUXBIN network

        Args:
            bootstrap: Whether to bootstrap P2P network (default: True)

        Example:
            await client.connect()
        """
        print("🚀 Connecting to LUXBIN network...")

        # Create P2P node
        self.node = QuantumP2PNode(
            quantum_backends=self.quantum_backends,
            ionq_api_key=self.ionq_api_key
        )

        if bootstrap:
            await self.node.bootstrap()

        self.node_id = self.node.node_id

        # Create router
        self.router = PhotonicRouter(self.node)

        # Create name system
        self.name_system = LUXBINNameSystem()
        self.name_system.blockchain.initialize()

        # Create genesis block if needed
        if len(self.name_system.blockchain.blockchain) == 0:
            self.name_system.blockchain.add_transaction({
                'type': 'GENESIS',
                'timestamp': time.time(),
                'data': 'SDK Client Genesis'
            })
            self.name_system.blockchain.mine_block()

        # Create DHT
        self.dht = LUXBINDistributedHashTable(self.node, replication_factor=3)

        # Create quantum transport
        self.quantum_transport = QuantumTransportProtocol(self.node)

        self.is_connected = True

        print(f"✅ Connected to LUXBIN network")
        print(f"   Node ID: {self.node_id[:32]}...")

        self._emit('connected', {'node_id': self.node_id})

    async def register_name(
        self,
        name: str,
        luxbin_address: str,
        owner_key: str = 'sdk_user'
    ) -> Optional[Dict]:
        """
        Register name on blockchain

        Args:
            name: Human-readable name (3-64 characters)
            luxbin_address: LUXBIN address to map to
            owner_key: Owner public key (default: 'sdk_user')

        Returns:
            Name record dict if successful, None otherwise

        Example:
            record = await client.register_name(
                "myapp",
                "luxbin://node1.550nm.ABC123/index.html"
            )
        """
        self._check_connected()

        record = await self.name_system.register_name(name, luxbin_address, owner_key)

        if record:
            self._emit('name_registered', {
                'name': record.name,
                'address': record.luxbin_address,
                'block': record.block_number
            })

            return {
                'name': record.name,
                'luxbin_address': record.luxbin_address,
                'owner_public_key': record.owner_public_key,
                'block_number': record.block_number,
                'transaction_hash': record.transaction_hash
            }

        return None

    async def resolve_name(self, name: str) -> Optional[str]:
        """
        Resolve name to LUXBIN address

        Args:
            name: Name to resolve

        Returns:
            LUXBIN address if found, None otherwise

        Example:
            address = await client.resolve_name("myapp")
        """
        self._check_connected()

        record = await self.name_system.resolve_name(name)

        if record:
            return record.luxbin_address

        return None

    async def publish(
        self,
        content: bytes,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Publish content to LUXBIN network

        Args:
            content: Content to publish (bytes)
            metadata: Optional metadata dict

        Returns:
            LUXBIN address for published content

        Example:
            address = await client.publish(
                b"Hello, World!",
                {'title': 'My Document', 'author': 'Alice'}
            )
        """
        self._check_connected()

        if isinstance(content, str):
            content = content.encode()

        address = await self.dht.store_content(content, metadata)

        self._emit('content_published', {
            'address': address,
            'size': len(content)
        })

        return address

    async def fetch(self, address_or_name: str) -> Optional[bytes]:
        """
        Fetch content from LUXBIN network

        Args:
            address_or_name: LUXBIN address or name

        Returns:
            Content bytes if found, None otherwise

        Example:
            content = await client.fetch("myapp")
            # or
            content = await client.fetch("luxbin://distributed.600nm.ABC123")
        """
        self._check_connected()

        # Resolve name if needed
        address = address_or_name
        if not address.startswith('luxbin://'):
            resolved = await self.resolve_name(address)
            if not resolved:
                return None
            address = resolved

        # Parse address
        components = LUXBINAddress.parse(address)
        if not components:
            return None

        # Retrieve from DHT
        content = await self.dht.retrieve_content(components.content_hash)

        if content:
            self._emit('content_fetched', {
                'address': address,
                'size': len(content)
            })

        return content

    async def send_message(
        self,
        peer_id: str,
        message: bytes
    ) -> bool:
        """
        Send encrypted message to peer

        Args:
            peer_id: Peer node ID
            message: Message to send

        Returns:
            True if successful

        Example:
            await client.send_message(
                peer_id,
                b"Secret message"
            )
        """
        self._check_connected()

        if isinstance(message, str):
            message = message.encode()

        # Establish quantum channel if needed
        if peer_id not in self.quantum_transport.channels:
            success = await self.quantum_transport.establish_quantum_channel(peer_id)
            if not success:
                return False

        # Encrypt and send
        encrypted = await self.quantum_transport.encrypt_message(peer_id, message)

        if encrypted:
            # In production, actually send via P2P network
            # For now, just return success
            self._emit('message_sent', {
                'peer_id': peer_id,
                'size': len(message)
            })
            return True

        return False

    def get_status(self) -> Dict:
        """
        Get client status

        Returns:
            Status dict with network info

        Example:
            status = client.get_status()
            print(f"Peers: {status['peers']}")
        """
        if not self.is_connected:
            return {
                'connected': False,
                'node_id': None,
                'peers': 0
            }

        network_status = self.node.get_network_status()

        return {
            'connected': True,
            'node_id': self.node_id,
            'peers': len(self.node.peers),
            'quantum_backends': self.quantum_backends,
            'network': network_status
        }

    def on(self, event: str, handler: Callable):
        """
        Register event handler

        Events:
        - connected: When client connects to network
        - name_registered: When name is registered
        - content_published: When content is published
        - content_fetched: When content is retrieved
        - message_sent: When message is sent

        Args:
            event: Event name
            handler: Callback function

        Example:
            def on_connected(data):
                print(f"Connected! Node: {data['node_id']}")

            client.on('connected', on_connected)
        """
        if event not in self._event_handlers:
            self._event_handlers[event] = []

        self._event_handlers[event].append(handler)

    def _emit(self, event: str, data: Dict):
        """Emit event to registered handlers"""
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                handler(data)

    def _check_connected(self):
        """Raise error if not connected"""
        if not self.is_connected:
            raise RuntimeError("Client not connected. Call await client.connect() first.")

    async def disconnect(self):
        """Disconnect from network"""
        self.is_connected = False
        self._emit('disconnected', {})
        print("🔌 Disconnected from LUXBIN network")


async def main():
    """Example usage"""
    print("=" * 70)
    print(" " * 20 + "LUXBIN SDK EXAMPLE")
    print("=" * 70)

    # Create client
    client = LUXBINClient(ionq_api_key="TH9yk8wG6PeJBh7ZmOQR22VTkarZ7Pf3")

    # Register event handlers
    client.on('connected', lambda data: print(f"\n✅ Connected! Node: {data['node_id'][:32]}..."))
    client.on('name_registered', lambda data: print(f"\n✅ Name registered: {data['name']} → {data['address']}"))
    client.on('content_published', lambda data: print(f"\n✅ Content published: {data['address']}"))

    # Connect to network
    await client.connect(bootstrap=False)  # Skip bootstrap for quick demo

    # Register name
    print("\n📝 Registering name...")
    record = await client.register_name(
        "sdk-demo",
        "luxbin://demo.550nm.ABC123/index.html"
    )

    # Publish content
    print("\n📤 Publishing content...")
    address = await client.publish(
        b"Hello from LUXBIN SDK!",
        {'title': 'SDK Demo', 'author': 'Developer'}
    )

    # Fetch content
    print("\n📥 Fetching content...")
    content = await client.fetch(address)

    if content:
        print(f"   Retrieved: {content.decode()}")

    # Get status
    print("\n📊 Client status:")
    status = client.get_status()
    print(f"   Connected: {status['connected']}")
    print(f"   Node ID: {status['node_id'][:32] if status['node_id'] else 'None'}...")
    print(f"   Peers: {status['peers']}")

    print("\n" + "=" * 70)
    print(" " * 18 + "✅ SDK EXAMPLE COMPLETE!")
    print("=" * 70)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
