from lib.skill import Skill


class SkillFactory:
    def __init__(self, raw_skill):
        self.raw_skill = raw_skill
        status, _, level, *skill_type = raw_skill.split()
        self.status = status
        self.level = float(level)
        self.skill_type = " ".join(skill_type)

    def new(self):
        return Skill(level=self.level, skill_type=self.skill_type, status=self.status)
