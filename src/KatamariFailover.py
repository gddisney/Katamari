class KatamariFailover:
    """Manages failover logic between cloud providers."""

    def __init__(self, providers: Dict[str, KatamariProviderInterface], wal_manager: WALManager):
        self.providers = providers
        self.wal_manager = wal_manager

    async def failover_to_provider(self, failed_provider: str, instance_type: str, region: str):
        """Failover to another provider."""
        logger.error(f"Failover triggered: {failed_provider} failed. Switching to another provider.")
        available_providers = [p for p in self.providers if p != failed_provider]
        for provider_name in available_providers:
            provider = self.providers[provider_name]
            return await provider.provision_instance(instance_type, region)
