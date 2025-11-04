# Scheduling Brain Service

This repository contains a Python-based microservice that provides staff scheduling optimization as a REST API. It replaces the Excel-based workflow with a scalable, programmatic solution using FastAPI and OR‑Tools.

## Features

- **REST API** (`/optimize`) for submitting scheduling requests and receiving optimized schedules.
- Uses **Google OR‑Tools** (CP‑SAT solver) to find optimal assignments based on cost and preference matrices.
- Modular design: separate modules for the optimizer, summary analytics, and API layer.
- Easy to deploy on cloud platforms like Render, Google Cloud Run, or AWS.
- Optional Dockerfile for containerized deployment.

## Project Structure

