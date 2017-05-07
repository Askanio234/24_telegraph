from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///telegraph.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

Base.query = db_session.query_property()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    post_url = Column(String(150), unique=True, index=True)
    post_header = Column(String(300))
    post_singature = Column(String(200))
    post_body = Column(String(5000))

    def __str__(self):
        return "post titled {} by {}".format(self.post_header, self.post_singature)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
