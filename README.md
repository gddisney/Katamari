# Katamari Ecosystem

Welcome to the **Katamari Ecosystem**, a modular, event-driven architecture designed to offer a flexible, end-to-end solution for handling distributed workloads, data pipelines, message queuing, serverless functions, real-time UI rendering, dynamic metric aggregation, identity and access management, and more. The **Katamari Ecosystem** seamlessly integrates its components to provide modern, scalable, data-driven infrastructure for a wide range of applications.

## Key Components of the Katamari Ecosystem

The **Katamari Ecosystem** consists of tightly integrated components, each specialized for specific tasks. Together, they form a powerful, cohesive, event-driven system:

### KatamariDB
![KatamariDB Overview](imgs/katamaridb.webp)

- A file-based, highly flexible key-value store inspired by MongoDB and Redis, with Elasticsearch-like query capabilities.
- Features a **Multi-Version Concurrency Control (MVCC)** system and a full-fledged **Object-Relational Mapping (ORM)** for advanced query handling and schema management.

### KatamariPipelines
![KatamariPipelines Overview](imgs/katamaripipelines.webp)

- A pipeline execution framework that orchestrates ETL (Extract, Transform, Load) processes and real-time data streaming.
- Seamlessly integrates with **KatamariDB** and **KatamariLambda** to manage workflows in an event-driven manner, ensuring efficient and responsive data handling.

### KatamariMQ
![KatamariMQ Overview](imgs/katamarimq.webp)

- A distributed message queue system designed for workload distribution, data sharding, and dynamic task management.
- Works in conjunction with **KatamariLambda** to execute serverless functions triggered by events, ensuring both scalability and resilience.

### KatamariLambda
![KatamariLambda Overview](imgs/katamarilambda.webp)

- A serverless compute platform that supports event-driven, distributed function execution.
- Provides the ability to define, schedule, and execute serverless functions, tightly integrated with **KatamariMQ** for dynamic task execution across distributed nodes.

### KatamariUI
- An asynchronous UI framework based on **FastAPI** and **WebSockets**, enabling real-time dynamic page rendering and interactive components.
- Supports theming, notifications, and visualizations, making it ideal for building real-time dashboards, admin interfaces, and responsive web applications.

### KatamariCharts
- A flexible charting component that supports both **Chart.js** and **Matplotlib** for creating rich, interactive data visualizations.
- Integrates easily with **KatamariUI**, enabling real-time data-driven visualizations for dashboards and analytics.

### KatamariAggregation
- A real-time, dynamic metric aggregation engine built on top of **KatamariDB** and **KatamariORM**.
- Allows users to define custom metrics and compute them over both real-time data streams and historical datasets, making it ideal for monitoring, performance tracking, and analytics.

### KatamariIAM
- A robust Identity and Access Management (IAM) solution integrated with **KatamariDB** and supporting multiple authentication methods.
- Provides **OAuth2**, **JWT-based authentication**, and **API key-based access** for users and service accounts.
- Features role-based access control (RBAC), multi-factor authentication support, session management, and **argon2**-based password hashing for secure user management.
- Seamlessly integrates with other **Katamari Ecosystem** components to secure access to data, services, and functions.

---

## Getting Started

To begin exploring the **Katamari Ecosystem**, clone the repository and dive into the individual components located in the `docs/` directory for detailed setup, configuration, and usage instructions.

```bash
git clone https://github.com/gddisney/katamari.git
```

### Running Demos

Inside the **demos/** directory, you'll find various sample applications showcasing how the **Katamari Ecosystem** components work together in real-world scenarios. These include:

- **WordPress Clone**: Demonstrates content management using **KatamariUI** and **KatamariDB**.
- **Twitter Clone**: A social media platform leveraging **KatamariMQ** and **KatamariLambda** for real-time workload distribution and handling.
- **News RSS Aggregator**: Shows ETL processes and data aggregation using **KatamariPipelines**.
- **Tabulae Clone**: A comprehensive example of data processing and visualization using **KatamariAggregation** and **KatamariCharts**.

Each demo is designed to highlight the power of the **Katamari Ecosystem** in various application domains, from real-time data streaming to complex visualizations and serverless computing.

---

## Example Use Cases

1. **End-to-End Event-Driven Architecture**: Build fully reactive systems where real-time data flows through **KatamariPipelines**, is processed by **KatamariLambda**, and dynamically rendered in **KatamariUI**. Ideal for low-latency applications such as IoT, financial trading platforms, or real-time data aggregation.

2. **Distributed Job Scheduling**: Use **KatamariMQ** with **KatamariLambda** to distribute workloads across multiple nodes. This enables event-driven task execution, with built-in support for data sharding, making it scalable for large-scale systems.

3. **Real-Time Dashboards and Alerts**: Combine **KatamariUI**, **KatamariCharts**, and **KatamariAggregation** to build dynamic dashboards that automatically update with real-time data. Perfect for monitoring systems and visualizing metrics as they change in real-time.

4. **Dynamic Metric Aggregation and Monitoring**: Leverage **KatamariAggregation** to define custom metrics on the fly and calculate them over both real-time and historical data streams. This is ideal for application performance monitoring, alerting, and generating insightful analytics.

5. **Identity and Access Management for Secure Applications**: Use **KatamariIAM** to secure applications with **OAuth2**, **JWT tokens**, and **API key-based authentication**. Assign roles and permissions to users and service accounts, control access to resources, and manage secure authentication across your distributed system.

---

## Ecosystem Components

Explore each component of the **Katamari Ecosystem** in detail:

- **KatamariDB**: A flexible, file-based key-value store with MVCC and ORM capabilities, perfect for high-performance, scalable storage.
- **KatamariPipelines**: Manage ETL workflows and real-time data processing with an event-driven execution model.
- **KatamariMQ**: A powerful message queue for workload distribution, seamlessly integrated with serverless functions.
- **KatamariLambda**: A serverless compute platform for distributed, event-driven function execution.
- **KatamariUI**: A real-time UI framework for creating dashboards and admin interfaces with dynamic visualizations.
- **KatamariCharts**: Integrates with **KatamariUI** to provide rich, interactive data visualizations.
- **KatamariAggregation**: Real-time metric computation and aggregation over stored and streaming data.
- **KatamariIAM**: A secure identity and access management system supporting multi-factor authentication, API keys, and role-based access control.

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).

For detailed documentation on each component, refer to the individual files in the `docs/` directory:

- [KatamariDB Documentation](docs/KatamariDB.md)
- [KatamariPipelines Documentation](docs/KatamariPipelines.md)
- [KatamariMQ Documentation](docs/KatamariMQ.md)
- [KatamariLambda Documentation](docs/KatamariLambda.md)
- [KatamariUI Documentation](docs/KatamariUI.md)
- [KatamariCharts Documentation](docs/KatamariCharts.md)
- [KatamariAggregation Documentation](docs/KatamariAggregation.md)
- [KatamariIAM Documentation](docs/KatamariIAM.md)

---

The **Katamari Ecosystem** is a cutting-edge, event-driven framework designed to solve the challenges of modern, distributed applications. It provides a solid foundation for building highly scalable, data-centric applications with a focus on real-time processing, serverless functions, distributed messaging, dynamic visualizations, and secure access management.

Explore the full power of the **Katamari Ecosystem** and start building event-driven, data-driven, and secure applications today!
