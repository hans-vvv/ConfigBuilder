# app/printers.py
from __future__ import annotations

import re
from pathlib import Path
from typing import Mapping, Optional
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

PathLike = str | Path


class Printer:
    """
    Minimal printer:
      - render(): pure -> { primary_key: text }
      - render_to_files(): writes files -> [Path]

    Notes:
      - If template_dir is None and template_name is an absolute path,
        template_dir is derived from it.
      - In per-primary-key mode, output filenames are sanitized from keys.
    """

    def __init__(
        self,
        *,
        config_tree: Mapping,
        template_name: str,
        template_dir: Optional[PathLike] = None,
        output_dir: PathLike = "output_configs",
        trim_blocks: bool = True,
        lstrip_blocks: bool = True,
        render_per_primary_key: bool = True,
        filename_suffix: str = "-cfg",
        autoload_env: bool = False,  # build Jinja env now or lazily in render()
    ) -> None:
        self.config_tree: Mapping = config_tree
        self.template_name: str = template_name
        self.output_dir: Path = Path(output_dir)
        self.trim_blocks = trim_blocks
        self.lstrip_blocks = lstrip_blocks
        self.render_per_primary_key = render_per_primary_key
        self.filename_suffix = filename_suffix

        # Resolve template_dir/name if an absolute template path was passed
        if template_dir is None:
            p = Path(template_name)
            if p.is_absolute():
                self.template_dir = p.parent
                self.template_name = p.name
            else:
                raise ValueError("template_dir is required when template_name is not an absolute path.")
        else:
            self.template_dir = Path(template_dir)

        self.env: Optional[Environment] = None
        if autoload_env:
            self._ensure_env()

    # ---------------------------
    # Public API
    # ---------------------------
    def render(self) -> dict[str, str]:
        """
        Pure render. Returns {primary_key: normalized_text}.
        In single-file mode, returns {"all": normalized_text}.
        """
        self._ensure_env()

        try:
            template = self.env.get_template(self.template_name)  # type: ignore[arg-type]
        except TemplateNotFound as e:
            td = str(self.template_dir.resolve())
            raise ValueError(f"Template not found: name='{self.template_name}', dir='{td}'") from e

        if self.render_per_primary_key:
            plan = self._plan_per_primary_key(self.config_tree)
            outputs: dict[str, str] = {}
            for primary_key, sub_tree in plan.items():
                text = template.render(sub_tree=sub_tree)
                outputs[str(primary_key)] = self._normalize_text(text)
            return outputs

        # Single-file (aggregate) mode
        text = template.render(sub_tree=self.config_tree)
        return {"all": self._normalize_text(text)}

    def render_to_files(self) -> list[Path]:
        """
        Renders then writes to disk. Returns a list of written Paths.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)
        outputs = self.render()

        written: list[Path] = []
        for primary_key, text in outputs.items():
            fname = f"{self._slug(primary_key)}{self.filename_suffix}"
            path = self.output_dir / fname
            path.parent.mkdir(parents=True, exist_ok=True)
            # explicit context manager
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            written.append(path)
        return written

    # ---------------------------
    # Internals
    # ---------------------------
    def _ensure_env(self) -> None:
        if self.env is None:
            self.env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                trim_blocks=self.trim_blocks,
                lstrip_blocks=self.lstrip_blocks,
            )

    def _plan_per_primary_key(self, config_tree: Mapping) -> dict[str, dict]:
        """
        Build {primary_key: subtree} with deterministic order.
        Primary keys are taken from top-level keys of config_tree.
        """
        plan: dict[str, dict] = {}
        # Sort robustly even if keys aren't strings
        for pk in sorted(config_tree.keys(), key=lambda k: str(k).lower()):
            plan[str(pk)] = dict(config_tree[pk])  # shallow copy
        return plan

    @staticmethod
    def _normalize_text(s: str) -> str:
        # Normalize line endings, trim trailing spaces, ensure trailing newline
        s = s.replace("\r\n", "\n")
        s = "\n".join(line.rstrip() for line in s.split("\n"))
        if not s.endswith("\n"):
            s += "\n"
        return s

    @staticmethod
    def _slug(s: str) -> str:
        # Lowercase, spaces->dashes, safe chars only; fallback if empty
        slug = re.sub(r"\s+", "-", str(s).strip().lower())
        slug = re.sub(r"[^a-z0-9._-]", "", slug)
        return slug or "unnamed"