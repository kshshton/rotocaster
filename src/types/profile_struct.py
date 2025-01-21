from dataclasses import dataclass, field


@dataclass
class ProfileStruct:
    steps: dict[str, dict] = field(default_factory=dict)

    def to_dict(self) -> dict[str, dict]:
        return {
            "steps": self.steps,
        }
