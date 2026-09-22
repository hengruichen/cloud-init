# Cloud-Init

[![CI](https://github.com/cloud-init/cloud-init/actions/workflows/main.yml/badge.svg)](https:***REDACTED***@github.com:cloud-init/cloud-init.git
```

## Build

To build the source code, run:

```bash
make
```

This will build the `cloud-init` CLI and the `cloud-config` CLI.

The `cloud-init` CLI is located at `build/cloud-init`.

The `cloud-config` CLI is located at `build/cloud-config`.

## Install

To install the CLI, run:

```bash
sudo make install
```

This will install the `cloud-init` CLI and the `cloud-config` CLI.

The `cloud-init` CLI is installed to `/usr/bin/cloud-init`.

The `cloud-config` CLI is installed to `/usr/bin/cloud-config`.

## Run

To run the CLI, run:

```bash
sudo cloud-init
sudo cloud-config
```

## Documentation

The documentation is available at [docs.cloud-init.io](https://docs.cloud-init.io/).

## Contributing

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for information on how to
contribute to this project.

## License

Copyright (c) 2007-2025 Canonical Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

