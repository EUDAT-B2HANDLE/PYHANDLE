# Publishing PyHandle

Releases are published from GitHub Actions when a `v*` tag is pushed. Configure
the `pypi` environment as a trusted publisher for this repository on PyPI, then
create and push a version tag (for example, `v1.5.0`).

To build locally, run `uv build`. The source version is defined in
`pyproject.toml` and should match the release tag.
