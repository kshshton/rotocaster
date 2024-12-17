

class ProfilesManager:
    def __init__(self):
        self.__profiles: dict = {}
        self.__active_profile: str = None

    @property
    def profiles(self) -> dict:
        return self.__profiles
    
    @profiles.setter
    def profiles(self, profiles) -> None:
        self.__profiles = profiles

    @property
    def active_profile(self) -> None:
        return self.__active_profile
    
    @active_profile.setter
    def active_profile(self, name: str) -> None:
        self.__active_profile = name

    @active_profile.deleter
    def active_profile(self) -> None:
        if len(self.list_profiles()) == 1:
            self.create_profile("")
        del self.__profiles[self.active_profile]
    
    @property
    def active_profile_value(self) -> int:        
        return self.__profiles[self.__active_profile]
    
    @active_profile_value.setter
    def active_profile_value(self, value: int) -> None:
        self.__profiles[self.__active_profile] = value

    def create_profile(self, name: str) -> None:
        if "" in self.list_profiles():
            self.delete_profile("")
        self.__profiles[name] = 0

    def is_profile_active(self) -> bool:
        return bool(self.__active_profile)
    
    def delete_profile(self, name: str) -> None:
        del self.__profiles[name]
    
    def select_profile(self, name: str) -> None:
        self.__active_profile = name

    def list_profiles(self) -> list:
        try:
            profiles = list(self.__profiles.keys())
            if len(profiles) > 1 and "" in profiles:
                del self.__profiles[""]
            return sorted(profiles)
        except:
            return []
    
    def first_profile(self) -> str:
        profiles = self.list_profiles()
        first_profile = next(iter(profiles), "")
        self.__active_profile = first_profile
        return first_profile