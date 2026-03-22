"""
Get directory for save data.

If script is `find_products` - inside user `save_json_dir` create directory
`{cnt}__{create_dt}`

else - use last directory by {cnt}
"""
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class SaveSettings(BaseModel):
    save_json_dir: Path = Path("saved_json_data")
    auto_create: bool = False

    @property
    def pages_dir(self) -> Path:
        p_dir = self.save_json_dir / "pages"
        p_dir.mkdir(parents=True, exist_ok=True)
        return p_dir

    @property
    def count_products_dir(self) -> Path:
        c_dir = self.save_json_dir / "count_products"
        c_dir.mkdir(parents=True, exist_ok=True)
        return c_dir

    @property
    def cards_dir(self) -> Path:
        c_dir = self.save_json_dir / "cards"
        c_dir.mkdir(parents=True, exist_ok=True)
        return c_dir

    def model_post_init(self, context: Any) -> None:
        """
        For find product create new dir for results
        Other use last created directory
        """
        self.save_json_dir.mkdir(parents=True, exist_ok=True)
        exists_dirs = {
            int(d.name.split("_")[0]): d
            for d in self.save_json_dir.glob("*") if d.is_dir()
        }

        last_save_dir = None
        if len(exists_dirs) != 0:
            last_save_dir = exists_dirs[max(exists_dirs)]

        if self.auto_create:
            create_dt = datetime.now().strftime("%Y_%m_%d__%H_%M_%S_%f")
            if last_save_dir is None:
                new_path = f"0__{create_dt}"
            else:
                new_path = f"{max(exists_dirs) + 1}__{create_dt}"
            new_save_dir = self.save_json_dir / new_path
            new_save_dir.mkdir(parents=True, exist_ok=True)

            object.__setattr__(self, "save_json_dir", new_save_dir)
        else:
            if last_save_dir is None:
                raise f'Error: first start script for find all products'
            object.__setattr__(self, "save_json_dir", last_save_dir)

    def __str__(self):
        """Show settings"""
        str_list = [
            "",
            "Save",
            f" - auto_create: {self.auto_create}",
            f" - save_json_dir: {self.save_json_dir.resolve()}"
        ]
        return "\n".join(str_list)
