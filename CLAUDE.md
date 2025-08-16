# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Baserow is an open-source no-code database tool and Airtable alternative. It consists of:
- **Backend**: Django-based API server (Python 3.11+)
- **Web Frontend**: Nuxt.js/Vue.js application (Node 24.0.0)
- **Database**: PostgreSQL for data storage

The repository includes OSS (MIT licensed), Premium, and Enterprise editions with a modular architecture supporting plugins.

## Development Commands

### Backend Commands (from `/backend` directory)

```bash
# Install full Baserow with premium/enterprise
make install

# Install OSS version only  
make install-oss

# Run development server
make run-dev  # Runs on 0.0.0.0:8000

# Run tests
make test              # Run all tests
make test-parallel     # Run tests in parallel
make test-coverage     # Generate coverage report

# Linting and formatting
make lint              # Check code style
make lint-fix          # Auto-fix code style issues
make format            # Format with black
make sort              # Sort imports with isort

# Database migrations
baserow makemigrations
baserow migrate
```

### Frontend Commands (from `/web-frontend` directory)

```bash
# Install dependencies
yarn install

# Run development server
yarn dev               # Runs on localhost:3000

# Run tests
yarn test              # Run all tests (core, premium, enterprise)
yarn test-coverage     # Generate coverage reports

# Linting and formatting
yarn lint              # Run eslint and stylelint
yarn fix               # Auto-fix linting issues
```

### Full Stack Development

```bash
# From root directory - starts all services with hot reloading
./dev.sh --build      # Initial setup with build
./dev.sh              # Start dev environment

# Using docker-compose
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Make commands from root
make docker-build     # Build docker images
make docker-start     # Start dev environment
make docker-stop      # Stop dev environment
```

## High-Level Architecture

### Backend Structure (`/backend/src/baserow/`)
- **`api/`**: REST API endpoints, authentication, serializers
- **`core/`**: Core functionality - workspaces, permissions, services
- **`contrib/`**: Main applications (database, builder, automation)
  - `database/`: Table/field management, views, formulas
  - `builder/`: Page builder application
  - `automation/`: Workflow automation features
- **`ws/`**: WebSocket support for real-time updates
- **`config/`**: Django settings and configuration

### Frontend Structure (`/web-frontend/modules/`)
- **`core/`**: Core UI components, authentication, workspace management
- **`database/`**: Database views (grid, gallery, form, kanban)
- **`builder/`**: Page builder UI
- **`automation/`**: Automation workflow editor

### Plugin System
Baserow uses a registry-based plugin architecture allowing custom:
- Field types
- View types  
- Applications
- Data providers
- Workflow actions

Plugins are registered in both backend (`registries.py`) and frontend (`plugin.js`) modules.

## Key Development Patterns

### Backend
- Uses Django REST Framework for API endpoints
- Service layer pattern for business logic (`service.py` files)
- Handler pattern for complex operations (`handler.py` files)
- Extensive use of Django signals for event handling
- Custom permission system with object-level permissions

### Frontend
- Nuxt.js modules for application structure
- Vuex stores for state management
- Mixins for shared component logic
- Real-time updates via WebSocket connections

## Testing Approach

### Backend Testing
- Tests located in `tests/` directories
- Uses pytest with Django test fixtures
- Database tests use transactions for isolation
- Mock external services and API calls

### Frontend Testing
- Uses Jest for unit testing
- Tests located in `test/` directories
- Component testing with Vue Test Utils
- Snapshot testing for UI consistency

## Important Notes

- Always check existing code patterns before implementing new features
- The codebase follows modular architecture - check if functionality belongs in core, a contrib module, or as a plugin
- Database migrations are critical - always test migration paths
- WebSocket connections handle real-time collaboration features
- Premium and Enterprise features are in separate directories but integrate with core

## Current Working Context

This appears to be a patched version of Baserow 1.33.4 with VocabAI-specific modifications. The main branch is `master` and there are uncommitted changes to `backend/src/baserow/contrib/database/fields/field_types.py`.