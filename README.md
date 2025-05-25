# 🐳 Docker Mastery — 50 Hands-On Exercises

A practical journey through Docker’s core and advanced concepts. Each folder contains a focused exercise to build your container skills with real-world scenarios.

---

## 📁 Container Basics & Management
- [Create and run containers with basic commands](/containers/run-basics/)
- [Understand and use container lifecycle commands (start, stop, pause, restart)](/containers/lifecycle/)
- [View logs and container stats in real-time](/containers/logs-stats/)
- [Use interactive mode to troubleshoot containers](/containers/interactive-mode/)
- [Manage container resources (memory, CPU limits)](/containers/resources/)
- [Exec into running containers and inspect environment](/containers/exec-inspect/)
- [Remove containers and clean up unused resources](/containers/cleanup/)

---

## 📦 Images & Dockerfiles
- [Write optimized Dockerfiles with multi-stage builds](/images/multistage-dockerfile/)
- [Build custom images from Dockerfiles](/images/build-image/)
- [Tag and push images to Docker Hub or private registries](/images/push-tag/)
- [Use `.dockerignore` files to speed up builds](/images/dockerignore/)
- [Analyze image layers and size with `docker history`](/images/image-layers/)
- [Automate image builds using Docker BuildKit](/images/buildkit/)
- [Understand caching behavior in Docker builds](/images/build-cache/)

---

## 🌐 Networking & Volumes
- [Create and use custom Docker networks](/networking/custom-networks/)
- [Connect multiple containers using user-defined networks](/networking/multi-container-networks/)
- [Expose container ports and map host ports](/networking/port-mapping/)
- [Use Docker DNS for container name resolution](/networking/dns/)
- [Create and mount volumes for persistent data](/volumes/create-mount/)
- [Use bind mounts vs volumes: pros and cons](/volumes/bind-vs-volume/)
- [Backup and restore volume data](/volumes/backup-restore/)
- [Manage volume lifecycle (create, inspect, prune)](/volumes/lifecycle/)

---

## ⚙️ Docker Compose & Multi-Container Apps
- [Write a `docker-compose.yml` file for a multi-service app](/compose/basic-compose/)
- [Use environment variables and `.env` files in Compose](/compose/env-vars/)
- [Manage service dependencies and startup order](/compose/dependencies/)
- [Scale services horizontally using Compose](/compose/scale-services/)
- [Use Compose overrides and multiple Compose files](/compose/overrides/)
- [Access Compose logs and debug multi-container setups](/compose/logs-debug/)
- [Use healthchecks in Compose services](/compose/healthchecks/)
- [Deploy Compose stack to Docker Swarm](/compose/swarm-deploy/)

---

## 🌀 Swarm Mode & Orchestration
- [Initialize a Docker Swarm cluster](/swarm/init/)
- [Add manager and worker nodes to the swarm](/swarm/nodes/)
- [Deploy services with replicated and global modes](/swarm/services/)
- [Update and rollback swarm services](/swarm/update-rollback/)
- [Configure secrets and configs in swarm services](/swarm/secrets-configs/)
- [Use overlay networks for swarm service communication](/swarm/overlay-network/)
- [Monitor swarm cluster and services](/swarm/monitoring/)

---

## 🔐 Security & Best Practices
- [Run containers as non-root users](/security/non-root/)
- [Use Docker Content Trust and image signing](/security/content-trust/)
- [Scan images for vulnerabilities using Docker Scan](/security/image-scan/)
- [Limit container capabilities and use seccomp profiles](/security/seccomp/)
- [Isolate containers using user namespaces](/security/user-namespaces/)
- [Implement resource quotas and limits in swarm](/security/resource-limits/)

---

## 🧰 Advanced Docker Features
- [Use Docker plugins and storage drivers](/advanced/plugins-storage/)
- [Create and use custom networks with macvlan driver](/advanced/macvlan/)
- [Build and use multi-architecture images with `docker buildx`](/advanced/buildx/)
- [Use Docker events and logging drivers](/advanced/events-logging/)
- [Automate image builds and deployments with Docker Hub webhooks](/advanced/webhooks/)

---

## 🌐 Integration & Ecosystem
- [Use Docker with Kubernetes (kind or minikube)](/integration/docker-k8s/)
- [Integrate Docker with CI/CD pipelines (Jenkins, GitHub Actions)](/integration/ci-cd/)
