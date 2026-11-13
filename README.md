# .github

Workflows compartidos entre mis proyectos.

## Descripción de Docker Hub

[`dockerhub-description.yml`](.github/workflows/dockerhub-description.yml) publica el README de un proyecto como descripción de su imagen en Docker Hub, para que nunca haya que editarla a mano.

En el README se marcan las partes que cambian, con comentarios que GitHub no muestra:

```markdown
<!-- dockerhub:skip -->
Solo en GitHub: clonar el repo, desarrollo en local...
<!-- /dockerhub:skip -->

<!-- dockerhub:only
Solo en Docker Hub: un enlace a GitHub, notas de los tags...
-->
```

Además, los avisos `> [!NOTE]` se convierten en texto que Docker Hub sí muestra, y los enlaces a secciones (`#seccion`) pasan a apuntar al README en GitHub. Si el resultado supera los 25.000 bytes que admite Docker Hub, el workflow falla y dice cuánto sobra.

Para usarlo en un proyecto, `.github/workflows/dockerhub-description.yml`:

```yaml
name: Docker Hub description
on:
  push:
    branches: [main]
    paths: [README.md, .github/workflows/dockerhub-description.yml]
  workflow_dispatch:
jobs:
  sync:
    uses: dgongut/.github/.github/workflows/dockerhub-description.yml@main
    secrets: inherit
```

y en el repo, los secretos `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN` (un token de Docker Hub con permisos *Read, Write, Delete*).

Para probarlo en local:

```bash
python3 scripts/dockerhub_readme.py README.md DOCKERHUB.md https://github.com/dgongut/proyecto
```
