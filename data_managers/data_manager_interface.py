from abc import ABC, abstractmethod



class DataManagerInterface(ABC):

    @abstractmethod
    def list_all_users(self):
        pass

    @abstractmethod
    def list_user_movies(self, user_id):
        pass



