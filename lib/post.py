from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    key = Column(String)
    from_network = Column(String)
    url = Column(String)
    use_on_twitter = Column(Boolean)
    use_on_pinterest = Column(Boolean)
    posted_at = Column(DateTime)
    md5 = Column(String)
    url_target = Column(String)
