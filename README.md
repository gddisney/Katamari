# Katamari
Katamari Ecosystem
# Katamari Ecosystem

Welcome to the **Katamari Ecosystem**, a modular system designed to offer a flexible, near real-time platform for handling distributed workloads, data pipelines, message queuing, serverless functions, UI building, and much more. This ecosystem combines the power of multiple components working together seamlessly to provide a complete infrastructure for modern applications.

## Key Components of the Katamari Ecosystem

The Katamari Ecosystem consists of the following key components:

1. [KatamariDB](docs/KatamariDB.md): A file-based, highly flexible key-value store inspired by MongoDB and Redis, using Elasticsearch-like queries. It supports Multi-Version Concurrency Control (MVCC) and provides basic ORM capabilities.

2. [KatamariPipelines](docs/KatamariPipelines.md): A pipeline execution framework to manage ETL processes and real-time data streaming. It integrates with **KatamariDB** and **KatamariLambda** to process jobs efficiently.

3. [KatamariMQ](docs/KatamariMQ.md): A message queue system that distributes jobs to workers, manages sharding for large datasets, and sends Lambda functions for execution. It includes both a server and client implementation, enabling distributed workloads and clustering.

4. [KatamariLambda](docs/KatamariLambda.md): A serverless compute platform designed to handle event-driven workloads and scalable function execution. KatamariLambda allows you to define, schedule, and execute functions across distributed systems.

5. [KatamariUI](docs/KatamariUI.md): A Streamlit-like UI framework integrated with FastAPI and WebSockets. It allows dynamic page rendering, theming, real-time updates, and components like charts, forms, and tables.

6. [KatamariCharts](docs/KatamariCharts.md): A charting component of the ecosystem, supporting both **Chart.js** and **Matplotlib** for generating visualizations and embedding them within the **KatamariUI**.

## Getting Started

To get started with the **Katamari Ecosystem**, clone the repository, and explore the individual components inside the `docs/` directory for detailed usage instructions and examples.

```bash
git clone https://github.com/your-repo/katamari-repo.git
```

### Running Demos

Inside the **demos/** directory, you'll find several sample applications and projects that demonstrate the capabilities of the ecosystem. These include:

- **WordPress Clone**
- **Twitter Clone**
- **News RSS Aggregator**
- **Tabulae Clone**

Each demo showcases how to integrate and utilize multiple components of the Katamari Ecosystem.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

For detailed information on each component, refer to the individual documentation files listed below:

- [KatamariDB Documentation](docs/KatamariDB.md)
- [KatamariPipelines Documentation](docs/KatamariPipelines.md)
- [KatamariMQ Documentation](docs/KatamariMQ.md)
- [KatamariLambda Documentation](docs/KatamariLambda.md)
- [KatamariUI Documentation](docs/KatamariUI.md)
- [KatamariCharts Documentation](docs/KatamariCharts.md)

---
